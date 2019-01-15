import pickle

from kafka import KafkaConsumer


def init_kafka_consumer(topic_name='strassen'):
    return KafkaConsumer(topic_name,
                         consumer_timeout_ms=100,
                         bootstrap_servers=['ip-172-31-6-28.ec2.internal:9092',
                                            'ip-172-31-11-76.ec2.internal:9092',
                                            'ip-172-31-5-160.ec2.internal:9092'],
                         value_deserializer=lambda m: pickle.loads(m))


def consume(consumer):
    try:
        return next(consumer)
    except Exception as e:
        return None
