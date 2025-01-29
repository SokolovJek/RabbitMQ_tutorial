import pika


connect = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connect.channel()

channel.queue_declare(
    'rpc_test12',
    exclusive=True
)

channel.basic_publish(
    exchange='',
    routing_key='rpc_test',
    body=str('time_delay'),
)