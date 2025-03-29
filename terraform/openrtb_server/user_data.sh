#!/bin/bash
exec > /var/log/user_data.log 2>&1
set -xe

# Update and install system packages
yum update -y
yum install -y git python3

# Install poetry for ec2-user
su - ec2-user -c "
  curl -sSL https://install.python-poetry.org | python3 -
  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.bashrc
  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.profile
"

# Set up SSH key
mkdir -p /home/ec2-user/.ssh
cp /tmp/github_deploy /home/ec2-user/.ssh/id_ed25519
chmod 600 /home/ec2-user/.ssh/id_ed25519
chown ec2-user:ec2-user /home/ec2-user/.ssh/id_ed25519

cat <<EOF > /home/ec2-user/.ssh/config
Host github.com
    StrictHostKeyChecking no
    IdentityFile ~/.ssh/id_ed25519
EOF

chown ec2-user:ec2-user /home/ec2-user/.ssh/config

# Clone repo and launch app
su - ec2-user -c "
  export PATH=\$HOME/.local/bin:\$PATH
  cd ~
  git clone git@github.com:ShurikM/srtb.git
  cd srtb/openrtb-server
  poetry install
  PYTHONPATH=src nohup poetry run uvicorn openrtb_server.main:app --host 0.0.0.0 --port 8080 > ~/server.log 2>&1 &
"
