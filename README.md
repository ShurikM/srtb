# Run Terraform

## Precondition

1. You are logged into AWS CLI with your account.
2. You have `psql` installed.

## Terraform to Create Aurora DB

This Terraform configuration will create:

1. An Aurora DB cluster with a `campaigns` table.
2. Insert a single test record with `active` set to `false` in the `campaigns` table.

To apply the Terraform configuration, run the following command:

```bash
cd ~/dev/projects/srtb && \
source .env && \
export TF_VAR_aurora_db_password=$AURORA_DB_PASSWORD && \
cd terraform/db && \
terraform apply
```

## Connect to AuroraDB

See connection details in `.vscode/settings.json`.