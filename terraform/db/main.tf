terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

# VPC
resource "aws_vpc" "db_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "srtb-vpc"
  }
}

# Subnet 1 - AZ a
resource "aws_subnet" "db_subnet_1" {
  vpc_id                  = aws_vpc.db_vpc.id
  cidr_block              = "10.0.1.0/24"   # <-- inside 10.0.0.0/16
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = false
  tags = {
    Name = "srtb-subnet-1"
  }
}

# Subnet 2 - AZ b
resource "aws_subnet" "db_subnet_2" {
  vpc_id                  = aws_vpc.db_vpc.id
  cidr_block              = "10.0.2.0/24"   # <-- inside 10.0.0.0/16
  availability_zone       = "eu-central-1b"
  map_public_ip_on_launch = false
  tags = {
    Name = "srtb-subnet-2"
  }
}

# Security Group for RDS
resource "aws_security_group" "db_sg" {
  name        = "srtb-db-sg"
  description = "Allow access to RDS only from specific sources"
  vpc_id      = aws_vpc.db_vpc.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Allow from inside the VPC only
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "srtb-db-sg"
  }
}

# DB Subnet Group (for RDS)
resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "srtb-db-subnet-group"
  subnet_ids = [
    aws_subnet.db_subnet_1.id,
    aws_subnet.db_subnet_2.id
  ]

  tags = {
    Name = "SRTB DB Subnet Group"
  }
}

# RDS PostgreSQL Database (Private)
resource "aws_db_instance" "postgresql" {
  identifier               = "srtb-postgres-db"
  allocated_storage        = 20
  max_allocated_storage    = 100
  engine                   = "postgres"
  engine_version           = "15.10"
  instance_class           = "db.t3.micro"  # Free Tier
  db_name                  = "srtb"
  username                 = "srtb_admin"
  password                 = var.db_password
  db_subnet_group_name     = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids   = [aws_security_group.db_sg.id]
  publicly_accessible      = false  # ❗ Important: Private
  skip_final_snapshot      = true

  tags = {
    Name = "SRTB PostgreSQL DB"
  }
}


# Variables
variable "db_password" {
  description = "Password for the PostgreSQL master user"
  type        = string
  sensitive   = true
}

# Outputs
output "rds_endpoint" {
  value = aws_db_instance.postgresql.endpoint
}

output "rds_port" {
  value = aws_db_instance.postgresql.port
}

output "rds_username" {
  value = aws_db_instance.postgresql.username
}

output "rds_database_name" {
  value = aws_db_instance.postgresql.db_name
}
