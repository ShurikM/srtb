# Run Terraform

This Terraform configuration will create:

1. An Aurora DB cluster with a `campaigns` table.
2. Insert a single test record with `active` set to `false` in the `campaigns` table.

```bash
cd ~/dev/projects/srtb && \
source .env && \
export TF_VAR_aurora_db_password=$AURORA_DB_PASSWORD && \
cd terraform/db && \
terraform apply
```

# Connect to AuroraDB

See connection details in `.vscode/settings.json`.