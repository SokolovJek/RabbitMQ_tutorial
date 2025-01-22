import pika
import time
import sys
import os


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}, count({body.count(b'.')})")
    time.sleep(body.count(b'.'))
    # отправляем в очередь подтверждение что мы обработали сообщение
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(" [x] Done")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # объявляем и настраиваем новую очередь, настраиваем что-бы очередь сохраняла состояние после перезапуска rabbitmq  (durable=True), это можно задать только новой очереди
    channel.queue_declare('task_queue', durable=True)

    # аргумент auto_ack=True автоматически подтверждает прием сообщений потребителем
    # channel.basic_consume('hello', auto_ack=True, on_message_callback=callback)

    # будем вручную подтверждать прием и обработку сообщения в callback функции
    channel.basic_consume('task_queue', auto_ack=False, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
