#!/usr/bin/env python

import re
import sys

def printOutput(filename2,list):
  

   try:
        with open(filename2,"w+") as fptr:
		fptr.write("<sensors>\n")
		for sen_val in list:
			sensor = sen_val[0][0]
			vals = sen_val[1]
			
 			sensor_str = "  <sensor"
			sensor_str = str(sensor_str) + " state=\""+str(sensor[0])+"\"" + " type=\""+str(sensor[1])+"\"" + " id=\""+str(sensor[2])+"\">"
			fptr.write(str(sensor_str)+"\n")
			for i in vals:
				fptr.write("    <val>"+str(i[0])+"</val>\n")
			fptr.write("  </sensor>\n")
			
		fptr.write("</sensors>\n")
   except:
	print "Error: Couldn't open output file"
	exit(3)

def openFile(filename):
    fin = []
    list = []
    tmp_list = []
    new_val_list = []
    try:
        with open(filename) as fptr:
            for line in fptr:
		col = line.split(':')
		sensor = col[0]
		vals = col[1].split(',')
		re_sensor = re.findall("(FL|RI|NY|NJ)(P|T|R)(\d+(-\w*)?)",sensor) 

		if len(re_sensor) > 0:
			for val in vals:
				new_val = re.findall("-?\d.?\d+",val)
				new_val_list.append(new_val)
		
			tmp_list.append(re_sensor)
			tmp_list.append(new_val_list)
	    		list.append(tmp_list)
		tmp_list = []
		new_val_list = []
		
    except:
        print "Error: Couldn't read "+filename
	exit(2)
    return list           


def main(argv):
    if len(argv) == 2:
	list = []
   	filename = argv[0]
   	filename2 = argv[1]
   	list = openFile(filename)
   	printOutput(filename2,list)
    else: 
	print "Usage: sensor_to_xml.py <input file> <output file>"
	exit(1)

    
if __name__=='__main__':
    main(sys.argv[1:])
