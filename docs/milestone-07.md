# Milestone 7 — AWS Lambda Failure Recovery and SQS Integration

## Objective

Implement resilient asynchronous failure handling for the AWS Sentinel-CI security detection Lambda using Amazon SQS, least-privilege IAM, and Terraform.

Validate the architecture through controlled failure injection, retry exhaustion, failure-record preservation, and restoration of normal security-event processing.

## Architecture

Synthetic Security Event
    |
    v
Amazon EventBridge
    |
    v
AWS Lambda — sentinel-ci-detector
    |
    +-- Successful processing --> S3 Security Findings
    |
    +-- Failed asynchronous invocation
            |
            v
       Lambda retry
            |
            v
       SQS OnFailure Destination

CloudWatch Logs provides operational visibility into invocation failures.

## Infrastructure as Code

### Amazon SQS

Terraform file: `terraform/sqs.tf`

Queue name: `sentinel-ci-failed-events`

Security and operational settings:

- SQS-managed encryption
- Four-day message retention
- Ten-second receive-message wait time
- Thirty-second visibility timeout

### Least-Privilege IAM

Terraform file: `terraform/failure_queue_iam.tf`

The Lambda execution role receives `sqs:SendMessage` permission scoped to the designated failure queue.

This avoids granting unrestricted SQS access.

### Lambda Asynchronous Invocation Configuration

Terraform file: `terraform/lambda_async.tf`

Verified settings:

- Maximum retry attempts: 1
- Maximum event age: 300 seconds
- OnFailure destination: `sentinel-ci-failed-events`

The destination preserves failed asynchronous invocation records after retry exhaustion.

## Controlled Failure Test

A temporary test condition was introduced into the Lambda handler.

The condition required:

- A specific controlled-failure event ID
- `simulation: true`
- An enabled test-only environment flag

The controlled test raised:

`RuntimeError: MILESTONE07_CONTROLLED_FAILURE_TEST`

The synthetic event was submitted through Amazon EventBridge.

### Observed Results

- EventBridge accepted the test event.
- CloudWatch recorded two failed Lambda invocation attempts.
- Lambda reported retry exhaustion.
- Amazon SQS received the asynchronous failure record.

The failure record contained:

- Event ID: `MILESTONE07-CONTROLLED-FAILURE`
- Condition: `RetriesExhausted`
- Approximate invocation count: 2
- Error type: `RuntimeError`
- Error message: `MILESTONE07_CONTROLLED_FAILURE_TEST`

Sanitized evidence is available in:

`evidence/milestone-07/sqs-failure-record-public.json`

## Production Restoration

After the controlled-failure test:

1. The original Lambda handler was restored.
2. The temporary failure-test environment flag was removed.
3. The production-safe deployment package was rebuilt.
4. Python unit tests passed.
5. Terraform successfully updated the Lambda.
6. AWS confirmed the Lambda was Active with a Successful update status.
7. The permanent SQS OnFailure destination remained configured.

The temporary failure-injection code was not retained in the production handler.

## Recovery Validation

A new synthetic RF anomaly event was submitted after restoration.

Event ID:

`MILESTONE07-RECOVERY-20261118200431`

The restored Lambda generated a structured security finding containing:

- Finding: `HIGH_RISK_ACTIVITY_DETECTED`
- Severity: `HIGH`
- Simulation: `true`
- Incident-response action: `SIMULATED_ESCALATION`
- Real response executed: `false`

The finding was persisted to the S3 evidence bucket.

### Evidence Integrity

The downloaded finding was independently hashed using SHA-256.

The calculated digest matched the digest embedded in the S3 object key:

`599b4428f6888fec60dae667e567d836cbec16bc400498934c2ebe7b5dff27f2`

This verifies consistency between the downloaded object and its content-addressed key.

It does not independently establish evidence immutability or chain of custody.

## SQS Cleanup

After the recovery test:

- The remaining SQS message was verified as the original controlled-failure record.
- The verified test message was deleted.
- SQS reported zero visible, in-flight, and delayed messages.

The SQS queue and permanent failure-destination configuration remain deployed.

## Automated Testing

The Python unit test suite completed successfully with 24 passing tests during Milestone 7 verification.

## Evidence

Supporting screenshots and sanitized JSON artifacts are located in:

`evidence/milestone-07/`

Evidence includes Terraform plans, infrastructure verification, controlled failure injection, CloudWatch results, SQS failure preservation, production restoration, SHA-256 integrity validation, and queue cleanup.

## Security Considerations

- All telemetry is synthetic.
- Incident-response escalation is simulated.
- No real containment action is executed.
- SQS permissions are restricted to the designated queue.
- The controlled-failure mechanism was removed after testing.
- The original SQS failure record is excluded from Git.
- A sanitized failure record is provided for portfolio review.

## Operational Limitations

The implementation preserves failed asynchronous invocations but does not provide automatic message replay.

SQS message retention is limited to four days.

The solution is a controlled security engineering demonstration, not a production incident-response service.

## Cost and Teardown

The deployed Lambda, SQS, EventBridge, S3, and CloudWatch resources may incur AWS charges.

Before teardown, review the Terraform destroy plan and confirm that required evidence has been retained.

Do not destroy the infrastructure until all verification and evidence collection are complete.