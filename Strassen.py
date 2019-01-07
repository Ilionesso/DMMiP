import numpy
from math import ceil, log

from tools.MatrixFiles import readMatrixA, readMatrixB, saveMatrix

leafsize = 128
matrixFileNameA = "inputMatrixA.txt"
matrixFileNameB = "inputMatrixB.txt"


def ikjalgorithm(A, B, n):
	C = numpy.zeros((n, n))
	for i in range(n):
		for k in range(n):
			for j in range(n):
				C[i, j] += A[i, k] * B[k, j]
	
	return C

def flatMultiplication(A, B):
	return numpy.dot(A, B)



def Strassen(A, B, tam):
	# if too small return just a simple division
	if tam <= leafsize:
		return flatMultiplication(A, B)
	
	# sub-matrix size
	newTam = tam // 2
	
	print (tam)
	
	# dividing the matrices in 4 sub-matrices
	a11 = A[0:newTam, 0:newTam]
	a12 = A[0:newTam, newTam:tam]
	a21 = A[newTam:tam, 0:newTam]
	a22 = A[newTam:tam, newTam:tam]
	
	b11 = B[0:newTam, 0:newTam]
	b12 = B[0:newTam, newTam:tam]
	b21 = B[newTam:tam, 0:newTam]
	b22 = B[newTam:tam, newTam:tam]
	
	# p1 = (a11+a22) * (b11+b22)
	p1 = Strassen(a11+a22, b11+b22, newTam)
	
	# p2 = (a21+a22) * (b11)
	p2 = Strassen(a21+a22, b11, newTam)
	
	# p3 = (a11) * (b12 - b22)
	p3 = Strassen(a11, b12-b22, newTam)
	
	# p4 = (a22) * (b21 - b11)
	p4 = Strassen(a22, b21-b11, newTam)
	
	# p5 = (a11+a12) * (b22)
	p5 = Strassen(a11+a12, b22, newTam)
	
	# p6 = (a21-a11) * (b11+b12)
	p6 = Strassen(a21-a11, b11+b12, newTam)
	
	# p7 = (a12-a22) * (b21+b22)
	p7 = Strassen(a12-a22, b21+b22, newTam)
	
	C = numpy.zeros((tam, tam))
	
	C[0:newTam, newTam:tam] = p3 + p5  # c12 = p3 + p5
	C[newTam:tam, 0:newTam] = p2 + p4  # c21 = p2 + p4
	
	C[0:newTam, 0:newTam] = p1 + p4 - p5 + p7  # c11 = p1 + p4 - p5 + p7
	C[newTam:tam, newTam:tam] = p1 + p3 - p2 + p6  # c22 = p1 + p3 - p2 + p6
	
	return C


def continueStrassen(p1, p2, p3, p4, p5, p6, p7, newTam):
	tam = newTam * 2
	C = numpy.empty((tam, tam))
	
	c11 = C[0:newTam, 0:newTam]
	c12 = C[0:newTam, newTam:tam]
	c21 = C[newTam:tam, 0:newTam]
	c22 = C[newTam:tam, newTam:tam]
	
	c12 = sum(p3, p4)  # c12 = p3 + p5
	c21 = sum(p2, p4)  # c21 = p2 + p4
	
	c11 = subtract(sum(p1, p4), subtract(p5, p7))  # c11 = p1 + p4 - p5 + p7
	c22 = subtract(sum(p1, p3), subtract(p2, p6))  # c22 = p1 + p3 - p2 + p6
	
	return C


def introStrassen(A, B):
	# Make the matrices bigger so that you can apply the strassen
	# algorithm recursively without having to deal with odd
	# matrix sizes
	n = A.shape[0]
	
	# nextPowerOfTwo
	m = 2 ** int(ceil(log(n, 2)))
	APrep = numpy.resize(A, (m,m))
	BPrep = numpy.resize(B, (m,m))
	CPrep = Strassen(APrep, BPrep, m)
	C = CPrep[:n, :n]
	return C


matrixA = readMatrixA()
matrixB = readMatrixB()
matrixC = introStrassen(matrixA, matrixB)
# matrixControl2 = ikjalgorithm(matrixA, matrixB, 250)
matrixControl = flatMultiplication(matrixA, matrixB)

saveMatrix(matrixC)
# saveMatrix(matrixControl2, "control2.txt")
saveMatrix(matrixControl, "control.txt")
