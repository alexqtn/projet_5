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

# 4. Define a function to connect to MongoDB
def connect_to_mongodb(uri_env_key='ADMIN_URI', db_name='healthcare_db', collection_name='patients', timeout_ms=5000):
    mongo_uri = os.getenv(uri_env_key)                                                # Get URI from environment
    if not mongo_uri:                                                                 # Check if URI exists
        logging.error(f"Environment variable '{uri_env_key}' not found.")             # Log error
        raise EnvironmentError(f"Missing environment variable: {uri_env_key}")        # Raise error if missing
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=timeout_ms)         # Create client with timeout
        client.admin.command('ping')                                                  # Ping to test connection
        logging.info(f"Connected to MongoDB using {uri_env_key}.")                    # Log success
        db = client[db_name]                                                          # Get database
        collection = db[collection_name]                                              # Get collection
        logging.info(f"Using collection '{collection_name}' in DB '{db_name}'.")      # Log details
        return collection                                                             # Return collection object
    except errors.ConnectionFailure as e:                                             # Handle connection error
        logging.error(f"MongoDB connection failed: {e}")                              # Log failure
        raise                                                                          # Raise to stop script

# 5. Get MongoDB collection via function
collection = connect_to_mongodb()  # Uses defaults: ADMIN_URI, healthcare_db, patients

# 6. Load the cleaned CSV file into a DataFrame
try:
    data_file_path = os.path.join(BASE_DIR, '..', 'data', 'cleaned_healthcare_dataset.csv')  # Path to cleaned data
    df = pd.read_csv(data_file_path)                                                         # Load CSV
    logging.info(f"Successfully loaded the cleaned CSV file: {data_file_path}")              # Log success
except FileNotFoundError:
    logging.error(f"File not found: {data_file_path}")                                       # Log error
    raise                                                                                     # Raise if file missing

# 7. Convert date columns to datetime format
date_columns = ['date_of_admission', 'discharge_date']                # Define date columns
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')               # Convert to datetime or NaT

# 8. Transform the DataFrame to a list of dictionaries
records = df.to_dict(orient='records')                                # Convert DataFrame to list of dicts

# 9. Ensure MongoDB understands the date format
for doc in records:
    for col in date_columns:
        if col in doc and isinstance(doc[col], pd.Timestamp):         # Check type
            doc[col] = doc[col].to_pydatetime()                       # Convert to Python datetime

# 9bis. Create unique index on patient_key
try:
    collection.create_index('patient_key', unique=True)              # Create unique index
    logging.info("Created unique index on 'patient_key' field.")     # Log success
except errors.OperationFailure as e:
    logging.error(f"Failed to create unique index: {e}")             # Log failure

# 10. Insert records into MongoDB
try:
    result = collection.insert_many(records)                          # Bulk insert
    logging.info(f'Inserted {len(result.inserted_ids)} records into MongoDB.')  # Log insert count
except errors.BulkWriteError as e:
    logging.error(f"Bulk write error: {e.details}")                   # Log detailed error

# 11. Final verification
count = collection.count_documents({})                                # Count all docs
print(f"Total records in MongoDB collection: {count}")                # Print result
logging.info(f"Total records in MongoDB collection: {count}")         # Log result

# 12. Keep script running to prevent Docker container exit
try:
    while True:
        pass  # Infinite loop to hold process
except KeyboardInterrupt:
    logging.info("Migration script terminated by user.")              # Log interrupt
    print("Migration script terminated by user.")                     # Console message
