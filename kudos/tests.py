from django.test import TestCase

# Create your tests here.
# version: "3.3"

# services:
#   db:
#     image: postgres:13
#     environment:
#       POSTGRES_USER: ${POSTGRES_USER}
#       POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
#       POSTGRES_DB: ${POSTGRES_DB}
#     volumes:
#       - postgres_data:/var/lib/postgresql/data
#     networks:
#       - kudos_network

#   redis:
#     image: redis:alpine
#     networks:
#       - kudos_network

#   web:
#     build: .
#     command: >
#       sh -c "while ! nc -z db 5432; do sleep 1; done &&
#              python3 manage.py makemigrations kudos &&
#              python3 manage.py migrate &&
#              python3 manage.py runserver 0.0.0.0:8000"
#     volumes:
#       - .:/app
#     ports:
#       - "8000:8000"
#     depends_on:
#       - db
#       - redis
#     networks:
#       - kudos_network
#     env_file:
#       - .env

#   celery:
#     build: .
#     command: celery -A kudos_project worker --loglevel=info
#     volumes:
#       - .:/app
#     depends_on:
#       - web
#     networks:
#       - kudos_network
#     env_file:
#       - .env

#   celery-beat:
#     build: .
#     command: celery -A kudos_project beat --loglevel=info
#     volumes:
#       - .:/app
#     depends_on:
#       - web
#     networks:
#       - kudos_network
#     env_file:
#       - .env

#   demo_data:
#     build: .
#     command: >
#       sh -c "while ! nc -z db 5432; do sleep 1; done &&
#              python3 manage.py migrate &&
#              python3 manage.py generate_demo_data"
#     depends_on:
#       - web
#     networks:
#       - kudos_network
#     env_file:
#       - .env

# volumes:
#   postgres_data:

# networks:
#   kudos_network:
#     driver: bridge
