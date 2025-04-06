## connecting to AWS:
1. aws sso login --profile AdministratorAccess-043309322226
2. export AWS_PROFILE=AdministratorAccess-043309322226

## Get AMI IDs
aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=al2023-ami-2023*-kernel-6.1-x86_64" \
            "Name=architecture,Values=x86_64" \
            "Name=virtualization-type,Values=hvm" \
            "Name=state,Values=available" \
  --region eu-central-1 \
  --query 'Images[*].[ImageId,CreationDate]' \
  --output text | sort -k2 | tail -n 1

## prepare the ec2
1. SSH into the instance: ssh ec2-user@63.176.177.0 -i ~/.ssh/id_rsa
2. Install core packages:
   sudo yum update -y
   sudo yum install -y git python3
3. install poetry:
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
4. Clone your GitHub repo:
git clone https://github.com/srtb360/srtb.git
cd YOUR_REPO

   



