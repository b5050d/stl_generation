FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY producer.py .

RUN pip install pika

CMD ["python", "producer.py"]
