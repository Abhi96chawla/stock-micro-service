# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nginx \
    build-essential \
    libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Define environment variable for Google Cloud credentials (if needed)
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/bubbly-mantis.json"

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/sites-available/default

# Expose the ports
EXPOSE 80 5002

# Start Nginx and the Flask application
CMD service nginx start && python3 upload.py
