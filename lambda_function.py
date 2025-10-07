import boto3
import tempfile
import os
from PIL import Image

# Initialize S3 client
s3_client = boto3.client('s3')

# Set your bucket names
SOURCE_BUCKET = "source-image-bucket"
DESTINATION_BUCKET = "processed-image-bucket"

def lambda_handler(event, context):
    """
    AWS Lambda handler to:
    - Download image from source bucket
    - Resize it
    - Upload processed image to destination bucket
    """

    # Get the uploaded file name from the event
    source_key = event['Records'][0]['s3']['object']['key']

    # Create temporary files for processing
    with tempfile.TemporaryDirectory() as tmpdir:
        download_path = os.path.join(tmpdir, os.path.basename(source_key))
        upload_path = os.path.join(tmpdir, f"processed-{os.path.basename(source_key)}")

        # Download the original image from the source bucket
        s3_client.download_file(SOURCE_BUCKET, source_key, download_path)
        print(f"Downloaded {source_key} from {SOURCE_BUCKET}")

        # Open and process the image (example: resize to 300x300)
        with Image.open(download_path) as img:
