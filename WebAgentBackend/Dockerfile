# 1. Use an official lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Environment flags to prevent .pyc generation and enable real-time logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copy requirements file and install dependencies first (caches layers efficiently)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your application source code into the container
COPY ./app ./app
# COPY ./credentials ./credentials

# 6. Expose the port FastAPI runs on
EXPOSE 8000

# 7. Start the server using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]