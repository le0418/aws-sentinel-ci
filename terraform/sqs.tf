resource "aws_sqs_queue" "failed_events" {
  name = "sentinel-ci-failed-events"

  message_retention_seconds = 345600
  receive_wait_time_seconds = 10

  sqs_managed_sse_enabled = true

  tags = {
    Project     = "aws-sentinel-ci"
    Environment = "lab"
    Purpose     = "security-event-failure-recovery"
  }
}
