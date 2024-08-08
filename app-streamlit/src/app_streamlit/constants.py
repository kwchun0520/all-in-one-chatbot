from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError
import json

load_dotenv()

DRY = bool(int(os.environ["DRY"]))
REGION = os.environ["REGION"]
SECRET_NAME = os.environ["AWS_TELEGRAM_SECRET_NAME"]
SECRET_TOKEN_KEY= os.environ["AWS_TELEGRAM_SECRET_TELEGRAM_TOKEN_KEY"]
SECRET_CHAT_ID_KEY= os.environ["AWS_TELEGRAM_SECRET_CHAT_ID_KEY"]


def get_secret():
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=REGION
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=SECRET_NAME
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    return get_secret_value_response["SecretString"]

if DRY:
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]
else:
    secret = json.loads(get_secret())
    TELEGRAM_TOKEN = secret[SECRET_TOKEN_KEY]
    CHAT_ID = secret[SECRET_CHAT_ID_KEY]
