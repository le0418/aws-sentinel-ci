
output "evidence_bucket_name" {
  description = "S3 bucket for simulated forensic evidence"
  value       = aws_s3_bucket.evidence.id
}


output "sentinel_lambda_name" {
  description = "Name of the Sentinel-CI detection Lambda function"
  value       = aws_lambda_function.sentinel_detector.function_name
}
