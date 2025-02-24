# Kudos App

A Django application where users can give kudos to other users in their organization. This app includes features like weekly kudos limits, messages, and tracking who gave kudos to whom.

## Features
- Send kudos to others with a personalized message.
- Track received kudos.
- Weekly reset of kudos limits.
- Celery task for periodic actions like resetting kudos weekly.

---

## **Setup Guide**
Steps for Local Development (Without Docker)
python3 -m venv venv
source venv/bin/activate

**With the virtual environment activated, install the dependencies**
pip install -r requirements.txt

**Run database migrations to set up the schema**
python3 manage.py makemigrations
python3 manage.py migrate

**To generate demo data, run the management command**
python manage.py generate_demo_data

**Now run the Django development server**
python3 manage.py runserver

**With Redis and Celery installed, run Celery Worker from your Django project directory**
celery -A kudos_project worker --loglevel=info

**You can run Celery Beat with the following command**
celery -A kudos_project beat --loglevel=info

## **Setup Guide**
**Steps for Local Development (With Docker)**
# Build and start the Docker containers
docker-compose up --build

This command will build the Docker images and start the following services:

Web: Django app
db: PostgreSQL database
redis: Redis instance for Celery
celery: Celery worker for background tasks
celery-beat: Celery Beat for periodic tasks

# Apply migrations to set up the database
docker-compose exec web python manage.py migrate

# Stop all containers
docker-compose down

# Stop containers and remove volumes
docker-compose down -v


