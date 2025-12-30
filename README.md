# Globant Data Engineer Technical Challenge

Technical Proof of Concept (PoC) developed as part of the **Globant Data Engineer selection process**.  
The objective of this project is to design and implement a **scalable, cloud-based data ingestion, validation, backup, and analytics platform**, following best practices in data engineering and software architecture.

---

## Challenge Overview

### Challenge #1 – Data Ingestion & Management

As a data engineer at Globant, the goal is to migrate historical and incoming data to a new SQL-based data platform, meeting the following requirements:

1. **Historical data ingestion**
   - Load historical data from CSV files into a SQL database.

2. **REST API for new data ingestion**
   - Validate each transaction against a defined data dictionary.
   - Support batch inserts (1 to 1000 rows per request).
   - Use a single API service to receive data for multiple tables.
   - Apply table-specific validation rules.

3. **Backup functionality**
   - Generate backups per table.
   - Store backups in **AVRO format** in the file system.

4. **Restore functionality**
   - Restore a specific table from its corresponding backup.

**Additional constraints**
- Invalid transactions must **not** be inserted and must be **logged**.
- All fields are required.
- CSV files are comma-separated.
- SQL database is mandatory (technology choice is open).

---

### Challenge #2 – Data Exploration & Analytics

Expose analytical endpoints to explore the ingested data and provide metrics required by stakeholders.  
Each metric must be exposed through a **dedicated REST endpoint**, optimized for analytical queries.

---

## Architecture

The solution is implemented entirely on **Google Cloud Platform (GCP)**, leveraging managed services to ensure scalability, reliability, and production readiness.

### Cloud Services Used

- **Google Cloud Storage (GCS)**
  - Storage of raw CSV files
  - Storage of processed files
  - Storage of AVRO backups

- **Cloud SQL (PostgreSQL)**
  - OLTP database for validated transactional data

- **BigQuery**
  - OLAP analytical layer
  - Optimized for stakeholder queries and reporting

- **Looker Studio**
  - Visualization and dashboarding for business metrics

---

## Architecture Diagram

![Project Architecture](architecture.png)

---

## Database Architecture

The project follows a **dual-database design pattern**:

- **OLTP layer**
  - Normalized schema
  - Optimized for data ingestion and consistency
  - Used by FastAPI services

- **OLAP layer**
  - Star schema
  - Optimized for analytical queries
  - Powered by BigQuery

This separation ensures **high ingestion performance** while enabling **efficient analytics**.

---

## Project Structure
challenge_globant/
├── app/ # FastAPI backend
│ ├── api/
│ ├── models/
│ ├── schemas/
│ ├── services/
│ └── main.py
│
├── jobs/ # Data pipeline (batch processing)
│ ├── ingestion/
│ ├── processing/
│ ├── persistence/
│ └── utils/
│
├── docker/
│ ├── Dockerfile
│ └── entrypoint.sh
│
├── architecture.png
├── .env
├── README.md
└── requirements.txt

---

## Data Pipeline (Batch Processing)

The **pipeline job** is responsible for:

- Reading CSV files from **Cloud Storage**
- Applying data validation and transformation rules
- Loading valid data into **Cloud SQL**
- Generating **AVRO backups** per table
- Moving processed and backup files to their corresponding GCS locations

---

## Containerization Strategy (Docker)

A **single Docker container** is used to run:

- **FastAPI REST service**
- **Scheduled batch pipeline (cron job)**

### Justification

- Simplifies deployment and environment consistency
- Ensures the API and batch jobs share:
  - The same dependencies
  - The same configuration
  - The same runtime environment
- Suitable for PoC and controlled workloads
- Easily portable to Cloud Run, GKE, or Compute Engine

---

## Security Considerations

Although no user authentication table is implemented, the API includes basic security mechanisms:

- API access protection using **custom headers (e.g., `X-TOKEN`)**
- Centralized validation layer
- Strict schema enforcement
- Logging of invalid transactions
- Environment-based configuration using `.env` variables

These measures provide a foundation that can be extended with OAuth2, IAM, or API Gateway.

---

## How to Run Locally (Without Docker)

1. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

for run Fast API
```bash
uvicorn app.main:app --reload
```
for manualy run pipeline
```bash
py .\jobs\main.py 
```
or
```bash
python .\jobs\main.py 
```

## How to Run with Docker
1. Build the image
```bash
docker build -t globant-challenge -f docker/Dockerfile .
```

2. Run the container
```bash
docker build -t globant-challenge -f docker/Dockerfile .
```
This will start:
- The FastAPI service
- The scheduled pipeline job

## API Features Summary

- Batch CSV ingestion
- REST API batch insert (1–1000 rows)
- Data validation and logging
- AVRO backup and restore
- Analytical endpoints for business metrics

## Development Workflow
- Git-based versioning with frequent commits
- Modular and extensible architecture
- Cloud-first design
- Clear separation of concerns (API, pipeline, analytics)

## Technologies Used
- Python
- FastAPI
- PostgreSQL
- Google Cloud Storage
- BigQuery
- Looker Studio
- Docker

##Author
Humberto Franco Osorio
Data Engineer