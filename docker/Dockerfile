# Step 1: Official image for Python 3.10 on Debian Bullseye
FROM python:3.10-slim-bullseye

# Étape supplémentaire avant RUN pip install
RUN apt-get update && apt-get install -y bash netcat && apt-get clean

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Explanation:
# This uses a minimal version of Python 3.10, which includes only what is necessary to run Python scripts.
# It helps reduce the image size and improves performance and portability.

# Step 2: Set the working directory inside the container
WORKDIR /app

# Explanation:
# All paths and commands in this container will now run relative to /app.
# This keeps everything organized inside the container.

# Step 3: Copy the project files into the container
COPY ./scripts/ ./scripts/
COPY ./data/ ./data/
COPY ./requirements.txt ./
COPY ./docker/wait-for-mongo.sh ./wait-for-mongo.sh

# Explanation:
# - Copies your migration scripts into the container under /app/scripts
# - Copies your data CSVs into /app/data
# - Copies the Python dependencies file (requirements.txt) for installation
# - Copies the wait script into the working directory

# Step 4: Install Python dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Explanation:
# - Installs all packages listed in requirements.txt (e.g., pandas, pymongo, python-dotenv)
# - The `--no-cache-dir` flag prevents pip from caching downloaded packages,
#   which helps keep the image size smaller.

# Step 5: Make the wait script executable
RUN chmod +x wait-for-mongo.sh

# Explanation:
# - This gives execution permissions to the wait-for-mongo.sh script
# - Without this step, the script could not be launched from CMD

# Step 6: Define the command to run when the container starts
CMD ["./wait-for-mongo.sh", "mongo", "27017", "--", "python", "scripts/migration.py"]

# Explanation:
# - The container will first run wait-for-mongo.sh to wait for MongoDB on host `mongo`, port 27017
# - Once the MongoDB container is ready, the Python migration script will be executed
# - This ensures a stable startup sequence without connection errors
