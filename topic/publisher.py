from sqlite3 import connect
import pika
import argparse


def  main(topic_pattern:str, message:str):
    connections = pika.BlockingConnection(
        parameters=pika.ConnectionParameters('localhost'))
    channel = connections.channel()

    channel.exchange_declare(
        exchange='animal_ex',
        exchange_type='topic'
    )


    channel.basic_publish(
        exchange='animal_ex',
        routing_key=topic_pattern,
        body=message
    )

    msg = f'{topic_pattern}: {message}'
    print(f'[*] Send "{msg}"')


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='publisher')
    arg_parser.add_argument('-t', '--topic', type=str, default='lazy.#', help='topic (["*.orange.*", "*.*.rabbit", "lazy.#."]) for consumer binding.')
    arg_parser.add_argument('-m', '--message', type=str, default='fast animal', help='message body')
    args = arg_parser.parse_args()
    main(args.topic, args.message)
