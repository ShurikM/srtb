#!/bin/bash
exec > /var/log/user_data.log 2>&1
set -xe

# Fix script line endings and permissions
chmod +x /var/lib/cloud/instance/scripts/* || true

# Update system and install essential packages
apt update -y
apt install -y python3.11 python3.11-venv python3.11-dev git curl build-essential dos2unix

# Set Python 3.11 as default
update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Install Poetry for ubuntu user
su - ubuntu -c "curl -sSL https://install.python-poetry.org | python3.11"

# Configure Poetry PATH for ubuntu user
su - ubuntu -c "
  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.bashrc
  echo 'export PATH=\$HOME/.local/bin:\$PATH' >> ~/.profile
"

# Install Node.js for React build
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Set up SSH access for private repo
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

# Clone repo, write .env.dev, build React UI, install Python backend
su - ubuntu -c "
  export PATH=\$HOME/.local/bin:\$PATH
  cd ~
  git clone git@github.com:ShurikM/srtb.git

  # Write environment file for FastAPI
  cat <<EOV > ~/srtb/.env
DB_PASSWORD=hdj47%Jd
DATABASE_URL=postgresql+psycopg2://srtb_admin:hdj47%Jd@srtb-postgres-db.cbemw6ioywh2.eu-central-1.rds.amazonaws.com:5432/srtb
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_BUCKET=srtb-log-bucket
S3_REGION=eu-central-1
IS_FAKE_DB=True
EOV

  # Build React frontend
  cd ~/srtb/web_ui
  npm install
  npm run build 2>&1 | tee ~/web_ui_build.log

  # Install Python dependencies
  cd ~/srtb/rtb_admin_api
  poetry install --no-root
"

# Create and register systemd service unit
cat <<EOF > /etc/systemd/system/rtb-admin-api.service
[Unit]
Description=RTB Admin API Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/srtb/rtb_admin_api
EnvironmentFile=/home/ubuntu/srtb/.env
Environment=PYTHONPATH=/home/ubuntu/srtb
# invoke Uvicorn via the venv's Python to guarantee it's on PATH
ExecStart=/home/ubuntu/.local/bin/poetry run python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable & start
chmod 644 /etc/systemd/system/rtb-admin-api.service
systemctl daemon-reload
systemctl enable rtb-admin-api.service
systemctl start rtb-admin-api.service
