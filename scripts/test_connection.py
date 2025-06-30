# === Step 1: Import necessary libraries ===

from pymongo import MongoClient         # Enables connection to MongoDB
from dotenv import load_dotenv          # Loads environment variables from .env file
import os                               # Access to environment variables

load_dotenv()  # Load environment variables from the .env file

# === Step 2: Connect to MongoDB using authenticated user ===

mongo_uri = os.getenv('ADMIN_URI_LOCAL')      # Get the MongoDB URI from .env (admin user)
print(f"URI utilisée : {mongo_uri}")    # Print the MongoDB URI for debugging  
client = MongoClient(mongo_uri)         # Connect to MongoDB using the URI

# === Step 3: Access database and collection ===

db = client['healthcare_db']            # Access the 'healthcare_db' database
collection = db['test_collection']      # Access a test collection

# === Step 4: Insert a test document ===

test_doc = {"connection": "successful"}                 # Create a document to insert
inserted_id = collection.insert_one(test_doc).inserted_id  # Insert document and get its ID
print("Inserted document ID:", inserted_id)             # Print the inserted document ID

# === Step 5: Read the inserted document ===

document = collection.find_one({"connection": "successful"})  # Find the inserted document
print("Document found:", document)                            # Print the document

# === Step 6: Update the document ===

collection.update_one(                           # Update a document
    {"_id": document["_id"]},                    # Match by ID # type: ignore
    {"$set": {"status": "checked"}}              # Set a new field 'status'
)
print("Document updated with new field: status = 'checked'")  # Confirmation message

# === Step 7: Read after update ===

updated = collection.find_one({"_id": document["_id"]})  # Re-read the updated document
print("Updated document:", updated)                      # Print updated document

# === Step 8: Delete the document ===

collection.delete_one({"_id": document["_id"]})          # Delete the document by ID
print("Document deleted.")                               # Confirmation message

# === Step 9: Confirm deletion ===

final_check = collection.find_one({"_id": document["_id"]})  # Try to find the deleted document
if final_check is None:
    print("Final check: document successfully removed from the database.")  # Deletion successful
else:
    print("Document still exists:", final_check)  # Document still present (unexpected)

# === Step 10: Close the connection ===

client.close()                                            # Close the MongoDB connection
print("MongoDB connection closed.")                       # Confirmation message