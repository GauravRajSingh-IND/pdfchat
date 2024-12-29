import boto3
from dotenv import load_dotenv
load_dotenv()

class PineconeDB:

    def __init__(self, file_path):
        self.pdf_path=file_path
        self.bucket=boto3.resource(service_name="s3", region_name="us-east-1")
        self.bucket_name="webapp-pdfchat"
        self.object_name="GauravRajSingh.pdf"

    def upload_pdf_s3(self):

        # Initialize s3 bucket object.
        s3_bucket=self.bucket.Bucket(self.bucket_name)

        try:
            self.bucket.Bucket(self.bucket_name).upload_file(self.pdf_path, self.object_name)
            print(f"File '{self.pdf_path}' uploaded successfully to '{self.bucket_name}/{self.object_name}'")

        except Exception as e:
            print(f"Error uploading file: {e}")
