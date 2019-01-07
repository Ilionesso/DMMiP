import numpy

from MatrixFiles import readMatrixA
from KafkaProducer import init_kafka_producer, publish_message

matrix = readMatrixA()
matrix_data_type = matrix.dtype.name
matrix_shape = matrix.shape
matrix_bytes = matrix.tobytes()

producer = init_kafka_producer()
publish_message(producer, 'test', matrix)


def encode_matrix(matrix):
    return matrix.tobytes()


def decode_matrix(matrix_bytes, matrix_data_type, matrix_shape):
    return numpy.frombuffer(matrix_bytes, dtype=matrix_data_type).reshape(matrix_shape)
