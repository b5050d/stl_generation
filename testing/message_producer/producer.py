"""
this script produces messages and adds to the rabbitmq
"""

# Handle Imports

import pika
import time
import sys

# Connect to RabbitMQ
# TODO - get these from environment variables
RABBIT_MQ_USERNAME = 'user'
RABBIT_MQ_PASSWORD = 'password'
RABBIT_MQ_PORT = 5672
RABBIT_MQ_ATTEMPTS = 10
RABBIT_MQ_QUEUE_NAME = "test_queue"


class Producer:
    def __init__(self):
        self.set_up_rabbitmq()

    def set_up_rabbitmq(self):
        credentials = pika.PlainCredentials(RABBIT_MQ_USERNAME, RABBIT_MQ_PASSWORD)
        parameters = pika.ConnectionParameters('rabbitmq', RABBIT_MQ_PORT, '/', credentials)
        self.connection = None

        for i in range(10):
            try:    
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                break
            except pika.exceptions.AMQPConnectionError:
                print("Waiting for RabbitMQ...retrying in 2 seconds.")
                time.sleep(2)

        if self.connection is None:
            print("Failed to connect to RabbitMQ after retries. Exiting.")
            sys.exit(1)

        # Declare a queue
        self.queue_name = RABBIT_MQ_QUEUE_NAME
        self.channel.queue_declare(queue=self.queue_name, durable=True)
    
    def main(self):
        # Send messages
        for i in range(500):
            message = f"Hello {i}"
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2  # make message persistent
                )
            )
            print(f"Sent: {message}")
            time.sleep(1)  # simulate some delay

        self.connection.close()


if __name__ == "__main__":
    a = Producer()
    a.main()
