import pika
import time
import argparse


def on_request(ch, method, props, body):
    time_delay = int(body)
    print(f'get request from({props.reply_to}), get time_delay={time_delay}')
    response = business_logic(time_delay)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
            ),
        body=str(response)
    )

    ch.basic_ack(
        delivery_tag=method.delivery_tag
        )

def business_logic(time_delay=10):
    print('I make main job')
    time.sleep(time_delay)
    print('I finish main job')
    return 'ok'


def main(queue_name):
    # NOTE: установления соединения
    connections = pika.BlockingConnection(
        parameters=pika.ConnectionParameters('localhost'))
    channel = connections.channel()

    # NOTE: объявления очереди и даем ей название
    channel.queue_declare(
        queue=queue_name
        )

    # NOTE: определяем подписчика
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=on_request
        )

    channel.basic_qos(
        prefetch_count=1        # указываем колл-во процессов
    )
    channel.start_consuming()


if __name__ == "__main__":
    print('[*] start rpc server')
    arg_parser  = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-q', '--queue', help='queue name', type=str)
    args = arg_parser.parse_args()
    if not args.queue:
        raise Exception('the args "--queue" is empty')
    main(args.queue)

