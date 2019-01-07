from MatrixFiles import readMatrixA
from tools.KafkaProducer import init_kafka_producer, publish_message

matrix = readMatrixA()
producer = init_kafka_producer()
publish_message(producer, 'test', matrix)


