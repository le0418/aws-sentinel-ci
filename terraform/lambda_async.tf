resource "aws_lambda_function_event_invoke_config" "sentinel_detector" {
  function_name = aws_lambda_function.sentinel_detector.function_name

  maximum_retry_attempts       = 1
  maximum_event_age_in_seconds = 300
}
