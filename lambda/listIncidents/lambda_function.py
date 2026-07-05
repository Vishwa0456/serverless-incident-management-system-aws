import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
INCIDENTS_TABLE = os.environ['INCIDENTS_TABLE']
incidents_table = dynamodb.Table(INCIDENTS_TABLE)

def lambda_handler(event, context):
    try:
        response = incidents_table.scan()
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error fetching incidents', 'error': str(e)})
        }
