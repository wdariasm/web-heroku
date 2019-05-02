from __future__ import print_function
from flask import request, Response
from flask_restful import Resource
import uuid, datetime, os
import boto3
from boto3.dynamodb.conditions import Attr
from passlib.hash import sha256_crypt
import jwt, json

region = os.environ.get('AWS_DEFAULT_REGION')
dynamodb = boto3.resource('dynamodb', region_name=region)
SECRET_KEY = 'hZBIRNBFzHGxl4GjcOKOVXzrYTNJBZvtwJVvF4nrHnTqa-vel6vtJ2LVIZE-yYFhzQrO0riQ8WHvDlb3Z0mOUhE'

tabla_usuario = dynamodb.Table( 'Usuario' )

def encode_auth_token(self, user_id, email):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
            'iat': datetime.datetime.utcnow(),
            'user_id': user_id,
            'email': email
        }

        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e

class Healthys(Resource):
    def get(self):
        response = Response(
            response=json.dumps(dict( estado='ok')),
            status=200, mimetype='application/json')
        return response

class Users(Resource):
    def post(self):
        content = request.get_json(force=True)
        responseEmail = tabla_usuario.scan(
            FilterExpression=Attr('email').eq(content['email'])
        )

        if (responseEmail['Count'] > 0):
            response = Response(
                response=json.dumps( dict( error='Usuario ya se encuentra registrado' ) ),
                status=400, mimetype='application/json' )
            return response

        id = str(uuid.uuid4())
        password = sha256_crypt.encrypt( content['password'] )

        respuesta = tabla_usuario.put_item(
            Item={
                'email': content['email'],
                'password': password,
                'first_name': content['first_name'],
                'last_name': content['last_name'],
                'id': id
            }
        )
        return respuesta

class UserLogin(Resource):
    def post(self):
        content = request.get_json( force=True )
        responseUser = tabla_usuario.scan(
            FilterExpression=Attr( 'email' ).eq( content['username'] )
        )

        if(responseUser['Count'] == 0):
            response = Response(
                response=json.dumps( dict( error='Usuario No Registrado' ) ),
                status=400, mimetype='application/json' )
            return response

        item= responseUser['Items'][0]
        passwordHash = item['password']
        #print(item)
        if (sha256_crypt.verify(content['password'], passwordHash)):
            token = encode_auth_token(self, item['id'], item['email'])
            response = Response(
                response=json.dumps( dict( token=token.decode('utf-8') ) ),
                status=200, mimetype='application/json' )
            return response

        response = Response(
                response=json.dumps( dict( error='Usuario No Registrado' ) ),
                status=400, mimetype='application/json' )
        return response