from __future__ import print_function
import boto3
import os

region = os.environ.get('AWS_DEFAULT_REGION')

dynamodb = boto3.resource('dynamodb', region_name=region)

"""
table1 = dynamodb.Table('Usuario')
table1.delete()

table2 = dynamodb.Table('Concurso')
table2.delete()

table3 = dynamodb.Table('Grabacion')
table3.delete()

table4 = dynamodb.Table('BatchLog')
table4.delete() """

tablaUsuario = dynamodb.create_table(
    TableName='Usuario',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH' #Partition key
        },
        {
            'AttributeName': 'email',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)


tabla_concurso = dynamodb.create_table(
    TableName='Concurso',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH' #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Owner_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Url_Concurso',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'concurso_owner_index',
            'KeySchema': [
                {
                    'AttributeName': 'Owner_id',
                    'KeyType': 'HASH'
                },
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        },
        {
            'IndexName': 'concurso_url_index',
            'KeySchema': [
                {
                    'AttributeName': 'Url_Concurso',
                    'KeyType': 'HASH'
                },
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }
    ]
)

tabla_grabacion = dynamodb.create_table(
    TableName='Grabacion',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH' #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Concurso_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Estado_Archivo',
            'AttributeType': 'S'
        }

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'grabacion_concurso_index',
            'KeySchema': [
                {
                    'AttributeName': 'Concurso_id',
                    'KeyType': 'HASH'
                },
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        },
        {
            'IndexName': 'grabacion_estado_index',
            'KeySchema': [
                {
                    'AttributeName': 'Estado_Archivo',
                    'KeyType': 'HASH'
                },
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }
    ]
)

tabla_batchLog = dynamodb.create_table(
    TableName='BatchLog',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH' #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)




#print("Tabla Usuario status:", tablaUsuario.table_status)

print("Tabla Concurso status:", tabla_concurso.table_status)

print("Tabla Grabacion status:", tabla_grabacion.table_status)

print("Tabla BatchLog status:", tabla_batchLog.table_status)

