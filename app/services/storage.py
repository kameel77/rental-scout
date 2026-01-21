import os
from typing import BinaryIO

import boto3

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET", "vehicle-images")
S3_REGION = os.getenv("S3_REGION", "us-east-1")


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION,
    )


def upload_file(file_obj: BinaryIO, key: str) -> str:
    client = get_s3_client()
    client.upload_fileobj(file_obj, S3_BUCKET, key)
    if S3_ENDPOINT:
        return f"{S3_ENDPOINT}/{S3_BUCKET}/{key}"
    return f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
