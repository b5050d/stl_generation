"""
Alright in this script we want to consume the messages and respond to the
producer 
"""

import pika
import time
import sys

# TODO - get these from environment variables
RABBIT_MQ_USERNAME = 'user'
RABBIT_MQ_PASSWORD = 'password'
RABBIT_MQ_PORT = 5672
RABBIT_MQ_ATTEMPTS = 10
RABBIT_MQ_QUEUE_NAME = "test_queue"


class Consumer:
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
        def callback(ch, method, properties, body):
            print(f"Received: {body.decode()}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)

        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


if __name__ == "__main__":
    a = Consumer()
    a.main()