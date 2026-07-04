import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

INCIDENTS_TABLE = os.environ['INCIDENTS_TABLE']
ACTIVITY_TABLE = os.environ['ACTIVITY_TABLE']

incidents_table = dynamodb.Table(INCIDENTS_TABLE)
activity_table = dynamodb.Table(ACTIVITY_TABLE)

def lambda_handler(event, context):
    try:
        incident_id = event['pathParameters']['incidentId']

        incident_response = incidents_table.get_item(Key={'incidentId': incident_id})
        incident = incident_response.get('Item')

        if not incident:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Incident not found'})
            }

        activity_response = activity_table.scan()
        activity_items = activity_response.get('Items', [])
        incident_activity = [item for item in activity_items if item.get('incidentId') == incident_id]

        return {
            'statusCode': 200,
            'body': json.dumps({
                'incident': incident,
                'activity': incident_activity
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error fetching incident', 'error': str(e)})
        }
