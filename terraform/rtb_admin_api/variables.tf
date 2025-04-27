variable "region" {
  default = "eu-central-1"
}

variable "key_name" {
  default = "openrtb-key"
}

variable "public_key_path" {
  default = "./github_deploy.pub"
}

variable "my_ip" {
  default = "147.235.206.11/32"
}

variable "ami_id" {
  description = "Amazon Linux 2023 AMI for eu-central-1"
  default     = "ami-0b74f796d330ab49c"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for logs"
  type        = string
}