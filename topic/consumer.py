import argparse
import pika
import os
import sys
from typing import (
    List
)


def main(topic_patterns: List):
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange='animal_ex',  # set name to exchange
        exchange_type='topic'  # set mode topic when used patterns
    )

    result = channel.queue_declare(
        queue='',               # for rabbit generating name for queue
        exclusive=True          # for del queue after stop consumer
    )
    name_queue = result.method.queue

    # NOTE: bind the queue from the exchange by routing_key
    for topic in topic_patterns:
        channel.queue_bind(
            queue=name_queue,
            exchange='animal_ex',
            routing_key=topic       # set topic pattern (lazy.# or )
        )
    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(f" [x] {method.routing_key}: {body}")

    channel.basic_consume(
        queue=name_queue,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()


if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser(description="consumer app")
    arg_parse.add_argument(
        '-t', '--topic',
        type=str, default='lazy.#',
        help='past the topic for bind consumer to queue (["*.orange.*", "*.*.rabbit", "lazy.#."])'
    )
    args = arg_parse.parse_args()
    try:
        main(args.topic.split(' '))
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
