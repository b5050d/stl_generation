FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY consumer.py .

RUN pip install pika

CMD ["python", "consumer.py"]
