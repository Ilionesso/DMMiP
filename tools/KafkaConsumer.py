from confluent_kafka import Consumer, KafkaError
import json

def _statsCallback(jsonStr):
    producer_metrics = json.loads(jsonStr)
    print(producer_metrics['msg_cnt'])
    for topic in producer_metrics['topics']:
        for partition in producer_metrics['topics'][topic]['partitions']:
            if producer_metrics['topics'][topic]['partitions'][partition]['consumer_lag'] > 0:
                print("Topic " + topic + " partition " + partition + " lag " + str(producer_metrics['topics'][topic]['partitions'][partition]['consumer_lag']))



c = Consumer({
    'bootstrap.servers': 'ip-172-31-6-28.ec2.internal:9092,'
                         'ip-172-31-11-76.ec2.internal:9092,'
                         'ip-172-31-5-160.ec2.internal:9092',
    'group.id': 'test_group',
    'auto.offset.reset': 'earliest',
    'statistics.interval.ms': 100
})

# Without subscription the metrics do not appear
c.subscribe(['test'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue


     # print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()