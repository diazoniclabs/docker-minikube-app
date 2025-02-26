# Use official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the app will run
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
