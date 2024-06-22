# Fetch Rewards Data Engineering Take Home: ETL off a SQS Queue

# Fetch Rewards ETL Project

This project demonstrates an ETL (Extract, Transform, Load) process that reads JSON data from an AWS SQS Queue, masks PII (Personally Identifiable Information) data, and writes the transformed data into a PostgreSQL database. Docker is used to run all components locally.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.7+
- Git

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/baibhavphukan/fetch-rewards-takehome.git
    cd fetch-rewards-takehome
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
   - Ensure Docker containers are running.
   - Open a new terminal or command prompt.
     
    ```sh
    python etl.py
    ```
    - The script will read messages from the SQS queue, transform them by masking PII, and then write the transformed data 
      to the PostgreSQL database.
      
## Verifying Data in PostgreSQL

1. **Connect to the PostgreSQL database:**
   ```sh
    psql -d postgres -U postgres -p 5432 -h localhost -W
    ```
2. **Run the following SQL query to view inserted data:**
   ```sh
   SELECT * FROM user_logins;
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

