# AWS Sentinel-CI

## Automated Threat Detection, Incident Response, and Failure Recovery

AWS Sentinel-CI is a cloud security engineering portfolio project that demonstrates automated security-event processing using AWS services, Python, and Terraform.

The project processes synthetic security telemetry, detects high-risk activity, preserves findings in Amazon S3, and captures failed asynchronous AWS Lambda invocations in Amazon SQS.

All incident-response actions are simulation-only.

## Architecture

EventBridge (Synthetic Security Telemetry)
    |
    v
AWS Lambda (Python Threat Detection)
    |
    +-- Successful Processing --> Amazon S3 (Security Findings)
    |
    +-- Failed Asynchronous Invocation
            |
            v
       Lambda Retry
            |
            v
       Amazon SQS (OnFailure Destination)

Supporting services:
- AWS IAM for least-privilege access
- Amazon CloudWatch Logs for operational visibility
- Terraform for infrastructure provisioning
- Python unittest for automated testing

## Security Engineering Capabilities

- Event-driven security telemetry processing
- Python-based threat detection and event validation
- Automated security finding generation
- Simulated incident-response escalation
- S3 evidence preservation and SHA-256 integrity verification
- Least-privilege IAM policies
- Lambda asynchronous invocation retry configuration
- SQS failure destination for exhausted retries
- Infrastructure as Code using Terraform
- Controlled failure testing and operational recovery

## AWS Services

- Amazon EventBridge
- AWS Lambda
- Amazon S3
- Amazon SQS
- AWS Identity and Access Management
- Amazon CloudWatch

## Technology Stack

- Python 3.14 Lambda runtime
- Terraform
- AWS CLI
- Docker
- Windows PowerShell
- Git and GitHub

## Verified Testing

The project has demonstrated:

1. Successful synthetic security-event ingestion through EventBridge.
2. Lambda-based detection of high-risk activity.
3. Persistence of structured security findings in Amazon S3.
4. SHA-256 verification of downloaded evidence.
5. Controlled Lambda execution failure.
6. Asynchronous retry behavior with two invocation attempts.
7. Preservation of the failed invocation in Amazon SQS.
8. Restoration of the production-safe Lambda configuration.
9. Successful processing of a new synthetic event after recovery.
10. Removal of the controlled-failure SQS test message.

The automated Python test suite passed 24 tests during Milestone 7 verification.

## Security and Safety

This project uses synthetic telemetry and simulated incident-response actions.

No real containment, isolation, or destructive incident-response actions are executed.

Sensitive operational evidence and temporary deployment artifacts are excluded from version control.

## Repository Structure

- `src/` - Security detection and Lambda application code
- `terraform/` - AWS infrastructure definitions
- `tests/` - Automated Python tests
- `evidence/` - Verification screenshots and sanitized artifacts
- `docs/` - Technical documentation
- `scripts/` - Supporting scripts

## Technical Documentation

See [Milestone 7: Lambda Failure Recovery](docs/milestone-07.md) for the detailed failure-recovery implementation and validation results.

## Cost and Resource Management

AWS resources may incur charges while deployed.

Review Lambda, SQS, EventBridge, S3, and CloudWatch usage and remove resources when they are no longer needed.

Terraform-managed infrastructure should be reviewed with `terraform plan -destroy` before any teardown.

## Project Status

Milestones 1-7: Implemented and tested in a controlled AWS environment.

The deployed resources may be removed after evidence collection and portfolio validation.