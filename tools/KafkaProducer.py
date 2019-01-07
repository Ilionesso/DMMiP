import datetime

from kafka import KafkaProducer


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['ip-172-31-6-28.ec2.internal:9092',
                                                     'ip-172-31-11-76.ec2.internal:9092',
                                                     'ip-172-31-5-160.ec2.internal:9092'])
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


def publish_message(producer_instance, topic_name, value):
    try:
        # key_bytes = bytes(key, encoding='utf-8')
        value_bytes = value.encode()
        producer_instance.send(topic_name, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message' + str(ex))


some_data_source = []
for i in range(20):
    new_Value = str(i) + " " + str(datetime.datetime.now())
    some_data_source.append(new_Value)

p = connect_kafka_producer()
for data in some_data_source:
    publish_message(p, 'test', data)