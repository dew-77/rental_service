# rabbitmq.py
import pika
import json
from typing import Any
from . import crud, database


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


def consume_messages(queue_name: str, callback: callable):
    # Setup RabbitMQ connection (simplified example)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Callback to handle messages
    def on_message(channel, method, properties, body):
        message = body.decode()
        # Convert the message into a dictionary (or JSON)
        message_data = json.loads(message)
        
        # Get a new database session
        db = next(database.get_db())
        
        # Process the message (call the callback function)
        callback(message_data, db)
        
        # Acknowledge the message
        channel.basic_ack(delivery_tag=method.delivery_tag)

    # Start consuming messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    
    print(f" [*] Waiting for messages in {queue_name}. To exit press CTRL+C")
    channel.start_consuming()