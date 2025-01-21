import pika
import sys
import os





def callback(ch, method, properties, body):
    print(f' [X] Received {body}')



def main():
    # подключаемся
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    channel = connection.channel()

    # проверяем\создаем очередь
    channel.queue_declare('hello')
    # передаем колбек функцию на событие
    channel.basic_consume(queue='hello',
                        auto_ack=True,
                        on_message_callback=callback)

    # старт цикла в ожидании сообщения
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
