# data-pipeline/setup.sh
#!/bin/bash
set -e

echo "🏠 HomieHub Data Pipeline Setup"
echo "================================"

# Remove existing .env file if it exists
rm -f .env
rm -rf ./logs ./plugins ./config

# Stop and remove containers, networks, and volumes
docker compose down -v

# Create required Airflow directories
mkdir -p ./logs ./plugins ./config

# Write the current user's UID into .env
echo "AIRFLOW_UID=$(id -u)" > .env

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. export housing list data.csv in data/raw/"
echo "2. Run: docker-compose up airflow-init"
echo "3. Run: docker-compose up -d"
echo "4. Open http://localhost:8080 "