FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for COM/RAS libraries in real usage)
# RUN apt-get update && apt-get install -y ...

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN pip install --no-cache-dir .

# Environment variables
ENV PROMETHEUS_LISTEN_PORT=8000
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run the exporter
CMD ["onec-exporter"]
