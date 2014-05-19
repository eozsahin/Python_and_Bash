#! /usr/bin/env python

import cypher
import sys


def main(argv):
	s = ""
	enc = ""
	mode = argv[2]
	if len(argv) != 3:
		print "Usage: encryptor.py <input_file_name> <password> <mode>"
		exit(1)
		
	elif mode != "E" and mode != "D" and mode != "C":
		print "error: invalid mode"
		exit(3)

	else:
		try:
			cypher.is_valid_password(argv[1])
		except ValueError:
			print "Invalid password"
			exit(3)
		try:
			with open(argv[0],"r") as tmp_file:
		    		lines = tmp_file.readlines()
			   	for i in lines:
					i = cypher.strip_invalid_characters(i)
					if(argv[2] == "E"):
						try:
							enc = cypher.vign_encrypt(i,argv[1])
		 				except ValueError,x:
							print x
							exit(3)
						print enc
					elif(argv[2] == "D"):
						try:
							enc = cypher.vign_decrypt(i,argv[1])
		 				except:
							print "couldn't decrypt the file"
							exit(3)
						print enc
					elif(argv[2] == "C"):
						try:
							enc = cypher.strip_invalid_characters(i,argv[1])
		 				except:
							print "couldn't decrypt the file"
							exit(3)
						print enc
		except IOError:
			print "the ",argv[0]," is not readable"
			exit(3)
			


if __name__=='__main__':
    main(sys.argv[1:])
