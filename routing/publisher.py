import pika
import argparse


SUPPORT_TYPES = ['info', 'warning', 'error']


def main(type_msg: str, message: str):
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # NOTE: не объявляем очередь нам это не нужно так как будем пулить в Обменник
    # result = channel.queue_declare(queue='', exclusive=True)

    # NOTE: настраиваем обменник
    channel.exchange_declare(
        exchange='direct_logs',         # указываем обменник
        exchange_type='direct'          # указываем тип обменника
    )

    msg = f'[{type_msg}]: {message}'
    # NOTE: настраиваем публикации
    channel.basic_publish(
        exchange='direct_logs',         # указываем имя Обменника
        routing_key=type_msg,           # указываем routing_key чтобы exchange знал в какую очередь пулить сообщение
        body=msg
    )
    print(f" [*] Sent {msg}")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='publisher')
    arg_parser.add_argument('-t', '--type', type=str, default='info',
                            help="type message ('info', 'warning', 'error')")
    arg_parser.add_argument('-m', '--message', type=str, default='Hello World!',
                            help="message string")
    args = arg_parser.parse_args()
    main(args.type, args.message)
