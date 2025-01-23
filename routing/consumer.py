import os
import pika
import sys
import argparse
import datetime
from typing import (
    List
)


def main(log_file: str = '', consumer_types: List = ['info']):

    connections = pika.BlockingConnection(
        parameters=pika.ConnectionParameters('localhost'))
    channel = connections.channel()

    # NOTE: настраиваем обменник
    channel.exchange_declare(
        exchange='direct_logs',                 # указываем обменник
        exchange_type='direct'                  # указываем тип обменника
    )

    # NOTE: настраиваем потребителя
    result = channel.queue_declare(
        queue='',                               # указываем чтобы rabbit сам генерировал название очереди
        exclusive=True                          # после отключения Consumer очередь будет удаленна
    )
    queue_name = result.method.queue
    print('queue name the - ', queue_name)

    # NOTE: связываем очередь с обменником
    for type in consumer_types:
        channel.queue_bind(                        # связываем ОЧЕРЕДЬ c ОБМЕННИКОМ
            queue=queue_name,                      # имя ОЧЕРЕДи
            exchange='direct_logs',                # имя ОБМЕННИКОМ
            routing_key=type                       # связываем очередь с ключом
        )

    def callback(ch, method, properties, body, log_file_path=log_file):
        # функция которая будет вызываться при получении сообщения от Publisher
        msg = f"{datetime.datetime.now()} {body.decode()}\n"
        if log_file:
            with open(log_file_path, 'a') as f:
                f.writelines(msg)
        else:
            print(msg)

    # NOTE: настраиваем потребителя
    channel.basic_consume(
        queue=queue_name,
        auto_ack=True,                          # указываем что consumer не будет подтверждать обработку сообщения
        on_message_callback=callback
    )
    channel.start_consuming()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='consumers')
    parser.add_argument('-f', '--file', type=str, help='file path', default='')
    parser.add_argument('-t', '--type', type=str,
                        help="type consumer ('info', 'warning', 'error')", default='info')
    args = parser.parse_args()
    print(args.type.split(' '))
    try:
        print(' [*] Waiting for messages. To exit press CTRL+C')
        main(args.file, args.type.split(' '))
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
