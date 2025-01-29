from urllib import response
import pika
import argparse
import uuid


class RPC_client:
    def __init__(self) -> None:
        self.connect = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connect.channel()

        result = self.channel.queue_declare(
            queue='',
            exclusive=True
        )
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.get_response,
            auto_ack=True
        )

        self.corr_id = None
        self.response = None
        print(f'[*] start rpc client by queue name: {self.callback_queue}')

    def get_response(self, ch, method, properties, body):
        print('get response ')
        if properties.correlation_id == self.corr_id:
            print(f'read body {body}')
            self.response = body

    def do_call_remote_method(self, time_delay):
        self.corr_id = str(uuid.uuid4())
        self.response = None

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_test',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=str(time_delay),
        )
        while self.response is None:
            print('i sleep wait the response')
            self.connect.process_data_events(time_limit=None)
        return self.response


def main(time):
    rpc_client = RPC_client()

    print(f" [x] Requesting fib({time})")
    response = rpc_client.do_call_remote_method(time)
    print(f" [.] Got {response}")


if __name__ == "__main__":
    arg_parser  = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-t', '--time', help='time for delay', type=int, default=7)
    args = arg_parser.parse_args()
    main(args.time)
