FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

RUN pip install redis && \
    pip install Flask && \
    pip install prometheus_client

COPY app.py .

CMD ["python", "app.py"]