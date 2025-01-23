import os
import pika
import time
import sys


def main(log_file=''):
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

    def callback(ch, method, properties, body, logging=log_file):
        msg = f"{time.time()}: [*] Received {body.decode()}, count({body.count(b'.')})\n"
        if log_file:
            with open(log_file[0], 'a') as f:
                f.writelines(msg)
        else:
            print(print(msg))
        time.sleep(body.count(b'.'))
        print(" [*] Done")

    channel.basic_consume(
        queue=queue_name,
        auto_ack=True,                  # указываем что consumer не будет подтверждать обработку сообщения
        on_message_callback=callback
    )
    channel.start_consuming()


if __name__ == "__main__":
    try:
        print(' [*] Waiting for logs. To exit press CTRL+C')
        path_log_file = sys.argv[1:]
        main(path_log_file)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
