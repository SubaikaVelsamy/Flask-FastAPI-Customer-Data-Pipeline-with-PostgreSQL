Flask + FastAPI Customer Data Pipeline with PostgreSQL

A Dockerized project demonstrating a complete data pipeline for customer data.

Flask Mock Server serves paginated customer data from a JSON file.

FastAPI Pipeline Service ingests data into PostgreSQL with upsert logic and pagination.

PostgreSQL is the backend database.

Fully containerized using Docker Compose for easy setup and testing.

Handles error cases (404 for missing customers) and uses environment variables for credentials.

Project Structure
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── database.py
    ├── Dockerfile
    └── requirements.txt

Prerequisites
Docker Desktop installed
Optional: PostgreSQL if testing outside Docker

Setup & Run
cd path/to/mock_test
docker-compose up --build

API Endpoints
1. Ingest data into PostgreSQL
   curl -X POST "http://localhost:8000/api/ingest"
     {"status": "success", "records_processed": 22}
2. Get paginated customers
   curl "http://localhost:8000/api/customers?page=1&limit=10"
3. Get single customer by ID
   curl "http://localhost:8000/api/customers/1"

Notes
Docker networking: Use service names for container-to-container calls (mock-server:5000).
Database connection: DATABASE_URL=postgresql://postgres:password@postgres:5432/customer_db
Pagination supported for Flask and FastAPI endpoints.
404 handling implemented for missing customers.

Stop Services
docker-compose down
