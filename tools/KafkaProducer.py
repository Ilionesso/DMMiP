import datetime

from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'ip-172-31-6-28.ec2.internal:9092,'
                                   'ip-172-31-11-76.ec2.internal:9092,'
                                   'ip-172-31-5-160.ec2.internal:9092'})


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


some_data_source = []
for i in range(20):
    new_Value = str(i) + " " + str(datetime.datetime.now())
    some_data_source.append(new_Value)


for data in some_data_source:
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    p.produce('test', data.encode('utf-8'), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()