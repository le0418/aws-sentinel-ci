
output "evidence_bucket_name" {
  description = "S3 bucket for simulated forensic evidence"
  value       = aws_s3_bucket.evidence.id
}
