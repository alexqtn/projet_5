#!/bin/bash

# Step 1: Capture the MongoDB hostname and port from arguments
host="$1"      # First argument: the hostname (e.g., "mongo")
port="$2"      # Second argument: the port number (e.g., "27017")

# Step 2: Shift the first two arguments so the rest becomes the command to run
shift 2
cmd="$@"

# Step 3: Wait for MongoDB to be ready
# This loop checks if MongoDB is accessible on the given host and port
until nc -z "$host" "$port"; do
  echo "Waiting for MongoDB at $host:$port..."
  sleep 2
done

# Step 4: MongoDB is now ready
echo "MongoDB is up - executing command"

# Step 5: Execute the Python migration script
# The command is passed as parameters after -- in Dockerfile CMD
exec $cmd