#!/bin/bash

# ETL Pipeline Runner Script
# Run this from the Project directory to execute the ETL pipeline

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR"

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}✗ Error: homiehub directory not found at $PROJECT_DIR${NC}"
    exit 1
fi

# Check if venv exists
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo -e "${RED}✗ Error: Virtual environment not found at $PROJECT_DIR/venv${NC}"
    echo "Please create a virtual environment first:"
    echo "  cd $PROJECT_DIR"
    echo "  python3 -m venv venv"
    exit 1
fi

# Check if GCP key exists
GCP_KEY="$SCRIPT_DIR/GCP_Account_Key.json"
if [ ! -f "$GCP_KEY" ]; then
    echo -e "${YELLOW}⚠ Warning: GCP key not found at $GCP_KEY${NC}"
    echo "Make sure your GCP credentials are properly configured."
fi

# Activate virtual environment and run ETL
cd "$PROJECT_DIR"

# Activate venv
source venv/bin/activate


# Run ETL pipeline
python -m pipelines.etl

# Check exit status
if [ $? -eq 0 ]; then
    echo "----------------------------------------------------------------------"
    echo -e "${GREEN}✓ ETL pipeline completed successfully!${NC}"
    echo "======================================================================"
    exit 0
else
    echo "----------------------------------------------------------------------"
    echo -e "${RED}✗ ETL pipeline failed!${NC}"
    echo "======================================================================"
    exit 1
fi