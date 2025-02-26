# Use Python's official image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install netcat (nc) and other dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Copy the users.csv file into the container (ensure it's in the root of your project)
COPY users.csv /app/users.csv

# Set environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=kudos_project.settings

# Expose port for the Django app
EXPOSE 8000

# Run the Django development server by default (you can override this to run other commands)
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
