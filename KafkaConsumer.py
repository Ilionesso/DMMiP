import json
from time import sleep

import numpy
from kafka import KafkaConsumer


def init_kafka_consumer(topic_name):
    return KafkaConsumer(topic_name,
                         consumer_timeout_ms=60000,
                         bootstrap_servers=['ip-172-31-6-28.ec2.internal:9092',
                                            'ip-172-31-11-76.ec2.internal:9092',
                                            'ip-172-31-5-160.ec2.internal:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))





if __name__ == '__main__':
    topic_name = 'test'

    consumer = init_kafka_consumer(topic_name)

    for msg in consumer:
        print(json.loads(msg))

    # if consumer is not None:
    #     consumer.close()
