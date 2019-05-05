from __future__ import print_function
from flask import Response
from flask_restful import Resource
import boto3
import json, os

queue_url = os.environ.get('SQS_QUEUE_URL')
token = os.environ.get('HIREFIRE_TOKEN')

class HiFire(Resource):

    def get(self, hifire_token):
        if hifire_token == token:
            sqs = boto3.client('sqs')
            queueAtr = sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['ApproximateNumberOfMessages']
            )
            messageCount = queueAtr['Attributes']['ApproximateNumberOfMessages']
            response = Response(
                response=json.dumps( dict( name= "worker", quantity=messageCount )),
                status=200, mimetype='application/json' )

            return response


