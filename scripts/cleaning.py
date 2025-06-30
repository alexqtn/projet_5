# 1. Import necessary libraries
import os                   # For handling file and directory paths
import pandas as pd         # For manipulating tabular data using DataFrames
import logging              # For logging actions and errors to a file

# 2. Dynamically define the base directory (folder where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get absolute path of current script

# 3. Define file paths relative to this script’s location
csv_file_path = os.path.join(BASE_DIR, '..', 'data', 'healthcare_dataset.csv')            # Raw input CSV
log_file_path = os.path.join(BASE_DIR, '..', 'logs', 'migration.log')                     # Log file path
output_file_path = os.path.join(BASE_DIR, '..', 'data', 'cleaned_healthcare_dataset.csv') # Output cleaned CSV

# 4. Set up logging configuration
logging.basicConfig(
    filename=log_file_path,                             # Log output file
    level=logging.INFO,                                 # Log INFO-level and above messages
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format includes timestamp, level, and message
)

# 5. Check if the CSV file exists
if not os.path.exists(csv_file_path):                   # If the file does not exist
    logging.error(f"File not found: {csv_file_path}")   # Log the error
    raise FileNotFoundError(f"File not found: {csv_file_path}")  # Halt script with exception

# 6. Load the CSV file into a DataFrame
try:
    df = pd.read_csv(csv_file_path)                     # Load the raw CSV into a DataFrame
    logging.info(f"Successfully loaded the CSV file: {csv_file_path}")  # Log successful loading
except Exception as e:
    logging.error(f"Error loading CSV file: {e}")       # Log the loading error
    raise                                               # Reraise the error to stop execution

# 7. Log structure and preview of the DataFrame
logging.info(f"DataFrame preview:\n{df.head()}")        # Log first few rows
logging.info(f"DataFrame info:\n{df.info()}")           # Log structure and types
logging.info(f"DataFrame description:\n{df.describe(include='all')}")  # Log column statistics

# 8. Normalize column names
df.columns = (
    df.columns
    .str.strip()                                        # Remove leading/trailing whitespaces
    .str.lower()                                        # Convert column names to lowercase
    .str.replace(' ', '_')                              # Replace spaces with underscores
    .str.replace(r'[^a-z0-9_]', '', regex=True)         # Remove special characters
)
logging.info(f"Normalized column names: {df.columns.tolist()}")  # Log cleaned column names

# 9. Normalize all string values in the DataFrame
for col in df.columns:
    if df[col].dtype == 'object':                      # Only process string/object type columns
        df[col] = (
            df[col]
            .astype(str)                               # Ensure all values are string type
            .str.strip()                               # Remove leading/trailing whitespaces
            .str.strip(',')                            # Remove trailing commas
            .str.replace(r'\s+', '_', regex=True)      # Replace any whitespace with underscores
            .str.lower()                               # Convert all text to lowercase
        )
logging.info("Normalized all string values across the DataFrame.")

# 10. Check and remove missing values
missing_values = df.isnull().sum()                      # Count missing values
if missing_values.any():                                # If any column has missing data
    logging.warning("Missing values found in the DataFrame:")
    logging.warning(f"\n{missing_values[missing_values > 0]}")  # Log columns with missing values
    df = df.dropna()                                    # Drop rows with any NaN values
    logging.info("Rows with missing values removed.")
else:
    logging.info("No missing values found.")

# 11. Check and remove duplicate rows
duplicates = df.duplicated().sum()                      # Count duplicated rows
if duplicates > 0:
    logging.warning(f"Duplicate rows found: {duplicates}")  # Log number of duplicates
    df = df.drop_duplicates()                           # Remove duplicates
    logging.info("Duplicate rows removed.")
else:
    logging.info("No duplicate rows found.")

# 12. Convert date columns to datetime format
for date_col in ['date_of_admission', 'discharge_date']:   # Loop through expected date columns
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')  # Convert to datetime, set invalid to NaT
        logging.info(f"Converted column '{date_col}' to datetime format.")
    else:
        logging.warning(f"Column '{date_col}' not found in DataFrame.")

# 13. Re-check for missing values after date conversion
missing_values_after_conversion = df.isnull().sum()     # Count missing values again
if missing_values_after_conversion.any():
    logging.warning("Missing values after date conversion:")
    logging.warning(f"\n{missing_values_after_conversion[missing_values_after_conversion > 0]}")
else:
    logging.info("No missing values after date conversion.")

# 14. Create a unique patient_key for MongoDB indexing
if all(col in df.columns for col in ['name', 'date_of_admission', 'hospital']):
    df['patient_key'] = (
        df['name'] + "_" +
        df['date_of_admission'].dt.strftime('%Y-%m-%d') + "_" +
        df['hospital']
    ).str.lower().str.replace(r'\s+', '_', regex=True).str.strip(',')
    logging.info("Created 'patient_key' field successfully.")
else:
    logging.warning("Could not create 'patient_key': required columns are missing.")

# 14bis. Remove duplicate patient_key values before exporting
if 'patient_key' in df.columns:
    duplicates = df.duplicated(subset='patient_key').sum()
    if duplicates > 0:
        logging.warning(f"Duplicate patient_key values found: {duplicates}")
        df = df.drop_duplicates(subset='patient_key')
        logging.info("Duplicate patient_key entries removed.")

# 15. Save the cleaned data to CSV
try:
    df.to_csv(output_file_path, index=False)            # Write cleaned DataFrame to file
    logging.info(f"Cleaned DataFrame saved to: {output_file_path}")  # Confirm save
except Exception as e:
    logging.error(f"Failed to save cleaned DataFrame: {e}")  # Log the saving error
    raise                                               # Reraise the error

# 16. Final message to the user
print("Data cleaning completed successfully.")           # Console output for user
logging.info("Data cleaning process completed successfully.")  # Log final success
