# Healthcare Data Migration to MongoDB

This project aims to clean, transform, and migrate a structured healthcare dataset from CSV format into a MongoDB database. It simulates a production-grade data pipeline using Docker for orchestration, role-based access control for data security, and a modular Python-based architecture for data processing.

---

## Objectives

- Clean and normalize healthcare data from a CSV file.
- Load the cleaned data into MongoDB.
- Set up user roles with custom privileges (admin, engineer, analyst).
- Orchestrate the entire setup using Docker and Docker Compose.
- Ensure security and reproducibility of the pipeline.
- Provide clear, modular code and thorough documentation.

---

## Project Architecture

PROJET_5/
│
├── .env # Environment variables for MongoDB URIs (excluded from Git)
├── .gitignore # Git exclusions
├── docker-compose.yml # Docker orchestration
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── p5_fiche_evaluation.pdf # Evaluation guidelines
│
├── data/ # Raw and cleaned data files
│ ├── healthcare_dataset.csv
│ └── cleaned_healthcare_dataset.csv
│
├── docker/ # Docker image and wait script
│ ├── Dockerfile
│ └── wait-for-mongo.sh
│
├── logs/ # Log files for tracking migration
│ └── migration.log
│
├── mongodb/ # MongoDB initialization and configuration
│ ├── mongo_init.js
│ └── mongod.conf
│
└── scripts/ # Python scripts for data processing
├── cleaning.py
├── data_processing.ipynb
├── migration.py
└── test_connection.py


---

## Component Breakdown

### 1. Data Cleaning (`scripts/cleaning.py`)
- Loads the raw CSV (`data/healthcare_dataset.csv`).
- Cleans column names, removes nulls, and normalizes data.
- Exports the cleaned dataset as `data/cleaned_healthcare_dataset.csv`.

### 2. MongoDB Setup
- a. Role-based Access Control (RBAC)
MongoDB is configured with three distinct roles, created automatically at container startup using mongo_init.js:
Role	Purpose	Permissions
admin	Full control	readWriteAnyDatabase, dbAdminAnyDatabase, userAdminAnyDatabase
engineer	Data ingestion + modification	readWrite on healthcare_db
analyst	Read-only access	read on healthcare_db

- b. Initialization script
Located in: mongodb/mongo_init.js
It creates:
The roles
Users with passwords
Assigns them to the healthcare_db database

- c. Configuration
mongod.conf: configures network access, disables telemetry, allows external connections
.env: stores all connection URIs (ADMIN_URI, ENGINEER_URI, ANALYST_URI) securely

### 3. Docker and Orchestration
- `docker/Dockerfile`: Python runtime with MongoDB client tools.
- `docker/wait-for-mongo.sh`: Ensures MongoDB is live before migration.
- `docker-compose.yml`: Defines MongoDB container, script volumes, and startup order.

### 4. Migration Script (`scripts/migration.py`)
- Connects to MongoDB via the `ENGINEER_URI` from `.env`.
- Loads cleaned data and inserts it into the `patients` collection.
- Logs the process and results into `logs/migration.log`.

### 5. Connection Test (`scripts/test_connection.py`)
- Tests connectivity and credentials for each user role.
- Verifies MongoDB availability and database accessibility.

### 6. Notebook (`scripts/data_processing.ipynb`)
- Interactive version of the cleaning and migration pipeline.
- Useful for step-by-step demonstrations or debugging.

---

## How to Run the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alexqtn/projet_5.git
   cd projet_5
Create your .env file (not tracked by Git):
MONGO_URI=mongodb://mongo:27017/

ADMIN_URI=mongodb://admin_user:admin123@mongo:27017/?authSource=admin
ENGINEER_URI=mongodb://engineer_user:engineer123@mongo:27017/healthcare_db?authSource=healthcare_db
ANALYST_URI=mongodb://analyst_user:analyst123@mongo:27017/healthcare_db?authSource=healthcare_db
Launch the services:
docker-compose up --build
(Optional) Run the migration manually:
docker exec -it mongo_migration_container python scripts/migration.py
MongoDB Roles

Role Name	Privileges	Database
admin_role	Full access: user, db, cluster admin	admin
engineer_role	Read/Write, create indexes/collections	healthcare_db
analyst_role	Read-only, view data and metadata	healthcare_db
Evaluation Criteria

This project satisfies the requirements outlined in p5_fiche_evaluation.pdf, including:

Functional Docker orchestration
Secure and scalable MongoDB setup
Structured Python scripts for ETL
Clean and reproducible data pipeline
Proper use of version control and documentation


Terminal – Commandes pour exécuter le projet
# GIT – Initialisation et gestion du dépôt
git init                                 # Initialise un dépôt Git local
git remote add origin <URL>              # Lie un dépôt distant (à faire une fois)
git remote -v                            # Vérifie les URL du dépôt distant
git add .                                # Ajoute tous les fichiers au commit
git commit -m "Initial commit"           # Valide les changements avec un message
git push -u origin main                  # Envoie le projet vers la branche principale de GitHub

# DOCKER – Gestion des conteneurs
docker-compose up --build                # Construit et lance les conteneurs (MongoDB + scripts)
docker-compose down                      # Arrête et supprime les conteneurs (volumes conservés)
docker ps                                # Liste les conteneurs Docker en cours d'exécution
docker exec -it mongo bash               # Accède à un terminal bash dans le conteneur MongoDB
docker exec -it mongo mongosh            # Accède à la shell MongoDB sans authentification (si ouverte)
docker exec -it mongo mongosh -u admin_user -p admin123 --authenticationDatabase admin     # Connexion MongoDB avec identifiants
docker logs <container_id>               # Affiche les logs d'un conteneur spécifique

# MONGODB – Opérations courantes
show dbs                                 # Affiche les bases disponibles (auth requis)
use healthcare_db                        # Bascule vers la base souhaitée
show collections                         # Affiche les collections de la base courante
db.patients.find().pretty()              # Affiche les documents de la collection patients de manière lisible
db.patients.countDocuments()             # Compte les documents dans la collection
db.patients.createIndex({ _id: 1 }, { unique: true })   # Ajoute une contrainte d’unicité sur l'identifiant
exit                                     # Quitte la shell MongoDB

# SCRIPTS PYTHON – Migration et tests
docker exec -it mongo_migration_container python scripts/migration.py          # Lance manuellement la migration des données
docker exec -it mongo_migration_container python scripts/test_connection.py    # Teste la connexion MongoDB depuis le script

# AUTRES – Vérifications
cat logs/migration.log                    # Affiche les logs de la migration
cat .env                                  # Vérifie les URI et identifiants définis