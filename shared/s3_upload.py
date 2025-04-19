import boto3
from shared.config import S3_BUCKET

s3 = boto3.client("s3")

def upload_file_to_s3(local_path: str, s3_key: str):
    try:
        s3.upload_file(local_path, S3_BUCKET, s3_key)
        print(f"[S3] Uploaded {local_path} → s3://{S3_BUCKET}/{s3_key}")
        return True
    except Exception as e:
        print(f"[S3 ERROR] {e}")
        return False