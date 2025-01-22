import os
import pika
import time
import sys


def callback(ch, method, properties, body):
    print(f" [*] Received {body.decode()}, count({body.count(b'.')})")
    time.sleep(body.count(b'.'))
    # ch.basic_ack(delivery_tag=method.delivery_tag) # отправляем в очередь подтверждение что мы обработали сообщение
    print(" [*] Done")


def main():
    connections = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connections.channel()

    channel.exchange_declare(
        exchange='logs',
        exchange_type='fanout')
    result = channel.queue_declare(
        queue='',                        # указываем чтобы rabbit сам генерировал название очереди
        exclusive=True                   # после отключения Consumer очередь будет удаленна
    )
    queue_name = result.method.queue
    print('queue name the - ', queue_name)

    channel.queue_bind(                 # связываем ОЧЕРЕДЬ c ОБМЕННИКОМ
        queue=queue_name,               # имя ОЧЕРЕДи
        exchange='logs'                 # имя ОБМЕННИКОМ
    )

    channel.basic_consume(
        queue=queue_name,
        auto_ack=True,                  # указываем что consumer не будет подтверждать обработку сообщения
        on_message_callback=callback
    )
    channel.start_consuming()


if __name__ == "__main__":
    try:
        print(' [*] Waiting for logs. To exit press CTRL+C')
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
