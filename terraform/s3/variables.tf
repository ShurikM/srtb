variable "s3_bucket_name" {
  description = "The name of the S3 bucket for RTB logs"
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev/staging/prod)"
  type        = string
  default     = "dev"
}
