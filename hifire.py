from __future__ import print_function
from flask import Flask
from flask import request, Response
from flask_restful import Api
from flask_cors import CORS
from flask_restful import Resource
import boto3
import json, os

queue_url = os.environ.get('SQS_QUEUE_URL')
token = os.environ.get('HIREFIRE_TOKEN')

app = Flask( __name__ )
api = Api(app)
cors = CORS(app, resources={r"/hirefire*": {"origins": "*"}})

class TestHiFire(Resource):

    def get(self, hifire_token):
        if hifire_token == token:
            sqs = boto3.client('sqs')
            queueAtr = sqs.get_queue_attributes(
                QueueUrl='string',
                AttributeNames=['ApproximateNumberOfMessages']
            )
            messageCount = queueAtr.Attributes.ApproximateNumberOfMessages
            response = Response(
                response=json.dumps( dict( name= "worker", quantity=messageCount )),
                status=200, mimetype='application/json' )

            return response


api.add_resource(TestHiFire, '/hirefire/<string:hifire_token>/info')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)