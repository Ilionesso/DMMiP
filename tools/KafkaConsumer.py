import json
from time import sleep

from kafka import KafkaConsumer

if __name__ == '__main__':
    topic_name = 'test'

    consumer = KafkaConsumer(topic_name,
                             auto_offset_reset='earliest',
                             consumer_timeout_ms=1000,
                             bootstrap_servers=['ip-172-31-6-28.ec2.internal:9092',
                                                'ip-172-31-11-76.ec2.internal:9092,',
                                                'ip-172-31-5-160.ec2.internal:9092'])
    for msg in consumer:
        print(msg.value)


        sleep(3)

    # if consumer is not None:
    #     consumer.close()
