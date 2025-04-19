resource "aws_s3_bucket" "rtb_logs" {
  bucket = var.s3_bucket_name

  tags = {
    Name        = "RTB Logs"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_public_access_block" "rtb_logs_block" {
  bucket = aws_s3_bucket.rtb_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "rtb_logs_versioning" {
  bucket = aws_s3_bucket.rtb_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}
