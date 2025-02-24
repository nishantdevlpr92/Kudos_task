# Kudos App

A Django application where users can give kudos to other users in their organization. This app includes features like weekly kudos limits, messages, and tracking who gave kudos to whom.

## Features
- Send kudos to others with a personalized message.
- Track received kudos.
- Weekly reset of kudos limits.
- Celery task for periodic actions like resetting kudos weekly.

---

## **Setup Guide**

# Build and start the Docker containers

```docker-compose up --build```

Or 

```docker-compose up``` 

This command will build the Docker images and start the following services:

Web: Django app
db: PostgreSQL database
redis: Redis instance for Celery
celery: Celery worker for background tasks
celery-beat: Celery Beat for periodic tasks

## Create super user to view the admin django admin panel

Run the following command to enter the container:

```
docker exec -it <container_name> bash
```

Once inside the container, navigate to your Django project folder (if needed) and run:

```
python manage.py createsuperuser
```
Enter the required details (username, email, and password) when prompted.

After creating the superuser, exit the container:

```
exit
```

Now, go to your Django admin panel:

```
http://localhost:8000/admin

```
Log in using the superuser credentials you just created.

## Access frontend

Go to the given url:

```
http://localhost:3000
```