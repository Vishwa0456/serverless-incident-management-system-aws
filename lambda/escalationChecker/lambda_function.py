import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

INCIDENTS_TABLE = os.environ['INCIDENTS_TABLE']
ACTIVITY_TABLE = os.environ['ACTIVITY_TABLE']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

incidents_table = dynamodb.Table(INCIDENTS_TABLE)
activity_table = dynamodb.Table(ACTIVITY_TABLE)

def lambda_handler(event, context):
    try:
        response = incidents_table.scan()
        incidents = response.get('Items', [])
        now = datetime.utcnow()

        escalated_count = 0

        for incident in incidents:
            status = incident.get('status')
            sla_deadline = incident.get('slaDeadline')

            if status in ['Closed', 'Resolved']:
                continue

            if sla_deadline:
                deadline_dt = datetime.fromisoformat(sla_deadline)
                if now > deadline_dt:
                    incident_id = incident['incidentId']

                    activity_table.put_item(
                        Item={
                            'activityId': str(uuid.uuid4()),
                            'incidentId': incident_id,
                            'actionType': 'ESCALATED',
                            'actionBy': 'System',
                            'actionTime': now.isoformat(),
                            'details': 'Incident breached SLA and was escalated'
                        }
                    )

                    sns.publish(
                        TopicArn=SNS_TOPIC_ARN,
                        Subject=f'SLA Breach Alert - {incident_id}',
                        Message=f'Incident {incident_id} breached SLA and requires attention.'
                    )

                    escalated_count += 1

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Escalation check completed',
                'escalatedCount': escalated_count
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error checking escalations', 'error': str(e)})
        }
