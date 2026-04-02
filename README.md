# Global Tech News Data Pipeline 🚀
A custom ETL pipeline built with Python and Apache Airflow that automates news aggregation and cloud storage.

## Overview
This project extracts the latest technology stories from the Hacker News API, transforms the data into a clean format using Pandas, and uploads the results to an AWS S3 bucket in the Stockholm region (`eu-north-1`).

---

## 🛠 Project Components
While this project uses the Astronomer framework, the core logic resides in these custom files:

* **`include/extract_tech_news.py`**: Python script that fetches the top 20 story IDs and details from Hacker News.
* **`include/transform_tech_news.py`**: Cleans the data, handles missing values, and uses `boto3` to securely upload the final CSV to AWS S3.
* **`dags/global_tech_news_pipeline.py`**: The Airflow DAG that orchestrates these tasks on a schedule.
* **`.env`**: (Local only) Stores AWS Credentials and region settings safely.

---

## How to Run Locally

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli) installed.

### 2. Setup
Clone this repository and ensure your `.env` file is configured with your AWS keys:
```text
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=eu-north-1
