# 1. Import required libraries
import os                                # For file path manipulation
import pandas as pd                      # For handling tabular data
from pymongo import MongoClient, errors  # For connecting and interacting with MongoDB
from dotenv import load_dotenv           # For loading environment variables from a .env file
import logging                           # For logging actions and errors
from datetime import datetime            # For handling date and time formats

# 2. Load .env variables
load_dotenv()  # This loads environment variables (e.g., MONGO_URI) into the system environment

# 3. Set up logging
BASE_DIR = os.path.dirname(os.path.abspath(__file__))                      # Current directory of the script
log_file_path = os.path.join(BASE_DIR, '..', 'logs', 'migration.log')     # Path to the log file
logging.basicConfig(                                                      # Logging configuration
    filename=log_file_path,                                               # Log output file
    level=logging.INFO,                                                   # Set log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'                    # Log format
)

# 4. Define path to cleaned CSV file
data_file_path = os.path.join(BASE_DIR, '..', 'data', 'cleaned_healthcare_dataset.csv')  # Path to the cleaned CSV

# 5. Connect to MongoDB
try:
    mongo_uri = os.getenv('ADMIN_URI')       # Get the MongoDB URI from environment or fallback
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)         # Connect with a timeout
    client.admin.command('ping')                                           # Simple ping to ensure Mongo is reachable
    db = client['healthcare_db']                                           # Access the database
    collection = db['patients']                                            # Access (or create) the collection
    logging.info("Connected to MongoDB successfully.")                     # Log connection success
except errors.ConnectionFailure as e:
    logging.error(f"Failed to connect to MongoDB: {e}")                    # Log failure
    raise                                                                  # Raise the error to stop the script

# 6. Load the cleaned CSV file into a DataFrame
try:
    df = pd.read_csv(data_file_path)                                       # Load the cleaned CSV
    logging.info(f"Successfully loaded the cleaned CSV file: {data_file_path}")  # Log success
except FileNotFoundError as e:
    logging.error(f"File not found: {data_file_path}")                     # Log if the file is missing
    raise

# 7. Convert date columns to datetime format
date_columns = ['date_of_admission', 'discharge_date']      # List of date fields to convert
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')                     # Convert each date column, invalids become NaT

# 8. Transform the DataFrame to a list of dictionaries
records = df.to_dict(orient='records')                                     # Convert DataFrame to list of JSON-style dictionaries

# 9. Ensure MongoDB understands the date format
for doc in records:
    for col in date_columns:
        if col in doc and isinstance(doc[col], pd.Timestamp):              # Check if value is a pandas datetime
            doc[col] = doc[col].to_pydatetime()                            # Convert pandas datetime to Python datetime

# 9bis. Créer un index unique sur le champ patient_key pour éviter les doublons
try:
    collection.create_index('patient_key', unique=True)
    logging.info("Created unique index on 'patient_key' field.")
except errors.OperationFailure as e:
    logging.error(f"Failed to create unique index: {e}")
    raise

# 10. Insert records into MongoDB
try:
    result = collection.insert_many(records)                               # Bulk insert all records
    logging.info(f'Inserted {len(result.inserted_ids)} records into MongoDB.')  # Log the number of inserted records
except errors.BulkWriteError as e:
    logging.error(f"Bulk write error: {e.details}")                        # Log any insertion error
    raise

# 11. Final verification
count = collection.count_documents({})                                    # Count documents in the collection
print(f"Total records in MongoDB collection: {count}")                    # Show confirmation to the user
logging.info(f"Total records in MongoDB collection: {count}")             # Log the total count
