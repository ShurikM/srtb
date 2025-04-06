# main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

# provider "aws" {
#   region = "us-east-1"  # Change to your preferred region
# }
provider "aws" {
  region = "eu-central-1"  # Frankfurt
}

# VPC and Security Group configuration for the database
resource "aws_vpc" "db_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  
  tags = {
    Name = "srtb-vpc"
  }
}

# Aurora requires at least 2 subnets in different AZs
resource "aws_subnet" "db_subnet_1" {
  vpc_id            = aws_vpc.db_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-central-1a"
  map_public_ip_on_launch = true
  
  tags = {
    Name = "srtb-subnet-1"
  }
}

resource "aws_subnet" "db_subnet_2" {
  vpc_id            = aws_vpc.db_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-central-1b"
  map_public_ip_on_launch = true
  
  tags = {
    Name = "srtb-subnet-2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.db_vpc.id
  
  tags = {
    Name = "srtb-igw"
  }
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.db_vpc.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  
  tags = {
    Name = "srtb-route-table"
  }
}

resource "aws_route_table_association" "rta_1" {
  subnet_id      = aws_subnet.db_subnet_1.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_route_table_association" "rta_2" {
  subnet_id      = aws_subnet.db_subnet_2.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_security_group" "db_sg" {
  name        = "srtb-db-sg"
  description = "Security group for SRTB Aurora PostgreSQL"
  vpc_id      = aws_vpc.db_vpc.id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # For production, restrict this to your application's CIDR
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

resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "srtb-db-subnet-group"
  subnet_ids = [aws_subnet.db_subnet_1.id, aws_subnet.db_subnet_2.id]
  
  tags = {
    Name = "SRTB DB Subnet Group"
  }
}

# Minimal Aurora PostgreSQL cluster
resource "aws_rds_cluster" "aurora_cluster" {
  cluster_identifier      = "srtb-aurora-cluster"
  engine                  = "aurora-postgresql"
  engine_version          = "16.6"
  database_name           = "srtb"
  master_username         = "srtb_admin"
  master_password         = var.aurora_db_password
  skip_final_snapshot     = true
  db_subnet_group_name    = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids  = [aws_security_group.db_sg.id]
  
  # Minimal settings for POC - absolute minimum capacity
  serverlessv2_scaling_configuration {
    min_capacity = 0.5  # Lowest possible value for Aurora PostgreSQL
    max_capacity = 1.0
  }
  
  # Enable Data API for AWS Query Editor access
  enable_http_endpoint = true
  
  tags = {
    Name = "SRTB Aurora Cluster"
  }
}

# Single Aurora instance
resource "aws_rds_cluster_instance" "aurora_instance" {
  identifier           = "srtb-aurora-instance"
  cluster_identifier   = aws_rds_cluster.aurora_cluster.id
  instance_class       = "db.serverless"  # Serverless v2 for minimal cost
  engine               = "aurora-postgresql"
  engine_version       = "16.6"
  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name
  publicly_accessible  = true
  
  tags = {
    Name = "SRTB Aurora Instance"
  }
}

# Null resource to execute the SQL script
resource "null_resource" "db_setup" {
  depends_on = [
    aws_rds_cluster_instance.aurora_instance
  ]

  # Wait for the database to be fully available
  provisioner "local-exec" {
    command = "sleep 60"  # Give Aurora time to fully initialize
    interpreter = ["bash", "-c"]
  }

  # Execute the SQL script using psql - Git Bash friendly format
  provisioner "local-exec" {
    command = "export PGPASSWORD='${var.aurora_db_password}' && psql -h ${aws_rds_cluster.aurora_cluster.endpoint} -p ${aws_rds_cluster.aurora_cluster.port} -U ${aws_rds_cluster.aurora_cluster.master_username} -d ${aws_rds_cluster.aurora_cluster.database_name} -f ${path.module}/setup.sql"
    interpreter = ["bash", "-c"]
  }
}

# Define variables
variable "aurora_db_password" {
  description = "Password for the Aurora PostgreSQL master user"
  type        = string
  sensitive   = true
}

# Output the cluster endpoint for connection
output "aurora_cluster_endpoint" {
  value = aws_rds_cluster.aurora_cluster.endpoint
}

output "aurora_port" {
  value = aws_rds_cluster.aurora_cluster.port
}

output "aurora_username" {
  value = aws_rds_cluster.aurora_cluster.master_username
}

output "aurora_database" {
  value = aws_rds_cluster.aurora_cluster.database_name
}