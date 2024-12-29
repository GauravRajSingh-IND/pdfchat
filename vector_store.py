import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from dotenv import load_dotenv
import os

class S3Uploader:
    def __init__(self, region_name="us-east-1"):
        """
        Initialize S3 uploader with AWS credentials from environment variables.

        Args:
            region_name (str): AWS region name (default: us-east-1)
        """
        load_dotenv()

        # Initialize S3 client instead of resource for better error handling
        self.s3_client = boto3.client(
            service_name="s3",
            region_name=region_name
        )

    def upload_file(self, file_path, bucket_name, object_name=None):
        """
        Upload a file to an S3 bucket.

        Args:
            file_path (str): Path to file to upload
            bucket_name (str): Bucket to upload to
            object_name (str): S3 object name. If not specified, file_path's basename is used

        Returns:
            bool: True if file was uploaded, else False
        """
        # Convert to Path object for better path handling
        file_path = Path(file_path)

        # If S3 object_name not specified, use file's basename
        if object_name is None:
            object_name = file_path.name

        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            self.s3_client.upload_file(
                str(file_path),
                bucket_name,
                object_name
            )
            print(f"Successfully uploaded '{file_path}' to 's3://{bucket_name}/{object_name}'")
            return True

        except ClientError as e:
            print(f"Failed to upload '{file_path}' to S3: {e}")
            return False

        except Exception as e:
            print(f"Unexpected error uploading to S3: {e}")
            return False

    def check_bucket_exists(self, bucket_name):
        """
        Check if a bucket exists and we have access to it.

        Args:
            bucket_name (str): Name of the bucket to check

        Returns:
            bool: True if bucket exists and accessible, False otherwise
        """
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            return False