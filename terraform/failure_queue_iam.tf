data "aws_iam_policy_document" "lambda_failure_queue_send" {
  statement {
    sid    = "SendFailedInvocationsToSQS"
    effect = "Allow"

    actions = [
      "sqs:SendMessage"
    ]

    resources = [
      aws_sqs_queue.failed_events.arn
    ]
  }
}

resource "aws_iam_role_policy" "lambda_failure_queue_send" {
  name   = "sentinel-ci-lambda-failure-queue-send"
  role   = aws_iam_role.sentinel_lambda.id
  policy = data.aws_iam_policy_document.lambda_failure_queue_send.json
}
