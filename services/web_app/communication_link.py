"""
This process is intended to write to rabbitmq
and then get responses from the backend and present that to the user
"""

import pika
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

processing_queue = 'processing_queue'
reply_queue = 'reply_queue'

# Send request
corr_id = str(uuid.uuid4())
channel.queue_declare(queue=reply_queue, durable=True)
channel.basic_publish(
    exchange='',
    routing_key=processing_queue,
    properties=pika.BasicProperties(
        reply_to=reply_queue,
        correlation_id=corr_id,
        delivery_mode=2  # make message persistent
    ),
    body=image_bytes
)

# Wait for response
def on_response(ch, method, props, body):
    if props.correlation_id == corr_id:
        print("Got processed data:", len(body))
        # Save or process response data
        ch.basic_ack(delivery_tag=method.delivery_tag)
        connection.close()

channel.basic_consume(
    queue=reply_queue,
    on_message_callback=on_response,
    auto_ack=False
)

print("Waiting for response...")
channel.start_consuming()
