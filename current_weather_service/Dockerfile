# Dockerfile for the current weather service
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python", "app/current_weather_service.py"]