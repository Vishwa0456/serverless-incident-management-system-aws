import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

INCIDENTS_TABLE = os.environ['INCIDENTS_TABLE']
ACTIVITY_TABLE = os.environ['ACTIVITY_TABLE']

incidents_table = dynamodb.Table(INCIDENTS_TABLE)
activity_table = dynamodb.Table(ACTIVITY_TABLE)

def lambda_handler(event, context):
    try:
        incident_id = event['pathParameters']['incidentId']
        body = json.loads(event.get('body', '{}'))
        new_status = body.get('status')
        action_by = body.get('actionBy', 'System')

        if not new_status:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'status is required'})
            }

        now = datetime.utcnow().isoformat()

        incidents_table.update_item(
            Key={'incidentId': incident_id},
            UpdateExpression="SET #s = :s, updatedAt = :u",
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={
                ':s': new_status,
                ':u': now
            }
        )

        activity_table.put_item(
            Item={
                'activityId': str(uuid.uuid4()),
                'incidentId': incident_id,
                'actionType': 'STATUS_UPDATED',
                'actionBy': action_by,
                'actionTime': now,
                'details': f'Status changed to {new_status}'
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Incident status updated successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error updating incident status', 'error': str(e)})
        }
