# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
# It's best to use a requirements.txt to manage dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (if applicable)
EXPOSE 5000

# Command to run the application (e.g., Flask or FastAPI server)
CMD ["python", "app.py"]
