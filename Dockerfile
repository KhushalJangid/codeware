# Use a base image with all necessary compilers
FROM python:3.13-slim

# Install OS dependencies and compilers
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    nodejs \
    npm \
    python3 \
    python3-pip \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy your Django project files to the container
COPY . .

# Install Python dependencies
RUN pip install poetry
RUN poetry install

# Collect static files (optional)
# RUN python manage.py collectstatic --noinput

# Expose the port the Django app runs on
EXPOSE 8000

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=codeware.settings
ENV PYTHONUNBUFFERED=1

# Run Django server (for development, use `gunicorn` for production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
