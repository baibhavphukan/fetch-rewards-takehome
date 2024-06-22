# Fetch Rewards Data Engineering Take Home: ETL off a SQS Queue

# Fetch Rewards ETL Project

This project demonstrates an ETL (Extract, Transform, Load) process that reads JSON data from an AWS SQS Queue, masks PII (Personally Identifiable Information) data, and writes the transformed data into a PostgreSQL database. Docker is used to run all components locally.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.7+
- Git
- Postgres

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


## Questions

### How would you deploy this application in production?

- **Deployment Strategy:** Deploy using a managed Kubernetes service such as Amazon EKS, Google Kubernetes Engine for container orchestration and scalability.
- **Database:** Utilize managed PostgreSQL services such as Amazon RDS or Google Cloud SQL for reliability, scalability, and automated backups.
- **CI/CD:** Implement CI/CD pipelines (e.g. GitLab CI/CD, GitHub Actions) for automated testing, building Docker images, and deployment to production.
- **Security:** Secure sensitive data using environment variables or secrets management tools. Implement encryption for data at rest and in transit.

### What other components would you want to add to make this production ready?

- **Logging and Monitoring:** Implement logging using something, for instance, ELK stack and monitoring (e.g Prometheus, Grafana) for application health and performance.
- **Error Handling:** Enhance error handling and retry mechanisms to handle network issues, database failures, and data processing errors gracefully.
- **Performance Optimization:** Optimize database queries and indexing. Consider caching strategies (e.g Redis) for improved performance.
- **Security:** Implement role-based access control (RBAC) for database and application access. Ensure compliance with data protection regulations such as GDPR, HIPAA etc.
- **Backup and Recovery:** Set up automated backups for databases and implement disaster recovery plans to ensure data integrity and availability.

### How can this application scale with a growing dataset?

- **Scaling Strategy:** Scale horizontally by adding more Docker containers using Kubernetes or Docker Swarm to handle increased message throughput.
- **Database Scaling:** Implement partitioning strategies in PostgreSQL to distribute data across multiple nodes and improve query performance.
- **Cloud Services:** Utilize cloud-native services like Amazon SQS for message queuing and Amazon RDS for scalable PostgreSQL deployments.
- **Performance Monitoring:** Monitor system metrics like CPU, memory usage etc. and scale resources dynamically based on workload demands.

### How can PII be recovered later on?

- **PII Recovery Strategy:** Store original PII data securely in an encrypted data store. Maintain a mapping mechanism linking masked values in the database to original PII data for recovery purposes.
- **Access Controls:** Implement strict access controls and auditing mechanisms to track access to sensitive data and ensure compliance with data privacy regulations.

### What are the assumptions you made?

- The JSON messages from the SQS queue have consistent fields (`user_id`, `device_type`, `ip`, `device_id`, `locale`, `app_version`, `create_date`).
- Docker and Docker Compose are used for local development and testing.
- The PostgreSQL database schema (`user_logins`) and necessary tables are pre-created as described in the Docker setup.
- The application will run on a local development environment with Docker and required dependencies installed. Although the python script handles in case there is no table created initially


---




