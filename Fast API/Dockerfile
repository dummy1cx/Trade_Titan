# Base image
## Pythin version 3.12 slim
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Disable .pyc and enable instant logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# copy app//model//requirements.txt
COPY app ./app
COPY model ./model
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]