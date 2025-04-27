#!/bin/bash
exec > /var/log/user_data.log 2>&1
set -xe

# Update and install system packages
yum update -y
yum install -y git python3

# Install Poetry
su - ec2-user -c "
  curl -sSL https://install.python-poetry.org | python3 -
  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.bashrc
  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.profile
"

# Setup SSH for GitHub access
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

# Clone repository
su - ec2-user -c "
  export PATH=\$HOME/.local/bin:\$PATH
  cd ~
  git clone git@github.com:ShurikM/srtb.git
  cd srtb/rtb_admin_api
  poetry install
"

# Create systemd service
cat <<EOF > /etc/systemd/system/rtb-admin-api.service
[Unit]
Description=RTB Admin API Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/srtb/rtb_admin_api
EnvironmentFile=/home/ec2-user/srtb/rtb_admin_api/.env
ExecStart=/home/ec2-user/.local/bin/poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Set permissions and reload systemd
chmod 644 /etc/systemd/system/rtb-admin-api.service
systemctl daemon-reload
systemctl enable rtb-admin-api.service
systemctl start rtb-admin-api.service
