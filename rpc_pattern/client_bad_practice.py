# В представленном примере мы создаем очередь обратных вызовов для каждого запроса на сервер RPC. Это довольно неэффективно


import pika
import argparse
import sys


def on_response(ch, method, props, body):
    print(f'get response: {body}')
    sys.exit(0)

def main(request_body):
    connections = pika.BlockingConnection(
        parameters=pika.ConnectionParameters('localhost')
    )
    channel = connections.channel()

    result = channel.queue_declare(
        queue='',
        exclusive=True
    )

    queue_name = result.method.queue

    print(f'make request from body (delay) = {request_body}')
    channel.basic_publish(
        exchange='',
        routing_key='rpc_bad_test',                # определяем ключ
        properties=pika.BasicProperties(
            reply_to=queue_name                 # используется для обозначения очереди обратных вызовов.
        ),
        body=str(request_body)
    )

        # NOTE: определяем подписчика
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=on_response
        )
    channel.start_consuming()



if __name__ == "__main__":
    print("[*] Start client APP")
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-t', '--time_delay', type=int, help='time delay', default=6)
    args = arg_parser.parse_args()
    main(request_body=args.time_delay)
