#!/bin/bash

# Enable logging
exec > /var/log/user_data.log 2>&1
set -xe

# Update + install basics
yum update -y
yum install -y git python3

# Install Poetry (as ec2-user)
su - ec2-user -c "
  curl -sSL https://install.python-poetry.org | python3 -
  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc
"

# Clone the repo and run the server
su - ec2-user -c "
  cd ~
  git clone https://github.com/srtb360/srtb.git
  cd srtb
  export PATH=\"\$HOME/.local/bin:\$PATH\"
  poetry install
  PYTHONPATH=src nohup poetry run uvicorn openrtb_server.main:app --host 0.0.0.0 --port 8080 > server.log 2>&1 &
"
