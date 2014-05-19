#! /usr/bin/env python

import sys
import os
import math
import string


global_cnt = 0
global_dict = {}


for lowercase in string.uppercase:
	global_dict[lowercase] = global_cnt
	global_cnt += 1
for uppercase in string.lowercase:
	global_dict[uppercase] = global_cnt
	global_cnt += 1
for num in string.digits:
	global_dict[num] = global_cnt
	global_cnt += 1
global_dict[' '] = 62

def strip_invalid_characters(s):
	out = ""
	for chars in s:
		if chars in global_dict:
			out = str(out) + str(chars)

	return out

def is_valid_password(s):
	for i in s:
		if i not in global_dict:
			return False
	return True

def vign_encrypt(message,password):
	encrypted_char = ""
	pass_cnt = 0
	res = ""
	if is_valid_password(password) == False:
		raise ValueError("bad password")
	else:
		
		for chars in message:
			if chars not in global_dict:
				raise ValueError("invalid input")
			else:
				tmp = (global_dict[chars] + global_dict[password[pass_cnt]]) % 63
				for keys in global_dict.keys():
					if global_dict[keys] == tmp:
						encrypted_char = str(keys)
				res = str(res) + str(encrypted_char)  

			pass_cnt += 1

			if pass_cnt == len(password):
				pass_cnt = 0 
			
		
	return res	


def vign_decrypt(message,password):
	encrypted_char = ""
	pass_cnt = 0
	res = ""
	if is_valid_password(password) == False:
		raise ValueError("bad password")
	else:
		
		for chars in message:
			if chars not in global_dict:
				raise ValueError("invalid input")
			else:
				tmp = (global_dict[chars] - global_dict[password[pass_cnt]]) % 63
				for keys in global_dict.keys():
					if global_dict[keys] == tmp:
						encrypted_char = str(keys)
				res = str(res) + str(encrypted_char)  

			pass_cnt += 1

			if pass_cnt == len(password):
				pass_cnt = 0 
	return res	

	
		

