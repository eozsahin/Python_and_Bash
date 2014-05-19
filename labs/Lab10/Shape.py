#! /usr/bin/env python

import sys
import os
import math

class Shape:
		def __init__(self,elements):
			pass
		def calcBoundingBox(self):
			return ((0,0),(0,0))


class Polygon(Shape):
		def __init__(self,elements):
			self.list = []
			for i in elements:
				self.list.append(i)

		def calcBoundingBox(self):	
			minx = 1000
			miny = 1000
			maxx = 0
			maxy = 0
			for i in self.list:
				x = i[0]
				y = i[1]
				if(x > maxx):
					maxx = x
				if(x < minx):
					minx = x
				if(y > maxy):
					maxy = y
				if(y < miny):
					miny = y
			return ((minx,miny),(maxx,maxy))		

class Triangle(Polygon):
		def __init__(self,elements):
			self.list = []
			if len(elements) == 3:
				for i in elements:
					self.list.append(i)
			else: 
				raise ValueError("not traingle!")

		def calcArea(self):
			A_x = float(self.list[0][0])
			A_y = float(self.list[0][1])
			B_x = float(self.list[1][0])
			B_y = float(self.list[1][1])
			C_x = float(self.list[2][0])
			C_y = float(self.list[2][1])

			return abs(A_x*(B_y - C_y)+B_x*(C_y - A_y)+C_x*(A_y - B_y))/2

class Circle(Shape):
		def __init__(self,elem,rad):
			if float(rad) > 0:
				self.x = elem[0]
				self.y = elem[1]
				self.rad = rad
			else:
				raise ValueError("invalid Circle!")

		def calcArea(self):

			return math.pi*float(self.rad)*float(self.rad)
		
		def calcBoundingBox(self):
			return ( -1*(self.rad - self.x),  -1*(self.rad - self.y)), (self.x + self.rad,self.y + self.rad)
			









