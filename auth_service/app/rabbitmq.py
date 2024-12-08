# rabbitmq.py
import pika
import json
from typing import Any

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')  # Change to your RabbitMQ server's host
    )
    channel = connection.channel()
    return channel


def publish_message(queue_name: str, message: Any):
    channel = get_rabbitmq_connection()

    # Ensure the queue exists
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Publish message to the queue
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        )
    )
    print(f"Sent message to {queue_name}: {message}")
    channel.close()


def consume_messages(queue_name: str, callback):
    channel = get_rabbitmq_connection()

    # Ensure the queue exists
    channel.queue_declare(queue=queue_name, durable=True)

    # Define the callback function that handles the message
    def on_message(ch, method, properties, body):
        message = json.loads(body)
        callback(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

    # Set up consumer to listen for messages
    channel.basic_consume(queue=queue_name, on_message_callback=on_message)

    print(f"Waiting for messages in {queue_name}...")
    channel.start_consuming()
