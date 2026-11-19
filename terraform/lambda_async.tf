resource "aws_lambda_function_event_invoke_config" "sentinel_detector" {
  function_name = aws_lambda_function.sentinel_detector.function_name

  maximum_retry_attempts       = 1
  maximum_event_age_in_seconds = 300

  destination_config {
    on_failure {
      destination = aws_sqs_queue.failed_events.arn
    }
  }

  depends_on = [
    aws_iam_role_policy.lambda_failure_queue_send
  ]
}
