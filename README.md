# Create DB

```bash
cd ~/dev/projects/srtb && \
source .env && \
export TF_VAR_aurora_db_password=$AURORA_DB_PASSWORD && \
cd terraform/db && \
terraform apply
```