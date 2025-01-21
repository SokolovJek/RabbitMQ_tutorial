import pika


# установить соединение
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
channel = connection.channel()

# создадим\проверим очередь hello
channel.queue_declare(queue='hello')


channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(' [X] Send "Hello world!"')

connection.close()
