#!/bin/bash
exec > /var/log/user_data.log 2>&1
set -xe

# Ensure script has correct permissions and line endings
chmod +x /var/lib/cloud/instance/scripts/* || true

# Install Python 3.11 and other tools
apt update -y
apt install -y python3.11 python3.11-venv python3.11-dev git curl build-essential dos2unix

# Make Python 3.11 the default
update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Install Poetry for ubuntu user
su - ubuntu -c "curl -sSL https://install.python-poetry.org | python3.11"

# Setup PATH for Poetry
su - ubuntu -c "
  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.bashrc
  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.profile
"

# Setup SSH key
mkdir -p /home/ubuntu/.ssh
cp /tmp/github_deploy /home/ubuntu/.ssh/id_ed25519
chmod 600 /home/ubuntu/.ssh/id_ed25519
chown ubuntu:ubuntu /home/ubuntu/.ssh/id_ed25519

cat <<EOF > /home/ubuntu/.ssh/config
Host github.com
    StrictHostKeyChecking no
    IdentityFile ~/.ssh/id_ed25519
EOF
chown ubuntu:ubuntu /home/ubuntu/.ssh/config

# Clone and install the app
su - ubuntu -c "
  export PATH=\$HOME/.local/bin:\$PATH
  cd ~
  git clone git@github.com:ShurikM/srtb.git
  cd srtb/openrtb_server
  ~/.local/bin/poetry install --no-root
"

# Create systemd service
cat <<EOF > /etc/systemd/system/openrtb-server.service
[Unit]
Description=OpenRTB Server Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/srtb/openrtb_server
EnvironmentFile=/home/ubuntu/srtb/.env
ExecStart=/home/ubuntu/.local/bin/poetry run env PYTHONPATH=/home/ubuntu/srtb uvicorn app.main:app --host 0.0.0.0 --port 8080

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
chmod 644 /etc/systemd/system/openrtb-server.service
systemctl daemon-reload
systemctl enable openrtb-server.service
systemctl start openrtb-server.service
