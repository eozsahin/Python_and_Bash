#!/usr/bin/env python

import sys
from matrices import *

def checkIfMatrixIsValid(matrix):
	num_cols = len(matrix)
	
	if(isinstance(matrix[0],list)):
		num_row = len(matrix[0])
	

	for i in range(num_cols):
		if(isinstance(matrix[i],list)):
			if(num_row != len(matrix[i])):
				return False
		else:
			return False
	return True

def getMatrixSize(matrix):
	
	if(checkIfMatrixIsValid(matrix)):
		num_rows=len(matrix)
		num_cols=len(matrix[0])
		return (num_rows,num_cols)
	else: 
		return ()
			
def getRow(matrix,rowIndex):
	if(checkIfMatrixIsValid(matrix)):
		size = getMatrixSize(matrix)
		if(rowIndex < size[0]):
			return matrix[rowIndex]
		else:
			return []
	else:
		return []
		
def getColumn(matrix,columnIndex):
	col = []
	if(checkIfMatrixIsValid(matrix)):
		size = getMatrixSize(matrix)
		max_cols = size[0]
		if(columnIndex < max_cols):
			for i in range(max_cols):
				col.append(matrix[i][columnIndex])
			return col
		else: 
			return col
	
	else:
		return col

def transposeMatrix(matrix):
	size = getMatrixSize(matrix)
	max_rows = size[0]
	max_cols = size[1]
	outer=[]
	inner=[]
	row=[]
	
	
	if(checkIfMatrixIsValid):
		for i in range(max_cols):
			for j in matrix:
				row.append(j[i])
			outer.append(row)
			row=[]
		return outer	
	else:
		return none
		
def dotProduct(row,column):
	sum = 0
	if(len(row) == len(column)):
		for i in range(len(row)):
			temp = row[i]*column[i]
			sum += temp
		return sum
	else:
		return None

def MultiplyMatrices(matrix1,matrix2):
	k =[]
	outer=[]
	if(checkIfMatrixIsValid(matrix1) and checkIfMatrixIsValid(matrix2)):
		for i in matrix1:
			for j in matrix2:
				dp = dotProduct(i,j)
				k.append(dp)
				dp=[]
			outer.append(k)
		return outer
			
		
	else:
		return None
				

def main():

	for g in all_mat1:
		for h in all_mat2:
			r = MultiplyMatrices(g,h)
	print r
	
	
	
	
	
        
if __name__=='__main__':
    main()
	
