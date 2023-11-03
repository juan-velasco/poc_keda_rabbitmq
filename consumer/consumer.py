#!/usr/bin/env python
import pika, sys, os, time

rabbitmqhost = os.environ["RABBITMQ_HOST"]

def main():
    credentials = pika.PlainCredentials('admin','admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmqhost, credentials= credentials))
    channel = connection.channel()
    
    channel.basic_qos(prefetch_count=1, global_qos=False)

    channel.queue_declare(queue='poc_keda')

    def callback(ch, method, properties, body):
        time.sleep(0.5)
        print(f" [x] Received {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='poc_keda', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)