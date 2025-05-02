variable "region" {
  default = "eu-central-1"
}

variable "key_name" {
  default = "openrtb-key"
}

variable "public_key_path" {
  default = "./github_deploy.pub"
}

data "http" "my_ip" {
  url = "https://checkip.amazonaws.com"   # returns your IP + newline
}

locals {
  ssh_cidr = "${chomp(data.http.my_ip.response_body)}/32"
}

variable "ami_id" {
  description = "Ubuntu 22.04 LTS (Jammy Jellyfish) for eu-central-1"
  default     = "ami-01179af425b2ee025"
}


variable "s3_bucket_name" {
  description = "Name of the S3 bucket for logs"
  type        = string
}