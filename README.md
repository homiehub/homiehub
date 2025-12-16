<p align="center">
  <img src="logo.png" alt="HomieHub Logo" height="150"/>
<h1 align="center" style="font-size: 30px; margin-bottom: -10px;">
  HomieHub <span style="font-size: 25px; font-weight: 500;">: AI-Powered Roommate Matching Platform</span>
</h1>
</p>
<p align="center">
  <a href="https://www.youtube.com/@TheSamzi">
    <img src="https://img.shields.io/badge/YouTube-e52d27?style=for-the-badge&logo=youtube&logoColor=white" 
         alt="YouTube" 
         style="height:24px;">
  </a>
  <a href="https://homiehub-23.vercel.app/">
    <img src="https://img.shields.io/badge/Website-0078D7?style=for-the-badge&logo=internet-explorer&logoColor=white" 
         alt="Website"
         style="height:24px;">
  </a>
</p>

## Overview
HomieHub is a cloud-native, MLOps-driven platform for university roommate matching. It aggregates listings from WhatsApp, social media, Kaggle datasets, and synthetic data via a conversational bot and web interface.

The data pipeline ingests, preprocesses, validates, and stores data, while the model pipeline performs semantic embedding, LLM-based scoring, and top-K roommate recommendations. The platform is Dockerized, monitored, CI/CD-ready, and privacy-first.

---
## System Design Architecture

![HomieHub System Architecture](homiehub_sysdesign.jpg)

The system follows a **5-lane microservices architecture** hosted on **GCP**:

1. **Data Pipeline (ETL)** – ingestion, cleaning, validation, storage
2. **Model Building** – LLM agent, recommendation engine, feature store
3. **Model Evaluation** – QA, metrics, fairness checks, drift detection
4. **CI/CD & Deployment** – automated builds, containerization, deployment
5. **Monitoring & Logging** – observability, email alerts, system health

> For detailed system documentation, see [system_design.md](system_design.md)
---

# Table of Contents

1. [Overview](#overview)
2. [System Design Architecture](#system-design-architecture)
3. [Project Structure](#project-structure)
4. [Features](#features)
   * [Data Pipeline](#data-pipeline)
   * [Model Pipeline](#model-pipeline)
   * [Web Platform](#web-platform)
5. [Documentation](#documentation)
6. [Quick Start](#quick-start)
   * [Prerequisites](#prerequisites)
   * [Installation](#installation)
7. [Contributing](#contributing)
8. [Acknowledgments](#acknowledgments)
9. [Contact & Collaboration](#contact--collaboration)
10. [License](#license)

---

## Project Structure
````
homiehub/
├── LICENSE
├── README.md
├── requirements.txt
├── homiehub.html
├── homiehub_sysdesign.jpg
├── system_design.md
├── data-pipeline/
│   ├── ETL_SCRIPT.sh
│   ├── airflow_setup.sh
│   ├── GCP_Account_Key.json
│   ├── assets/                  # Diagrams & flowcharts
│   ├── dags/
│   │   └── homiehub_data_pipeline.py
│   ├── data/
│   │   ├── processed/
│   │   └── raw/
│   ├── docs/                     # Documentation
│   │   ├── setup_guide.md        # [Setup Guide]
│   │   └── scripts_usage.md      # [Scripts Usage Guide]
│   ├── logs/                     # ETL execution logs
│   ├── pipelines/
│   │   └── etl.py
│   ├── requirement.txt
│   ├── src/                      # Source code modules
│   │   ├── extraction/
│   │   ├── ingestion/
│   │   ├── load/
│   │   ├── preprocessing/
│   │   └── utils/
│   ├── test/
│   └── working_data/
├── model-pipeline/
│   ├── assets/
│   ├── experiments/              # MLflow experiments & logs
│   ├── llm-agent/                # LLM scoring microservice
│   ├── recommendation-service/   # Recommendation API
│   ├── user-room-service/        # User & room service
│   └── readme.md
└── gcloud/
````
## Features

### [Data Pipeline](data-pipeline/readme.md)
- **Multi-Source Aggregation**: WhatsApp, Facebook Marketplace, Kaggle datasets, synthetic data
- **Automated ETL**: Apache Airflow orchestration with Docker containerization
- **Preprocessing & Bias Detection**: Transformation, schema validation, fairness checks
- **NLP Processing**: spaCy-based extraction from unstructured text
- **Data Quality**: Schema validation, DVC versioning
* **Cloud Native**: GCS & Firestore storage, DVC versioning
* **Monitoring**: Email notifications, logs, drift detection

### [Model Pipeline](model-pipeline/readme.md)

The `model-pipeline/` module handles AI-driven roommate matching using semantic search, embeddings, and preference-aware ranking. This pipeline is designed to be fully MLOps-compliant, supporting modular model updates, batch and real-time inference, and scalable deployment.

**Model Pipeline Capabilities**
1. Semantic Embedding Models
- Sentence Transformer–based vectorization
- Room & user representation learning
- Cosine similarity + hybrid BM25 reranking
2. LLM Agent for Context-Aware Scoring
- Evaluates roommate compatibility using LLM-based reasoning
- Tools-enabled evaluation (budget alignment, commute, noise tolerance, habits)
- Supports OpenAI API + local LLM deployments
3. Recommendation Engine
- Top-K candidate retrieval using vector search
- LLM reranker for personalized scoring
- Real-time recommendation function via Cloud Functions
4. MLOps Features
- Dockerized microservices for all three components
- GitHub Actions-based CI/CD 
- Configurable deployment targets: Cloud Run / GKE
- Monitoring & metrics hooks (Prometheus-ready)

### Web Platform 
- .edu authentication via Auth0
- Verified student listings
- Real-time matching interface
- Privacy-first design

## Documentation

| Module             | Description                                        | Link                                                                         |
| ------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Data Pipeline**  | Complete ETL & data processing pipeline guide      | [data-pipeline/README.md](./data-pipeline/README.md)                         |
| **Setup Guide**    | Installation, environment setup, and configuration | [data-pipeline/docs/setup_guide.md](./data-pipeline/docs/setup_guide.md)     |
| **Scripts Usage**  | Guide for running automation scripts               | [data-pipeline/docs/scripts_usage.md](./data-pipeline/docs/scripts_usage.md) |
| **Model Pipeline** | AI & recommendation system documentation           | [model-pipeline/readme.md](./model-pipeline/readme.md)                       |
| **System Design**  | Full system architecture & lane-level details      | [system_design.md](system_design.md)                                         |

## Quick Start

### Prerequisites
- **Python 3.11** (required for Apache Airflow 3.1.1)
- Docker & Docker Compose (20.10+ / 2.0+)
- Google Cloud Platform account
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/homiehub/homiehub.git
   cd homiehub
   ```

2. **Python Environment**

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Data Pipeline Setup**

```bash
cd data-pipeline
chmod +x airflow_setup.sh
./airflow_setup.sh
cp /path/to/service-account.json GCP_Account_Key.json
echo "GCP_PROJECT_ID=your-project-id" >> .env
echo "GCP_BUCKET_NAME=homiehub-data-bucket" >> .env
docker-compose up airflow-init
docker-compose up -d
```

* Airflow UI: [http://localhost:8080](http://localhost:8080)
* Username: `airflow2`, Password: `airflow2`
* Enable DAG: `homiehub_data_pipeline`

4. **Model Pipeline Setup**

```bash
cd model-pipeline/experiments
mlflow ui
docker-compose -f llm-agent/docker-compose.yml up -d
docker-compose -f recommendation-service/docker-compose.yml up -d
docker-compose -f user-room-service/docker-compose.yml up -d
```

## Contributing

1. Fork & create a branch:

```bash
git checkout -b feature/YourFeature
```

2. Run tests:

```bash
cd data-pipeline && python -m pytest test/
cd model-pipeline/experiments && pytest test/
```

3. Commit & push:

```bash
git commit -m "Add YourFeature"
git push origin feature/YourFeature
```

* Follow **PEP 8**, write tests, update docs, and ensure all tests pass.
---

## Acknowledgments

Apache Airflow, Google Cloud Platform, MLflow, DVC, EvidentlyAI, MLOps course mentors, Open-source community

## Contact

For inquiries, collaboration, or contributions:

* Submit an [issue](https://github.com/homiehub/homiehub/issues) on GitHub
* Connect with the maintainers via the [Documentation](#documentation) resources for guidance on script usage, data pipelines, model pipelines, and system design


## License

Licensed under the [MIT License](./LICENSE).