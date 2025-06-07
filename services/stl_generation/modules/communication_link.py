"""
This script is intended to recieve messaages from the web app
over rabbitmq and then generate the STL and add that to rabbitmq
"""

import pika

def process_image(image_bytes):
    # Placeholder for your processing logic
    processed_image_bytes = image_bytes  # For example
    return processed_image_bytes

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

processing_queue = 'processing_queue'
channel.queue_declare(queue=processing_queue, durable=True)

def on_request(ch, method, props, body):
    processed_data = process_image(body)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id,
            delivery_mode=2
        ),
        body=processed_data
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=processing_queue, on_message_callback=on_request)

print("Awaiting requests...")
channel.start_consuming()
