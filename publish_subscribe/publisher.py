import pika
import sys


def main(message):
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # не объявляем очередь нам это не нужно так как будем пулить в Обменник
    # result = channel.queue_declare(queue='', exclusive=True)

    channel.exchange_declare(
        exchange='logs',                                       # указываем обменник
        exchange_type='fanout'                                 # указываем тип обменника
    )
    channel.basic_publish(
        exchange='logs',                                       # указываем имя Обменника
        routing_key='',                                        # не указываем очередь т.к. будет Обменник
        body=message
    )
    print(f" [*] Sent {message}")


if __name__ == '__main__':
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    main(message)
