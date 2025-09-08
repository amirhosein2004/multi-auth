# Use Python 3.11 slim image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code (including manage.py and erp_main/)
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "erp_main.wsgi:application"] 