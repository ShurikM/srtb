variable "region" {
  default = "eu-central-1"
}

variable "key_name" {
  default = "openrtb-key"
}

variable "public_key_path" {
  default = "/Users/shurikm/.ssh/id_rsa.pub"
}

variable "my_ip" {
  default = "147.235.206.11/32"
}

variable "ami_id" {
  description = "Amazon Linux 2023 AMI"
  default     = "ami-0c101f26f147fa7fd" # us-east-1
}
