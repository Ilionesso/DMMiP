import pickle

from kafka import KafkaProducer


def init_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['ip-172-31-6-28.ec2.internal:9092',
                                                     'ip-172-31-11-76.ec2.internal:9092',
                                                     'ip-172-31-5-160.ec2.internal:9092'],
                                  value_serializer=lambda m: pickle.dumps(m))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


def produce(producer_instance, value, topic_name='strassen'):
    try:
        producer_instance.send(topic_name, value=value)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message' + str(ex))

#
# if __name__ == '__main__':
#     some_data_source = []
#     for i in range(20):
#         new_Value = str(i) + " " + str(datetime.datetime.now())
#         some_data_source.append(new_Value)
#
#     p = init_kafka_producer()
#     for data in some_data_source:
#         publish_message(p, 'test', data)
