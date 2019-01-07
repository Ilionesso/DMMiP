import json

import numpy

from MatrixFiles import readMatrixA
from KafkaProducer import init_kafka_producer, publish_message


matrix = readMatrixA()
matrix_data_type = matrix.dtype.name
matrix_shape = matrix.shape


json_dump = json.dumps({'matrix': matrix.tobytes(), 'shape': matrix_shape, 'data_type': matrix_data_type})

producer = init_kafka_producer()
publish_message(producer, 'test', json_dump)


def encode_matrix(matrix):
    return matrix.tobytes()


def decode_matrix(matrix_bytes, matrix_data_type, matrix_shape):
    return numpy.frombuffer(matrix_bytes, dtype=matrix_data_type).reshape(matrix_shape)
