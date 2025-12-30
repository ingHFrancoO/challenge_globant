# Base image
FROM python:3.11-slim

# Avoid log buffering
ENV PYTHONUNBUFFERED=1

# install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Create app folder
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Copy cron file
RUN mkdir -p /app/logs
COPY docker/pipeline_cron /etc/cron.d/pipeline_cron
RUN chmod 0644 /etc/cron.d/pipeline_cron
RUN crontab /etc/cron.d/pipeline_cron

# Expose FastAPI port
EXPOSE 8000

# Run cron in the background and FastAPI in the foreground
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8000