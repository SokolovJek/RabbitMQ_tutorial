import pika
import sys


def main(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # channel.queue_declare('hello')
    # объявляем и настраиваем новую очередь, настраиваем что-бы очередь сохраняла состояние после перезапуска rabbitmq  (durable=True), это можно задать только новой очереди
    channel.queue_declare('task_queue', durable=True)
    # помечаем сообщение параметром delivery_mode = pika.DeliveryMode.Persistent для того чтобы rabbitmq сохранял его.
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.DeliveryMode.Persistent
                          ))
    print(f" [x] Sent {message}")


if __name__ == '__main__':
    message = ' '.join(sys.argv[1:]) or 'Hello world!'
    main(message)
