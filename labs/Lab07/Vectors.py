#! /usr/bin/env python

import sys
import os
import math

class Vector:
	def __init__(self,elements):
		self.elements=[]
		for i in elements:
			self.elements.append(i)
	def add(self,other):
		new = []
		if (len(self.elements)  != len(other.elements)):
			raise ValueError("The vectors are not same in size")
		else:
			len_vec = len(self.elements)
			for i in range(len_vec):
				tmp = self.elements[i] + other.elements[i]
				new.append(tmp)

		return Vector(new)

	def sub(self,other):
		new = []
		
		if (len(self.elements) != len(other.elements)):
			raise ValueError("The vectors are not same in size")
		else:
			len_vec = len(self.elements)
			for i in range(len_vec):
				tmp = self.elements[i] - other.elements[i]
				new.append(tmp)
			  
		return Vector(new)
	
	def dot(self,other):
		tot = 0
		if (len(self.elements) != len(other.elements)):
			raise ValueError("The vectors are not same in size")
		else:
			len_vec = len(self.elements)
			for i in range(len_vec):
				tmp = self.elements[i] * other.elements[i]
				tot += tmp
			  
		return tot

	def scale(self, by):
		new = []

		for i in self.elements:
			new.append(int(i)*int(by))
			  
		return Vector(new)

	def extend(self,other):
		new =[]
		
		for i in self.elements:
			new.append(i)
		
		for j in other.elements:
			new.append(j)
		
		return Vector(new)

	def length(self):
		return len(self.elements)

	def distance(self,other):
		dist = 0
		length = len(other.elements)
		tot = 0
		if (len(self.elements) != len(other.elements)):
			raise ValueError("The vectors are not same in size")
		else:
		
			for i in range(length):
				tmp = (self.elements[i] - other.elements[i])**2
				tot += tmp
		
		return math.sqrt(tot) 	
		
	def at(self,i):
		return self.elements[i]
	
	def __str__(self):
		el = ""
		cnt = 0
		length = len(self.elements)
		for i in self.elements:
			
			if cnt == 0:
				el = " "+str(i)
			else:
				 el = str(el) +", " + str(i)

			cnt = cnt + 1
		tmp = "Vector["+str(length)+"]:"+str(el)
		return str(tmp)


class Vector3D(Vector):
	def __init__(self,elements):
		self.elements = []
		if len(elements) == 0:
			raise ValueError("No element is passed to Vector3D")
		else:
			for i in elements:
				self.elements.append(i)
	
	def add(self,other):	
		if len(other.elements) != 3:
			raise ValueError("Error in addition of vector3D: other vector is not size of 3")
		else:
			new_obj = Vector(self.elements).add(other)

		return Vector3D(new_obj.elements)

	def sub(self,other):
		if len(other.elements) != 3:
			raise ValueError("Error in addition of vector3D: other vector is not size of 3")
		else:
			new_obj = Vector(self.elements).sub(other)

		return Vector3D(new_obj.elements)

	
	def scale(self,by):
		new = []

		for i in self.elements:
			new.append(i*by)
			  
		return Vector3D(new)

	def extend(self,other):
		raise NotImplementedError("Cannot extend the size of a Vector3D")
		return None

	def __str__(self):
		return "Vector3D: ("+str(self.elements[0])+","+str(self.elements[1])+","+str(self.elements[2])+")"
			
		
def parseVector3D(stringVector):
	new_list = stringVector.split(",")
	return Vector3D(new_list)
	



if __name__ == "__main__":
	vec_a = Vector([2,6,1,-9.1])
	vec_b = Vector([3,2.7,0,18])
	vec_result = vec_a.add(vec_b)
	print vec_result

	vec_a = Vector3D([7.2,4.13,5])
	vec_c = Vector3D([2,2,2])
	vec_d = Vector3D([1,1,1])
	scalar = 3.1415
	vec1 = vec_a.scale(scalar)

	print vec1
	print vec1.length() #uses inheritance
	print vec_b.length()
	print vec_c.add(vec_d) #check if inheritance takes place
	print isinstance(vec_c.add(vec_d),Vector3D) #makes sure that it return a Vector3D obj
	
	#print vec1.dot(vec_b) #error check for different size

	







	
