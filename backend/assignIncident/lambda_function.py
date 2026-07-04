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
        assigned_to = body.get('assignedTo')
        action_by = body.get('actionBy', 'System')

        if not assigned_to:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'assignedTo is required'})
            }

        now = datetime.utcnow().isoformat()

        incidents_table.update_item(
            Key={'incidentId': incident_id},
            UpdateExpression="SET assignedTo = :a, updatedAt = :u",
            ExpressionAttributeValues={
                ':a': assigned_to,
                ':u': now
            }
        )

        activity_table.put_item(
            Item={
                'activityId': str(uuid.uuid4()),
                'incidentId': incident_id,
                'actionType': 'ASSIGNED',
                'actionBy': action_by,
                'actionTime': now,
                'details': f'Incident assigned to {assigned_to}'
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Incident assigned successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error assigning incident', 'error': str(e)})
        }
