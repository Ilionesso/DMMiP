import json
from time import sleep

import numpy
from kafka import KafkaConsumer


def init_kafka_consumer(topic_name):
    return KafkaConsumer(topic_name,
                         consumer_timeout_ms=60000,
                         bootstrap_servers=['ip-172-31-6-28.ec2.internal:9092',
                                            'ip-172-31-11-76.ec2.internal:9092',
                                            'ip-172-31-5-160.ec2.internal:9092'])


def decode_matrix(matrix_bytes, matrix_data_type, matrix_shape):
    return numpy.frombuffer(matrix_bytes, dtype=matrix_data_type).reshape(matrix_shape)


if __name__ == '__main__':
    topic_name = 'test'

    consumer = init_kafka_consumer(topic_name)

    for msg in consumer:
        print(decode_matrix(msg.value, 'int64',(500, 500)))

    # if consumer is not None:
    #     consumer.close()
