
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "sentinel_lambda" {
  name               = "sentinel-ci-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_cloudwatch_log_group" "sentinel_lambda" {
  name              = "/aws/lambda/sentinel-ci-detector"
  retention_in_days = 7
}

data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "${aws_cloudwatch_log_group.sentinel_lambda.arn}:*"
    ]
  }
}

resource "aws_iam_role_policy" "lambda_logging" {
  name   = "sentinel-ci-lambda-logging"
  role   = aws_iam_role.sentinel_lambda.id
  policy = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_lambda_function" "sentinel_detector" {
  function_name = "sentinel-ci-detector"

  filename         = "${path.module}/../build/sentinel-ci-lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../build/sentinel-ci-lambda.zip")

  role    = aws_iam_role.sentinel_lambda.arn
  handler = "src.lambda_handler.lambda_handler"
  runtime = "python3.14"

  timeout     = 10
  memory_size = 128

  depends_on = [
    aws_iam_role_policy.lambda_logging,
    aws_cloudwatch_log_group.sentinel_lambda
  ]
}
