# Serverless Incident Management System on AWS

A production-style serverless incident management application built on AWS that allows users to create, view, assign, and update incidents through a web interface. The system tracks incident activity, stores incident records in DynamoDB, sends notifications for important events, and automatically checks for SLA breaches using EventBridge Scheduler.

---

## Project Overview

This project was built to simulate a lightweight incident management platform used in operations / support environments. It provides an end-to-end serverless workflow for incident lifecycle management, including:

- Incident creation
- Incident listing and detail retrieval
- Incident assignment
- Incident status updates
- Incident activity tracking
- SLA deadline monitoring
- Automated escalation alerts for breached incidents

The frontend is hosted on Amazon S3 as a static website, while backend APIs are exposed through Amazon API Gateway and implemented using AWS Lambda. Incident and activity data are stored in Amazon DynamoDB. Amazon SNS is used for alert notifications, and Amazon EventBridge Scheduler periodically triggers escalation checks.

---

## Architecture

### Frontend
- **Amazon S3** – Static website hosting for the incident dashboard and frontend pages

### API Layer
- **Amazon API Gateway** – Exposes REST-style HTTP endpoints for incident operations

### Compute
- **AWS Lambda** – Implements backend business logic for all incident workflows

### Database
- **Amazon DynamoDB**
  - `Incidents` table – stores incident records
  - `IncidentActivity` table – stores activity history / audit trail

### Notifications
- **Amazon SNS** – Sends incident alert / escalation notifications

### Scheduling / Automation
- **Amazon EventBridge Scheduler** – Invokes escalation checks periodically for SLA breach detection

### Monitoring / Debugging
- **Amazon CloudWatch Logs** – Used to monitor Lambda executions and troubleshoot failures

---

## Project Architecture Flow

1. User opens the frontend hosted on **Amazon S3**
2. Frontend calls backend APIs through **Amazon API Gateway**
3. API Gateway invokes the relevant **AWS Lambda** function
4. Lambda performs incident logic such as:
   - create incident
   - list incidents
   - fetch incident details
   - update incident status
   - assign incident
5. Incident records are stored in the **Incidents** DynamoDB table
6. Incident activity logs are stored in the **IncidentActivity** DynamoDB table
7. **SNS** sends notifications for important incident/escalation events
8. **EventBridge Scheduler** periodically invokes the escalation Lambda to identify incidents whose SLA deadline has passed

---

## Features

- Create incidents from a web form
- View all incidents in a dashboard
- View incident details and activity history
- Update incident status
- Assign incidents to a user / engineer
- Store activity trail for audit visibility
- Send escalation alerts for breached incidents
- Automatically check SLA deadlines on a recurring schedule

---

## AWS Services Used

- Amazon S3
- Amazon API Gateway
- AWS Lambda
- Amazon DynamoDB
- Amazon SNS
- Amazon EventBridge Scheduler
- Amazon CloudWatch Logs
- AWS IAM

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/incidents` | Create a new incident |
| `GET` | `/incidents` | List all incidents |
| `GET` | `/incidents/{incidentId}` | Get incident details and activity |
| `PATCH` | `/incidents/{incidentId}/status` | Update incident status |
| `PATCH` | `/incidents/{incidentId}/assign` | Assign an incident |

---

## Lambda Functions

- **CreateIncidentFunction** – Creates a new incident, stores it in DynamoDB, writes activity, and can trigger notifications
- **ListIncidentsFunction** – Returns all incidents
- **GetIncidentFunction** – Returns incident details and activity history
- **UpdateIncidentStatusFunction** – Updates incident status and logs the change
- **AssignIncidentFunction** – Assigns an incident to a user and logs the action
- **EscalationCheckerFunction** – Checks for incidents whose SLA deadline has passed and publishes escalation alerts

---

## DynamoDB Tables

### 1) Incidents
Stores the main incident record:
- incidentId
- title
- description
- severity
- category
- status
- createdBy
- assignedTo
- createdAt
- updatedAt
- slaDeadline

### 2) IncidentActivity
Stores the activity history for incidents:
- incidentId
- activityId
- actionType
- actionBy
- actionTime
- details

---

## Frontend Pages

- **Dashboard (`index.html`)** – Lists all incidents
- **Create Incident (`create-incident.html`)** – Form to create a new incident
- **Incident Details (`incident-details.html`)** – Shows incident information, activity history, status update form, and assignment form

---

## Project Structure

```text
serverless-incident-management-system/
├── lambda/
│   ├── create-incident/
│   │   └── lambda_function.py
│   ├── list-incidents/
│   │   └── lambda_function.py
│   ├── get-incident/
│   │   └── lambda_function.py
│   ├── update-status/
│   │   └── lambda_function.py
│   ├── assign-incident/
│   │   └── lambda_function.py
│   └── escalation-checker/
│       └── lambda_function.py
├── frontend/
│   ├── index.html
│   ├── create-incident.html
│   ├── incident-details.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── project-notes.txt
└── README.md

---

## How It Works

### Create Incident
The frontend sends a `POST /incidents` request to API Gateway. The Lambda function creates an incident ID, stores the incident in the `Incidents` table, writes an activity entry into `IncidentActivity`, and returns the created incident.

### View Incidents
The dashboard calls `GET /incidents` to fetch all incident records from DynamoDB.

### View Incident Details
The details page calls `GET /incidents/{incidentId}` to fetch both the incident record and the activity history.

### Update Status
The details page sends a `PATCH /incidents/{incidentId}/status` request. Lambda updates the incident status and logs the action in `IncidentActivity`.

### Assign Incident
The details page sends a `PATCH /incidents/{incidentId}/assign` request. Lambda updates the assignee and logs the assignment action.

### Escalation Check
EventBridge Scheduler periodically invokes `EscalationCheckerFunction`, which scans incidents, identifies records whose SLA deadline has passed, writes escalation activity, and publishes alert notifications using SNS.

---

## Prerequisites

To build and run this project, the following AWS services and tools are required:

- AWS account with access to S3, Lambda, API Gateway, DynamoDB, SNS, EventBridge Scheduler, IAM, and CloudWatch
- Basic knowledge of AWS serverless services
- Web browser for testing the frontend
- Git for version control
- Postman or browser developer tools for API testing

---

## Deployment Summary

The project was deployed in a serverless architecture using the following AWS setup:

- Frontend static website hosted in an Amazon S3 bucket
- Backend APIs exposed through Amazon API Gateway
- Lambda functions used for incident operations and escalation workflows
- DynamoDB used for storing incidents and activity history
- SNS used for notifications and escalation alerts
- EventBridge Scheduler used to trigger periodic SLA escalation checks
- CloudWatch Logs used for Lambda monitoring and troubleshooting

---

## Sample Incident Lifecycle

1. A user creates a new incident from the frontend form.
2. The frontend sends a request to API Gateway.
3. The Create Incident Lambda stores the incident in the `Incidents` table.
4. An activity log entry is created in the `IncidentActivity` table.
5. The incident appears on the dashboard page.
6. A user can open the incident details page and:
   - update the incident status
   - assign the incident to an engineer
7. Each change is stored as a new activity entry in DynamoDB.
8. EventBridge Scheduler periodically triggers the escalation Lambda.
9. If an incident crosses its SLA deadline, the escalation Lambda:
   - logs an escalation activity
   - sends an SNS alert notification

---

## Learning Outcomes

This project provided hands-on experience with:

- Designing a serverless application architecture on AWS
- Building API-driven Lambda workflows
- Using DynamoDB for operational application data
- Connecting frontend pages to API Gateway endpoints
- Hosting static frontend applications on Amazon S3
- Implementing automated background checks using EventBridge Scheduler
- Sending notifications with SNS
- Using CloudWatch Logs for debugging and monitoring

---

## Project Highlights

- End-to-end serverless incident workflow built on AWS
- Frontend integrated directly with API Gateway APIs
- Real-time incident creation, status update, and assignment workflows
- Activity tracking implemented as a separate audit trail table
- Automated SLA breach detection using scheduled Lambda execution
- Practical use of multiple AWS services in one integrated project

---

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Create Incident
![Create Incident](screenshots/create-incident.png)

### Incident Details
![Incident Details](screenshots/incident-details.png)

## Future Improvements

Possible production enhancements include:

- Authentication and role-based access control using Amazon Cognito
- Better search / filtering for incidents
- Pagination for large incident lists
- Severity-based routing and notification channels
- Dashboard metrics and SLA analytics
- CI/CD deployment pipeline for Lambda and frontend changes
- Infrastructure as Code using Terraform or AWS SAM / CloudFormation

---

## Author

**Vishwanath Veerapur**
