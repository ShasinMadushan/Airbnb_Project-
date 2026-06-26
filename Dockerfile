# Use a lightweight, official Python runtime
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code and data directories into the container
COPY src/ src/
COPY data/ data/

# Command to run your pipeline
CMD ["python", "src/transformation/clean_listings.py"]