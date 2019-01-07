from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers='ip-172-31-6-28.ec2.internal:9092,'
                                           'ip-172-31-11-76.ec2.internal:9092,'
                                           'ip-172-31-5-160.ec2.internal:9092')
consumer.subscribe(['topic'])
for msg in consumer:
    print(msg.headers)
    print(msg)
