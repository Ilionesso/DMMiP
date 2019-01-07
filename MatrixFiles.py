import numpy

matrixAfilename = "inputMatrixA.txt"
matrixBfilename = "inputMatrixB.txt"
outputFilename = "outputMatrix.txt"
resourceFolderName = "resources/"


def readMatrix(filename):
	return numpy.genfromtxt(resourceFolderName+filename, dtype="i")


def readMatrixA():
	return readMatrix(matrixAfilename)


def readMatrixB():
	return readMatrix(matrixBfilename)


def saveMatrix(matrix, filename=outputFilename, fmt="%1i"):
	numpy.savetxt(resourceFolderName + filename, matrix, fmt)
