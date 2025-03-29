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
