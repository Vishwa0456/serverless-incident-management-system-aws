import json
import boto3
import os
import uuid
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

INCIDENTS_TABLE = os.environ['INCIDENTS_TABLE']
ACTIVITY_TABLE = os.environ['ACTIVITY_TABLE']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

incidents_table = dynamodb.Table(INCIDENTS_TABLE)
activity_table = dynamodb.Table(ACTIVITY_TABLE)

def get_sla_deadline(severity):
    now = datetime.utcnow()
    if severity == "Critical":
        return (now + timedelta(hours=1)).isoformat()
    elif severity == "High":
        return (now + timedelta(hours=4)).isoformat()
    elif severity == "Medium":
        return (now + timedelta(hours=8)).isoformat()
    else:
        return (now + timedelta(hours=24)).isoformat()

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        title = body.get('title')
        description = body.get('description')
        severity = body.get('severity')
        category = body.get('category')
        created_by = body.get('createdBy')

        if not title or not description or not severity or not category or not created_by:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required fields'})
            }

        now = datetime.utcnow().isoformat()
        incident_id = f"INC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        sla_deadline = get_sla_deadline(severity)

        incident_item = {
            'incidentId': incident_id,
            'title': title,
            'description': description,
            'severity': severity,
            'category': category,
            'status': 'Open',
            'createdBy': created_by,
            'assignedTo': 'Unassigned',
            'createdAt': now,
            'updatedAt': now,
            'slaDeadline': sla_deadline
        }

        incidents_table.put_item(Item=incident_item)

        activity_table.put_item(
            Item={
                'activityId': str(uuid.uuid4()),
                'incidentId': incident_id,
                'actionType': 'CREATED',
                'actionBy': created_by,
                'actionTime': now,
                'details': f'Incident created with severity {severity}'
            }
        )

        if severity in ['High', 'Critical']:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f'{severity} Incident Alert - {incident_id}',
                Message=f'Incident {incident_id} created.\nTitle: {title}\nSeverity: {severity}\nCategory: {category}\nCreated By: {created_by}'
            )

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Incident created successfully',
                'incident': incident_item
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error creating incident', 'error': str(e)})
        }
