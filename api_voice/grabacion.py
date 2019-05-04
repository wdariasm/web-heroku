from __future__ import print_function
from flask import request
from flask_restful import Resource
import uuid, datetime, os, base64
import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

region = os.environ.get('AWS_DEFAULT_REGION')
dynamodb = boto3.resource('dynamodb', region_name=region)
tabla_grabacion = dynamodb.Table('Grabacion')

queue_url = os.environ.get('SQS_QUEUE_URL')


def enviar_mensaje_sqs(grabacion_id, concurso_id, autor):
    try:

        sqs = boto3.client('sqs')
        response = sqs.send_message(
            QueueUrl=queue_url,
           # DelaySeconds=5,
            MessageAttributes={
                'Grabacion_id': {
                    'DataType': 'String',
                    'StringValue': grabacion_id
                },
                'Concurso_id': {
                    'DataType': 'String',
                    'StringValue': concurso_id
                }
            },
            MessageBody=(
                'Nueva grabación subida por:  ' + autor
            ),
            MessageGroupId = grabacion_id
        )
        #print("ID Mensaje " +  response['MessageId'])
    except ClientError as error:
        print( error )
    except Exception as ex:
        print( ex )

class Grabacion(Resource):
    def post(self):
        try:
            content = request.form
            audio = content['Archivo_Original']
            id = str( uuid.uuid4() )

            format, audio_string = audio.split( ';base64,' )
            ext = format.split( '/' )[-1]
            filename = "original/" + id + "." + ext
            audio_data = base64.b64decode( audio_string )

            s3 = boto3.resource( 's3' )
            s3.Bucket( 'supervoices-app' ).put_object( Key=filename, Body=audio_data )

            fecha = datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S.%f' )
            observacion = content['Observaciones']
            if observacion == "":
                observacion = "Ninguna"

            respuesta = tabla_grabacion.put_item(
                Item={
                    'Nombre_Autor': content['Nombre_Autor'],
                    'Apellido_Autor': content['Apellido_Autor'],
                    'Mail_Autor': content['Mail_Autor'],
                    'Fecha_Publicacion': fecha,
                    'Archivo_Original': filename,
                    'Estado_Archivo': '0',
                    'Observaciones': observacion,
                    'Concurso_id': content['Concurso_id'],
                    'Archivo_Final': 'temp',
                    'id': id
                }
            )

            enviar_mensaje_sqs( id, content['Concurso_id'], content['Nombre_Autor'])
            return respuesta

        except ClientError as error:
            print(error)
        except Exception as ex:
            print(ex)


class ConcursoGrabacion(Resource):
    def get(self, concurso_id, estado):

        if(estado == '1'):
            response_grabacion = tabla_grabacion.query(
                #FilterExpression=Attr('Concurso_id').eq(concurso_id) & Attr( 'Estado_Archivo' ).eq('1')
                IndexName='grabacion_concurso_index',
                KeyConditionExpression=Key( 'Concurso_id' ).eq( concurso_id ),
                FilterExpression = Attr( 'Estado_Archivo' ).eq('1')
            )
        else:
            response_grabacion = tabla_grabacion.query(
                IndexName='grabacion_concurso_index',
                KeyConditionExpression=Key( 'Concurso_id' ).eq( concurso_id )
            )

        return response_grabacion['Items']

class TestGrabacion(Resource):
    def post(self):
        try:
            content = request.get_json( force=True)
            mensajes = int( content['mensajes'])
            respuesta = None
            for x in range(0, mensajes):
                id = str( uuid.uuid4())
                filename = "original/09804dfa-6455-49df-934c-4d7bea3bd772.ogg"
                fecha = datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S.%f' )

                respuesta = tabla_grabacion.put_item(
                    Item={
                        'Nombre_Autor': 'Test ' + str(x),
                        'Apellido_Autor': 'Grabacion ' + str(x),
                        'Mail_Autor': 'testheroku@yopmail.com',
                        'Fecha_Publicacion': fecha,
                        'Archivo_Original': filename,
                        'Estado_Archivo': '0',
                        'Observaciones': 'Ninguna',
                        'Concurso_id': 'a8b80a47-7a4a-428f-80e2-ea5bdef59a91',
                        'Archivo_Final': 'temp',
                        'id': id
                    }
                )
                enviar_mensaje_sqs( id, 'a8b80a47-7a4a-428f-80e2-ea5bdef59a91', 'Test ' + fecha)

            return respuesta

        except ClientError as error:
            print(error)
        except Exception as ex:
            print(ex)