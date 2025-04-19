provider "aws" {
  region = var.region
}

resource "aws_key_pair" "deployer" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

resource "aws_security_group" "openrtb_sg" {
  name        = "openrtb-sg"
  description = "Allow SSH and HTTP for RTB"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip] # Restrict SSH to your IP
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "openrtb_server" {
  ami                         = var.ami_id
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.deployer.key_name
  vpc_security_group_ids      = [aws_security_group.openrtb_sg.id]

  tags = {
    Name = "openrtb-server"
  }

  user_data = file("${path.module}/user_data.sh")

  provisioner "file" {
    source      = "${path.module}/github_deploy"
    destination = "/tmp/github_deploy"

    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("${path.module}/github_deploy")
      host        = self.public_ip
    }
  }

  iam_instance_profile = aws_iam_instance_profile.rtb_instance_profile.name

  # Optional: Wait for SSH to be ready before next steps
  provisioner "remote-exec" {
    inline = ["echo EC2 is ready."]
    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("${path.module}/github_deploy")
      host        = self.public_ip
    }
  }
}

resource "aws_iam_role" "rtb_ec2_role" {
  name = "rtb-ec2-s3-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "rtb_s3_policy" {
  name = "S3LogAccess"
  role = aws_iam_role.rtb_ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.s3_bucket_name}",
          "arn:aws:s3:::${var.s3_bucket_name}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_instance_profile" "rtb_instance_profile" {
  name = "rtb-instance-profile"
  role = aws_iam_role.rtb_ec2_role.name
}


