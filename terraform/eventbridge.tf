resource "aws_cloudwatch_event_rule" "sentinel_security_events" {
  name        = "sentinel-ci-security-events"
  description = "Routes synthetic Sentinel-CI security telemetry to the detector"

  event_pattern = jsonencode({
    source        = ["sentinel.ci"]
    "detail-type" = ["SecurityTelemetry"]
    detail = {
      simulation = [true]
      event_type = [
        "RF_ANOMALY",
        "UNAUTHORIZED_DEVICE",
        "SUSPICIOUS_NETWORK_CONNECTION"
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "sentinel_detector" {
  rule      = aws_cloudwatch_event_rule.sentinel_security_events.name
  target_id = "sentinel-ci-lambda-target"
  arn       = aws_lambda_function.sentinel_detector.arn

  input_path = "$.detail"
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowSentinelEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sentinel_detector.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.sentinel_security_events.arn
}
