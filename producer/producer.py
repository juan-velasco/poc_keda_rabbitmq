#!/usr/bin/env python
import pika, time, os

rabbitmqhost = os.environ["RABBITMQ_HOST"]

credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmqhost, credentials= credentials))
channel = connection.channel()

channel.queue_declare(queue='poc_keda')

counter = 0
while True:
    counter = counter + 1
    channel.basic_publish(exchange='', routing_key='poc_keda', body='Hello World! '+str(counter))
    time.sleep(0.1)

connection.close()