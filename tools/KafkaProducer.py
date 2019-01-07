import datetime

from kafka import KafkaProducer

p = KafkaProducer(bootstrap_servers='ip-172-31-6-28.ec2.internal:9092,'
                                    'ip-172-31-11-76.ec2.internal:9092,'
                                    'ip-172-31-5-160.ec2.internal:9092')

some_data_source = []
for i in range(20):
    new_Value = str(i) + " " + str(datetime.datetime.now())
    some_data_source.append(new_Value)

for data in some_data_source:
        p.send('test', data.encode('utf-8'))
