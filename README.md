# Medical Data Migration to MongoDB

This project automates the migration of a cleaned medical dataset (in CSV format) into a MongoDB database. The process ensures data integrity, proper field typing (including date fields), structured logging for auditing, and access control through user roles. The MongoDB environment is secured with predefined roles and users, all initialized at container startup.

## Project Structure

Projet_5/
├── data/
│ ├── healthcare_dataset.csv
│ └── cleaned_healthcare_dataset.csv
├── logs/
│ └── migration.log
├── scripts/
│ ├── migration_script.py
│ └── insert_to_mongodb.py
├── mongodb/
│ └── mongo_init.js
├── .env
├── requirements.txt
└── README.md


## Technologies Used

- Python 3.10+
- Pandas
- PyMongo
- MongoDB
- dotenv
- Docker (next phase)

## MongoDB Schema (Document Model)

Documents are stored in the `patients` collection of the `healthcare_db` database. Each document may look like the following:

```json
{
  "_id": ObjectId,
  "patient_id": "P001",
  "age": 58,
  "gender": "Female",
  "diagnosis": "Hypertension",
  "treatment": "Medication",
  "hospital": "St. Louis",
  "doctor": "Dr. Lambert",
  "date_of_birth": ISODate,
  "admission_date": ISODate,
  "discharge_date": ISODate
}
MongoDB Roles and Users

All roles and users are created via the mongo_init.js script at startup.

Roles
admin_role: full access for administration, inherited from built-in roles
engineer_role: read/write/create/index privileges on healthcare_db
analyst_role: read-only access to healthcare_db
Users
Username	Role	Scope	Permissions
admin_user	admin_role	admin DB	Full administration
engineer_user	engineer_role	healthcare_db	Read, insert, update, delete, index
analyst_user	analyst_role	healthcare_db	Read-only
Environment Variables (.env)

MONGO_URI=mongodb://mongo:27017/

# Admin connection
ADMIN_URI=mongodb://admin_user:admin123@localhost:27017/?authSource=admin

# Engineer connection (used by insert script)
ENGINEER_URI=mongodb://engineer_user:engineer123@localhost:27017/healthcare_db?authSource=healthcare_db

# Analyst connection
ANALYST_URI=mongodb://analyst_user:analyst123@localhost:27017/healthcare_db?authSource=healthcare_db
Note: For production, replace default passwords and move credentials into a secure secret manager.

How to Run the Migration

1. Install dependencies
Create and activate a virtual environment, then run:

pip install -r requirements.txt
2. Prepare the cleaned dataset
Execute the cleaning script to transform the raw CSV into a clean version:

python scripts/migration_script.py
This will generate cleaned_healthcare_dataset.csv in the data/ directory.

3. Run the MongoDB insert script
python scripts/insert_to_mongodb.py
This connects to MongoDB using the engineer account and inserts all cleaned records into the database. Logs are generated in logs/migration.log.

Logging

Logs include:

Data loading confirmation
Cleaning actions and status
Connection to MongoDB
Insert status and document count
Index creation result
They are stored in:

logs/migration.log
Security and Best Practices

Never expose MongoDB publicly without authentication.
Change all default usernames and passwords before production.
Use Docker secrets or a vault service to store sensitive information.
Restrict network access to MongoDB via firewall or security groups.
Regularly back up the database after migration.