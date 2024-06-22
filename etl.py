import hashlib
import json
import boto3
import psycopg2
from psycopg2 import sql

# Configuration for SQS and PostgreSQL
SQS_QUEUE_URL = "http://localhost:4566/000000000000/login-queue"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Function to mask PII data using SHA-256 hashing
def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Function to transform a message, masking PII and setting default values
def transform_message(message):
    data = json.loads(message)
    transformed_data = {
        'user_id': data.get('user_id', ''),
        'device_type': data.get('device_type', ''),
        'masked_ip': mask_pii(data.get('ip', '')),
        'masked_device_id': mask_pii(data.get('device_id', '')),
        'locale': data.get('locale', ''),
        'app_version': data.get('app_version', ''),
        'create_date': data.get('create_date', '1970-01-01')  # Default date if create_date is missing
    }
    return transformed_data

# Function to create the user_logins table if it does not already exist
def create_table_if_not_exists(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_logins(
        user_id             varchar(128),
        device_type         varchar(32),
        masked_ip           varchar(256),
        masked_device_id    varchar(256),
        locale              varchar(32),
        app_version         varchar(32),
        create_date         date
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

# Function to read messages from the SQS queue
def read_from_queue():
    sqs = boto3.client('sqs', endpoint_url="http://localhost:4566", region_name="us-east-1")
    response = sqs.receive_message(QueueUrl=SQS_QUEUE_URL, MaxNumberOfMessages=10)
    return response.get('Messages', [])

# Function to write transformed records to the PostgreSQL database
def write_to_postgres(records):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    create_table_if_not_exists(conn)
    
    cursor = conn.cursor()
    insert_query = sql.SQL(
        "INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    for record in records:
        cursor.execute(insert_query, (
            record['user_id'],
            record['device_type'],
            record['masked_ip'],
            record['masked_device_id'],
            record['locale'],
            record['app_version'],
            record['create_date']
        ))
    conn.commit()
    cursor.close()
    conn.close()

# Main function to orchestrate reading from SQS, transforming, and writing to PostgreSQL
def main():
    messages = read_from_queue()
    if messages:
        records = [transform_message(msg['Body']) for msg in messages]
        write_to_postgres(records)

# Entry point of the script
if __name__ == "__main__":
    main()
