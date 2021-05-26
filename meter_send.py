from os import register_at_fork
from time import time
import pika
import random
import time 

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='value')
while True:
    time.sleep(3)
    value=random.randrange(0,9000)
    channel.basic_publish(exchange='', routing_key='meter_data', body=str(value))
connection.close()