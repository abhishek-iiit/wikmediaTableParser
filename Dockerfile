# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY wikipedia_parser/ wikipedia_parser/
COPY .env .env

# Set entrypoint
ENTRYPOINT ["python", "-m", "wikipedia_parser.main"]
