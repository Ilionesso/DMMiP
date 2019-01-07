import random
import os
import numpy

from tools.MatrixFiles import saveMatrix

n = 512
maximal = 10
matrixFileNameA = "inputMatrixA.txt"
matrixFileNameB = "inputMatrixB.txt"


def createMatrix(filename):
	matrix = numpy.random.randint(0, maximal, size=(n, n))
	saveMatrix(matrix, filename=filename, fmt='%1i')


createMatrix(matrixFileNameA)
createMatrix(matrixFileNameB)
