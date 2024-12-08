import pika
import json
from sqlalchemy.orm import Session
from . import crud, database


def consume_messages(queue_name: str, db_session_maker):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"Received message: {message}")

        # Process the message and save it to the database
        with db_session_maker() as db:
            crud.create_notification(db, message)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Listening for messages on queue: {queue_name}")
    channel.start_consuming()
