import os
import json

import boto3


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMO_DB_TABLE_NAME'])

    body = event['body-json']

    table.put_item(
        Item={
            'ID': body['key'],
            'Image': {
                'Name': body['key']
            },
            'User': {
                'Name': body['user']['name'],
                'Mail': body['user']['mail']
            }
        }
    )

    register_image_data = table.get_item(
        Key={
            'ID': body['key']
        }
    )

    return json.dumps(register_image_data['Item'])
