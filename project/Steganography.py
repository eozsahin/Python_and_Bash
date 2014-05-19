#!/usr/bin/env python

import sys
import os
import math
from PIL import Image
import cypher

class Steganography:
	def __init__(self,img,string):
		"""
		Constructor for the Steganography object. It accepst image name and the embedded string		
		"""
		self.img = img
		self.string = string
	def __isValid(self):
		"""
		Validating the string that if it is possible to fit inside the image. It returns True if possible and False otherwise.	
		"""
		#get the size of the image
		w,h = Image.open(str(self.img)).size
		image_size = w*h
		str_size = len(self.string)

		#check if the string will fit in the image
		if (8*str_size > image_size):
			return False
		else:
			return True

	def embedStr(self,style,key):
		"""
		This method first encrypt the message by vigenere encryption and embeds the given string into a specified image. It returns True if everything went normal. If an error occured 	during the process it returns false and gives out an error message.
		"""

		#variable declarations
		pix_list = []
		tmp_list = []	
		str_list = []
		byte_array = []
		tmp = 0

		#check if string is valid to embed
		if(self.__isValid() == True):
			enc_message = cypher.vign_encrypt(self.string,key) #encrypt message
			s = bytearray(enc_message+"^")

			byte_array = [ bin(c) for c in s] #get the binary value of the message
	
			#open the image and get the pixel values as well as height and width of it
			width,height = Image.open(self.img).size
			im = Image.open(self.img)
			pix = im.load()

			#if the specified direction is vertical
			if(style == "vertical"):
				#print "vertical embedding is selected"
				self.dir = "V"
				#get the pixel values and store them in a list with specified direction
				for w in range(width):
					for h in range(height):
				   		pix_list.append(bin(pix[w,h]))
				
				#zero pad the byte_array and the list of pixel values
				tmp_list = [list(i.split('b')[1].rjust(8,'0')) for i in pix_list]
				byte_array = [list(x.split('b')[1].rjust(8,'0')) for x in byte_array]
				
				#embedd the bits of the message into the LSB of the byte in the image 
				z = 0
				for bit in byte_array:
					for i in range(8):
						tmp_list[z][7] = bit[i]
						z = int(z) +1
				#change format	
				tmp_list = [ int("".join(i),2) for i in tmp_list]
				
				#with the new image bytes form a new image
				im2 = Image.new(im.mode,im.size)
				pix2 = im2.load()
				cnt = 0
				#place the bytes in the picture
				for w in range(width):
					for h in range(height):
						pix2[w, h] = tmp_list[cnt]
						cnt  = int(cnt) + 1

			else:
				#embed the string in the horizontal direction
				#print "horizontal embedding is selected."
				self.dir = "H"
				#get the pixel values of the image with horizontal direction
				for h in range(height):
					for w in range(width):
				   		pix_list.append(bin(pix[w,h]))
			   #store them in the tmp_list and adjust data
				tmp_list = [list(i.split('b')[1].rjust(8,'0')) for i in pix_list]
				byte_array = [list(x.split('b')[1].rjust(8,'0')) for x in byte_array]

				#embed the bits in the pixels LSB value 
				z = 0
				for bit in byte_array:
					for i in range(8):
						tmp_list[z][7] = bit[i]
						z = int(z) +1
				#these are the new list that contain the new pixel values including the message inside
				tmp_list = [ int("".join(i),2) for i in tmp_list]
			
				#open a new image and place the pixels
				im2 = Image.new(im.mode,im.size)
				pix2 = im2.load()
				cnt = 0
				for h in range(height):
					for w in range(width):
						pix2[w, h] = tmp_list[cnt]
						cnt  = int(cnt) + 1
		
			#save the image new image
			pic_name = "embedded"+str(self.img)
			pic_name1 = "embedded_1"+str(self.img)
			self.emb_img_name = pic_name
			im2.save(pic_name)
                    
		else:
			print "Not valid to Embed"
			return False
			exit(1)

		return True

	def decodeStr(self,key):
		"""
		Given the encryption key, it extracts the embedded message in an image with specified key. It returns the string with decrypting the message.
		"""
		#variable declarations
		pix_list = []
		#open image and get width and height, pixels
		im = Image.open(self.emb_img_name)
		pix = im.load()
		width,height = Image.open(self.emb_img_name).size
	
		#with the specified direction get the current pixel values
		if(self.dir == "V"):
			#print "decoding in vertical fashion"
			for w in range(width):
				for h in range(height):
				   	pix_list.append(bin(pix[w,h]))
		else:
			#print "deconding in horizontal fashion"
			for h in range(height):
				for w in range(width):
				   	pix_list.append(bin(pix[w,h]))
		#store the pixels with adjusted values
		tmp_list = [list(i.split('b')[1].rjust(8,'0')) for i in pix_list]
		
		#variable declarations
		tot_str = ""
		byte = ""
		cnt = 0
		flag = 1 
		
		#obtain the image, recieve byte and check if it is valid and not the end char which is '^'
		while (flag == 1):
			for i in range(8):
				bit = tmp_list[cnt][7]
				cnt = int(cnt) + 1
				byte =  byte + str(bit) 
			if(int(byte,2) == 94):
				flag = 0
			if(int(byte,2) < 32 or int(byte,2) > 122):
				raise ValueError("Input string contains random symbols!")
			tot_str = tot_str + chr(int(byte,2)) 
			byte = ""

		return cypher.vign_decrypt(tot_str[:-1],key) #decrypt message and return

	def resetImg(self):
		"""
		This method sets all the LSB of pixels to zero for protection
		"""
		#open the embedded image and get height and width values
		pix_list = []
		im = Image.open(self.emb_img_name)
		width,height = Image.open(self.emb_img_name).size
		pix = im.load()
		#get the pixel values in a list
		pix_list=list(im.getdata())

		#get the binary value and add padding zeros
		tmp_list = [list(bin(i).split('b')[1].rjust(8,'0')) for i in pix_list]
		
		#sets all the LSB to zero
		for i in tmp_list:
			i[7] = "0"
		
		#join and make base conversion		
		tmp_list = [int("".join(i),2) for i in tmp_list] 
		im2 = Image.new(im.mode,im.size)
		pix2 = im2.load()
		
		#change the pixel values and overwrite
		cnt = 0		
		for w in range(width):
			for h in range(height):
				pix2[w,h] = tmp_list[cnt]
				cnt = int(cnt) + 1
		im2.save(self.emb_img_name)


