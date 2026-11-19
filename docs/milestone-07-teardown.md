# AWS Sentinel-CI — Milestone 7 Teardown Report

**Date:** November 18, 2026  
**AWS Region:** us-east-1  
**Project:** AWS Sentinel-CI  
**Status:** Teardown completed and verified

## Executive Summary

The AWS Sentinel-CI deployment was successfully removed
after completion of Milestone 7 testing and evidence collection.

Terraform reported:

```text
Apply complete! Resources: 0 added, 0 changed, 16 destroyed.
```

## 1. Evidence Preservation

Before destroying the infrastructure:

- The S3 evidence bucket was inventoried.
- Three object versions were identified.
- Evidence files were backed up outside the Git repository.
- Backup integrity was verified using SHA-256 comparisons.
- The Terraform destroy plan was reviewed.

## 2. S3 Cleanup

The three verified S3 object versions were deleted using
AWS CLI.

Subsequent verification confirmed:

```text
Remaining object versions: 0
Remaining delete markers: 0
Total Objects: 0
Total Size: 0
```

## 3. Terraform Infrastructure Teardown

The saved Terraform destroy plan identified:

```text
Plan: 0 to add, 0 to change, 16 to destroy.
```

Terraform successfully destroyed all 16 planned resources.

The teardown included:

- AWS Lambda function and invocation configuration
- Amazon EventBridge rule and target
- Amazon SQS failure destination
- Amazon CloudWatch Logs log group
- AWS IAM role and associated policies
- Amazon S3 evidence bucket and its configurations

## 4. Post-Teardown Verification

Terraform state verification confirmed zero remaining
managed AWS resources.

Independent AWS CLI checks returned:

| Service | Verification |
|---|---|
| Lambda | ResourceNotFoundException |
| EventBridge | ResourceNotFoundException |
| SQS | NonExistentQueue |
| S3 | HTTP 404 |
| IAM | NoSuchEntity |
| CloudWatch Logs | Empty log group result |

These checks confirm removal of the named Sentinel-CI
resources. They do not constitute a full account-wide
billing or resource audit.

## 5. Evidence Screenshots

| Screenshot | Description |
|---|---|
| [26](../evidence/milestone-07/26-teardown-precheck.png) | Pre-teardown checks |
| [27](../evidence/milestone-07/27-s3-evidence-backup.png) | S3 evidence backup |
| [28](../evidence/milestone-07/28-terraform-destroy-plan.png) | Original Terraform destroy plan, captured after teardown |
| [30](../evidence/milestone-07/30-s3-bucket-empty-verification.png) | S3 bucket emptiness verification |
| [31](../evidence/milestone-07/31-terraform-destroy-complete.png) | Successful Terraform teardown |
| [32](../evidence/milestone-07/32-terraform-state-empty.png) | Empty Terraform state |
| [33](../evidence/milestone-07/33-aws-resource-removal-verification.png) | Independent AWS CLI verification |
| [34](../evidence/milestone-07/34-final-teardown-git-security-review.png) | Final Git security review |

The S3 deletion was confirmed by AWS CLI output in the
project execution session. Screenshot 29 was not captured;
the deletion was not rerun.

## 6. Security and Cost Controls

- Temporary S3 deletion manifest removed.
- Terraform state and saved plans excluded from Git.
- No matching sensitive filenames detected among tracked files.
- Source code, documentation, and screenshots preserved.
- Project infrastructure removed to reduce ongoing AWS costs.

## Final Result

**Milestone 7 infrastructure teardown: COMPLETE**

The project retains its source code and supporting evidence
for portfolio review and future reconstruction.