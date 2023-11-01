import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import glob
from tqdm import tqdm

load_dotenv()

PARQUET_FILES_PATH = "../data/parquet_files/*.parquet"


def get_csv_files(path):
    return glob.glob(path)


def get_file_name_from_file_path(file_path):
    return file_path.split(".")[1]


client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET"),
)


def upload_file(client, file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = client
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False

csv_files = get_csv_files(PARQUET_FILES_PATH)
for file in tqdm(csv_files, desc="Processing CSV files"):
    upload_file(
        client,
        file,
        bucket="samsung-health-data",
        #object_name=get_file_name_from_file_path(file),
    )
