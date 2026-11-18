data "aws_iam_policy_document" "lambda_findings_write" {
  statement {
    sid    = "WriteSecurityFindings"
    effect = "Allow"

    actions = [
      "s3:PutObject"
    ]

    resources = [
      "${aws_s3_bucket.evidence.arn}/findings/*"
    ]
  }
}

resource "aws_iam_role_policy" "lambda_findings_write" {
  name   = "sentinel-ci-lambda-findings-write"
  role   = aws_iam_role.sentinel_lambda.id
  policy = data.aws_iam_policy_document.lambda_findings_write.json
}
