#! /usr/bin/env python

import sys
import glob
import re
def getNumberFrequency():
	temp_list = []
	main_dict = {}
	dict={}

	with open("areaCodes.txt","r") as fptr:
		lines = fptr.readlines()
		for i in lines:
			list = re.sub(r'[!.,;?"-]',' ',i).split()
			temp_list.append(list[1])
			temp_list.append("0")
			main_dict[list[0]] = temp_list
			temp_list=[]
			dict[list[1]] = 0
	#print main_dict
	with open("phoneNumbers.txt","r") as fptr2:
		lines = fptr2.readlines()
		for line in lines:
			k = re.sub(r'[!.,;?"-()]',' ',line).split()
			tmp_var =  main_dict[k[0]][1]
			tmp_var = int(tmp_var) + 1
			main_dict[k[0]][1] = tmp_var
			
	for keys,values in main_dict.items():
		state = values[0]
		if state in dict:
			tmp = dict[state]
			dict[state] = int(values[1]) + int(tmp) 	

	with open("frequency.txt","w") as fptr:
		new = "\n"
		space = "        "
		fptr.write("State"+space+"Count"+new)
		fptr.write("------------------------------"+new)
		for key,value in dict.items():	
			fptr.write(str(key)+space+str(value)+new)


def getNameScores():
	tot=0
	tot1=0
	list_name=[]
	dict_names={}
	dict = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,
'T':20,'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26}
	lists = []
	with open("names.txt","r") as fptr:
		lines = fptr.readlines()
		#lists.append(lines)
		for i in lines:
			list = re.sub(r'[!.,;?"]',' ',i).split()

	for i in list:
		dict_names[i] = 0;
		for k in range(len(i)):	
			temp = dict[i[k]] 
			tot += temp
		dict_names[i] = tot
		tot1 =+tot 
	print "sum of all the names: ",tot1


		


def main(argv):
	getNameScores()
	getNumberFrequency()
	

if __name__=='__main__':
	 main(sys.argv[1:])
