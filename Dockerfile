# Use a base image with all necessary compilers
FROM python:3.11-slim

# Install OS dependencies and compilers
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    nodejs \
    npm \
    curl \
    unzip \
    python3 \
    python3-pip \
    && apt-get clean

# Set environment variables for Dart
ENV DART_SDK_VERSION=3.5.2 
ENV DART_SDK_ARCH=arm64 

# Download and install Dart ARM SDK
RUN curl -o dart-sdk.zip https://storage.googleapis.com/dart-archive/channels/stable/release/$DART_SDK_VERSION/sdk/dartsdk-linux-$DART_SDK_ARCH-release.zip 
RUN unzip dart-sdk.zip -d /usr/lib/ && rm dart-sdk.zip

# Add Dart to PATH
ENV PATH="/usr/lib/dart-sdk/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy your Django project files to the container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Collect static files (optional)
# RUN python manage.py collectstatic --noinput

# Expose the port the Django app runs on
EXPOSE 8000

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=codeware.settings
ENV PYTHONUNBUFFERED=1

# Run Django server (for development, use `gunicorn` for production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
