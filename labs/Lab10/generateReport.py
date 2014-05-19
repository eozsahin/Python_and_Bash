#!/usr/bin/env python

import re
import sys


def printOutput(outfile,dict):
	
	with open(outfile,"w+") as fptr:
		fptr.write("<students>\n")
		for keys,values in dict.items():
			st_str = "  <student "
			st_str = st_str +  "name=\""+str(values[0])+"\"" + " id=\""+str(keys)+"\">" 
			values.pop(0)
			fptr.write(str(st_str)+"\n")
			for val in values:
				if int(val[1]) > int(90):
					tmp = "A"
				elif int(val[1]) > 80:
					tmp = "B"
				elif int(val[1]) > 70:
					tmp = "C"
				elif int(val[1]) > 60:
					tmp = "D"
				else:
					tmp = "F"
				

				cl_str = "    <ECE"+str(val[0])+ " score=\""+str(val[1])+ " grade=\""+str(tmp)+"\">" 
				fptr.write(cl_str+"\n")
			fptr.write("  </student>\n")



def openFile(filename):
	dict_class = {}
	list_of_students = []
	list_of_classes = []
	tmp_list = []
	
	valid = 1 
	try:
		with open(filename,"r") as fptr:
			for line in fptr:
				col = line.split(',')
				#print col
				new = col[0].split(':')
				found = re.findall("(<)(\w+)(>)(\w+)(\s)(\w+)",new[0]) 
	
				if(len(found) > 0):
					st_id = found[0][1]
					st_name = found[0][3] + " " + found[0][5]
					#print st_name
					check = re.findall("(\[)(\d+)(:)(\d+)(\])(</)"+st_id,col[len(col)-1])
					#print check
					if (len(check) > 0):
						list_of_classes.append(st_name)
						for i in col:
							classes = re.findall("(\[)(\d+)(:)(\d+)(\])",i) 
							class_name = classes[0][1]
							class_score = classes[0][3]
							tmp_list.append(class_name)
							tmp_list.append(class_score)
							list_of_classes.append(tmp_list)
							tmp_list = []
						dict_class[st_id] = list_of_classes
						list_of_classes = []
		return dict_class 
	except:
		print "Error: Couldn't read "+filename
		exit(2)
		    


def main(argv):
	dict = {}
	if len(argv) == 2:
		list = []
		input_file = argv[0]
		output_file = argv[1]
		dict = openFile(input_file)
		printOutput(output_file,dict)
	else: 
		print "check usage"
		exit(1)

    
if __name__=='__main__':
    main(sys.argv[1:])
