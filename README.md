Healthcare Data Migration to MongoDB

This project aims to clean, transform, and migrate a structured healthcare dataset from CSV format to a MongoDB database. It is designed to simulate a production-grade data pipeline using Docker for orchestration, role-based access control for data security, and a modular Python-based architecture for data handling.

Objectives

Clean and normalize healthcare data from a CSV file
Load the cleaned data into MongoDB
Set up user roles with custom privileges (admin, engineer, analyst)
Orchestrate the entire setup using Docker and Docker Compose
Ensure security and reproducibility of the pipeline
Provide clear modular code and documentation for maintainability
Project Architecture

PROJET_5/
│
├── .env                          # Environment variables for MongoDB
├── .gitignore                   # Git exclusions
├── docker-compose.yml           # Docker orchestration
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── p5_fiche_evaluation.pdf      # Evaluation guidelines
│
├── data/                        # Data folder
│   ├── healthcare_dataset.csv
│   └── cleaned_healthcare_dataset.csv
│
├── docker/                      # Docker-related scripts
│   ├── Dockerfile
│   └── wait-for-mongo.sh
│
├── logs/                        # Migration logs
│   └── migration.log
│
├── mongodb/                     # MongoDB init & config
│   ├── mongo_init.js
│   └── mongod.conf
│
└── scripts/                     # Python and notebook scripts
    ├── cleaning.py
    ├── data_processing.ipynb
    ├── migration.py
    └── test_connection.py
Components Description

1. Data Cleaning (scripts/cleaning.py)
Reads raw CSV from data/healthcare_dataset.csv
Cleans column names, removes nulls, normalizes fields
Outputs cleaned data to data/cleaned_healthcare_dataset.csv
2. MongoDB Setup
mongodb/mongo_init.js: Defines custom roles and creates users
mongodb/mongod.conf: Configures MongoDB (e.g., bind IP, security)
.env: Stores URIs for different users and access levels
3. Docker and Orchestration
docker/Dockerfile: Builds a Python environment with MongoDB client
docker/wait-for-mongo.sh: Ensures MongoDB is up before migration
docker-compose.yml: Launches MongoDB container, volumes, and networks
4. Migration Script (scripts/migration.py)
Connects to MongoDB using credentials from .env
Loads cleaned data and inserts it into the collection
Logs the result into logs/migration.log
5. Validation (scripts/test_connection.py)
Tests whether MongoDB is reachable using the correct role
Prints success/failure for connection and query
6. Notebook (scripts/data_processing.ipynb)
Provides a visual and iterative version of the pipeline
Useful for debugging or presenting intermediate steps
Running the Project

Clone the repository:
git clone https://github.com/alexqtn/projet_5.git
cd projet_5
Create .env file (already included):
MONGO_URI=mongodb://mongo:27017/

ADMIN_URI=mongodb://admin_user:admin123@mongo:27017/?authSource=admin
ENGINEER_URI=mongodb://engineer_user:engineer123@mongo:27017/healthcare_db?authSource=healthcare_db
ANALYST_URI=mongodb://analyst_user:analyst123@mongo:27017/healthcare_db?authSource=healthcare_db
Launch the services:
docker-compose up --build
Run the migration manually (if not in auto-mode):
docker exec -it mongo_migration_container python scripts/migration.py
MongoDB Roles

Role Name	Privileges	Database
admin_role	Admin/cluster/db/user management	admin
engineer_role	Read/write, collection/index create	healthcare_db
analyst_role	Read-only, view structure	healthcare_db
Evaluation Criteria

This project follows the expectations outlined in p5_fiche_evaluation.pdf, including:

Docker orchestration
MongoDB user security
Modular, clean, and reproducible code
Structured data pipeline and transformation
Version control and documentation
Future Improvements

Implement data validation and schema constraints before insertion
Add unit tests for each transformation step
CI/CD integration for deployment and testing
Visualization dashboards for data analysis
