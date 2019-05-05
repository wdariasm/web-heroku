from __future__ import print_function
from flask import Flask
from flask import request, Response
from flask_restful import Api
from flask_cors import CORS
from flask_restful import Resource
from botocore.exceptions import ClientError
import json, redis, uuid, os, datetime



app = Flask( __name__ )
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

url_cache = os.environ.get( 'MEMCACHEDCLOUD_SERVERS' )
user_cache = os.environ.get( 'MEMCACHEDCLOUD_USERNAME' )
pass_cache = os.environ.get( 'MEMCACHEDCLOUD_PASSWORD' )


def ConexionRedis():
    r = redis.StrictRedis( host=url_cache, port=6379, db=0, socket_timeout=1, decode_responses=True )
    return r

class TestRedis(Resource):
    def get(self):
        con_redis = ConexionRedis()
        list_data = []
        for key in con_redis.scan_iter( "concurso:*" ):
            print(key)
            datos = con_redis.hgetall(key)
            list_data.append(datos)

        return list_data

    def post(self):
        try:
            content = request.get_json()

            id = str(uuid.uuid4())
            filename = "static/images/" + id + ".mp3"
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            nombre_hash = 'concurso:'+ id

            datos_concurso = {
                'Nombre': content['Nombre'],
                'Url_Concurso': content['Url'],
                'Fecha_Fin': content['Fecha_Fin'],
                'Fecha_Inicio': content['Fecha_Inicio'],
                'Premio': content['Premio'],
                'Guion': content['Guion'],
                'Recomendaciones': content['Recomendaciones'],
                'Imagen': '',
                'Owner_id': content['Owner_id'],
                'id': id,
                'Fecha_Creacion': fecha
            }
            print(datos_concurso)
            con_redis = ConexionRedis()
            print("Conexion redis -- " + str(con_redis))
            response = con_redis.hmset(nombre_hash, datos_concurso)

            return response

        except ClientError as error:
            print('Error boto: ' +  error['message'] )

        except Exception as ex:
            print( 'Error general ' + str(ex) )


api.add_resource(TestRedis, '/api/redis/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
