FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application
COPY . /app/

# Make start script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Use start script
CMD ["./start.sh"]
