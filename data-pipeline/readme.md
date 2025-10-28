# HomieHub Data Pipeline

## Overview

The **HomieHub Data Pipeline** is an end-to-end ETL pipeline for processing housing listing data.
It performs data acquisition, cleaning, transformation, feature engineering, and storage of processed datasets.
The pipeline is orchestrated using **Apache Airflow**, includes **logging, alerts, and summary emails**, and tracks data versions via **DVC**.

---

## Key Features

* Modular ETL code: `extraction`, `ingestion`, `preprocessing`, and `utils`
* Reproducible workflow using **Docker** and **Airflow**
* Logging and alert system for monitoring pipeline execution
* Data versioning using **DVC**
* SMTP email notifications for ETL summary and logs
* Supports anomaly detection and schema validation in preprocessing

---

## Folder Structure

```text
.
├── __init__.py
├── assets/
│   ├── 1_grant_chart.png
│   └── 2_homiehub_data_pipeline-graph.png
├── config/
├── dags/
│   ├── __init__.py
│   ├── airflow_etl.py       # old (deprecated)
│   └── homiehub_data_pipeline.py
├── data/
│   ├── features/
│   ├── processed/
│   └── raw/
├── docker-compose.yaml       # DO NOT PUSH TO GIT (use locally)
├── docs/
├── logs/
├── plugins/
├── readme.md
├── requirements.txt
├── setup.sh
├── src/
│   ├── __init__.py
│   ├── extraction/
│   │   ├── __init__.py
│   │   └── whatsapp_data_extraction.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── data_handlers/
│   │       ├── __init__.py
│   │       └── csv_extractor.py
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── transform.py
│   └── utils/
│       ├── __init__.py
│       └── io.py
├── test/
│   └── __init__.py
└── working_data/
    └── __init__.py
```

---

## Instructions

1. **Run the setup script** to install dependencies and prepare the environment:

```bash
bash setup.sh
```

2. **Follow the printed next steps**:

```bash
echo "Next steps:"
echo "1. Export your housing list CSV into the raw data folder: data/raw/"
echo "2. Initialize Airflow (one-time setup): docker-compose up airflow-init"
echo "3. Start Airflow services: docker-compose up -d"
echo "4. Open Airflow UI: http://localhost:8080"
```

3. **Make sure the raw CSV file** is in the correct folder:

```bash
cp <your_housing_list_data.csv> data/raw/
```

4. **Trigger the DAG**:

   * Open the Airflow UI at [http://localhost:8080](http://localhost:8080)
   * Navigate to the **`homiehub_data_pipeline`** DAG
   * Turn it **ON** and **Trigger DAG** manually (or wait for scheduled runs if configured)

5. **Check pipeline progress**:

   * Logs are saved under `logs/`
   * Summary emails and log emails are sent to the configured SMTP email (`samhita.kolluri@gmail.com`)

6. **DVC data versioning**:

   * Pull tracked datasets:

```bash
dvc pull
```

---

## DAG Overview

#### DAG Gantt Chart
![HomieHub Gantt Chart](assets/1_grant_chart.png)

**homiehub_data_pipeline DAG** consists of the following steps:

1. **Load Raw Listings** – reads raw CSV into a temporary file
2. **Transform Listings** – data cleaning, preprocessing, and feature engineering
3. **Save Processed Listings** – outputs cleaned CSV to `data/processed/`
4. **Finalize ETL** – prints ETL completion in logs
5. **Push Summary** – generates ETL summary for XCom and notifications
6. **Send Summary Email** – sends success/failure summary via SMTP
7. **Send Logs Email** – emails logs for the current DAG run

#### DAG Graph
![HomieHub DAG](assets/2_homiehub_data_pipeline-graph.png)
---

## SMTP Email Configuration

Airflow `smtp_default` connection in Airflow UI. Go to admin, connections and add `smtp_default` connection. Don’t use your Gmail login password you need an App Password.

| Field       | Value                                                                             |
| ----------- | --------------------------------------------------------------------------------- |
| Conn Id     | smtp_default                                                                      |
| Conn Type   | SMTP                                                                              |
| Host        | smtp.gmail.com                                                                    |
| Port        | 587                                                                               |
| Login       | (`your_email@gmail.com`) |
| Password    | `your_app_password`                                                     |
| Timeout     | 30                                                                                |
| Retry Limit | 5                                                                                 |
| TLS         | false                                                                             |
| SSL         | true                                                                              |
| Auth Type   | basic                                                                             |


---

## Pipeline Flow 
![Flowchart](assets/0_flowchart_datapipeline.png)
---

## Testing

* Unit tests are included in the `test/` directory
* Focused on data preprocessing and transformation
* Run tests with:

```bash
pytest test/
```

---

## Reproducibility

* All dependencies are specified in `requirements.txt`
* Pipeline runs inside Docker containers
* Data is versioned using **DVC** and tracked in Git
* Clear setup and run instructions ensure reproducibility across machines

---

## Logging & Alerts

* Airflow logs all task outputs in `logs/`
* If anomalies or errors occur, **emails are sent automatically** to `your-mail-id@gmail.com`
* Log email includes all task logs for the DAG run
* Retry limits and timeouts are set in the DAG (`default_args`) for robustness


