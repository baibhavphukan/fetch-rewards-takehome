# Fetch Rewards Data Engineering Take Home: ETL off a SQS Queue

## Overview
This project reads JSON data containing user login behavior from an AWS SQS Queue, masks PII fields, and writes the transformed data to a Postgres database.

## Setup

1. **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd <repo-name>
    ```

2. **Start Docker services:**
    ```sh
    docker-compose up
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the ETL script:**
    ```sh
    python etl.py
    ```

## Details

- **PII Masking:** `device_id` and `ip` fields are hashed using SHA-256 to mask PII while maintaining consistency for duplicate detection.
- **Database Connection:** The application connects to a Postgres database using `psycopg2`.
- **Data Transformation:** The JSON data is flattened and PII fields are masked.

## Assumptions
- The SQS queue and Postgres database are available locally as described in the Docker setup.
- The table `user_logins` is pre-created in the Postgres database.

## Next Steps
- Implement error handling and retries for reading from SQS and writing to Postgres.
- Add logging for better monitoring and debugging.
- Consider using environment variables for configuration.

## Deployment
- This application can be containerized using Docker for consistent deployment across environments.
- For production, consider using AWS services like RDS for Postgres and SQS directly.

## Scaling
- For a growing dataset, use batch processing and potentially partition the Postgres table for performance.
- Consider using AWS Lambda for automatic scaling with SQS triggers.

## PII Recovery
- Store original PII data in a secure, encrypted data store if recovery is necessary. Access should be strictly controlled.

