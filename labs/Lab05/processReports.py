#!/usr/bin/env python

import sys
import re
import glob

def strainSummaryReport(data):
	dict_cost = data[3]	
	dict_unit = data[2]
    	n_line="\n"
	space = "             "
    	with open("strainSummaryReport.txt","w") as fptr:
        	fptr.write("Virus Name            Total Units         Total Spending"+n_line)
        	fptr.write("--------------------------------------------------------"+n_line)

		for un in dict_unit:
			for c in dict_cost:
				if (str(un) == str(c) ):
            				fptr.write( str(un) +space +str(dict_unit[un])+space+str(dict_cost[c])+ n_line)
	




def userSummaryReport(data,user):
	dict_cost = data[0]	
	dict_unit = data[1]
    	n_line="\n"
	space = "             "
    	with open("userSummaryReport.txt","w") as fptr:
        	fptr.write("User Name            Total Units         Total Spending"+n_line)
        	fptr.write("--------------------------------------------------------"+n_line)

        	for u in user:
			for un in dict_unit:
				for c in dict_cost:
					
					if ((str(u) == str(un)) and (str(u) == str(c)) ):
						print "ok"
            					fptr.write( str(user[u]) +space +str(dict_unit[un])+space+str(dict_cost[c])+ n_line)
	



def getUserCostList(report_set):
	dict_cost={} #{USER:COST}
	dict_unit={} #{USER:UNIT}
	dict_virus_unit={} #{VIR:UNIT}
	dict_virus_cost={} #{VIR:UNIT}
	cnt = 0
	total_unit = total_cost = 0
	list_dicts=[]
	list=[]
	
	for report in report_set:
		with open(report,"r") as tmp_rep:
			lines = tmp_rep.readlines()
			temp = lines[0].strip().split(":")
			user_id = temp[1]
			#print user_id		
			for i in lines:
				cnt +=1
				if(cnt > 4):
					thisline = re.sub(r'[.!,;?]', ' ', i).split()
					unit = thisline[2]
					total_unit  = int(total_unit) + int(unit)
					tmp = thisline[3]
					tmp = tmp.split("$")
					cost = tmp[1]
					total_cost = int(total_cost)+int(cost)
					virus =thisline[1] 
					
					if virus in dict_virus_unit:
						dict_virus_unit[virus] += total_unit
						dict_virus_cost[virus] += total_cost
					else: 
						dict_virus_unit[virus] = total_unit
						dict_virus_cost[virus] = total_cost
						
			if user_id in dict_cost:
				dict_cost[user_id] += total_cost
				dict_unit[user_id] += total_unit
			else:
				dict_cost[user_id] = total_cost
				dict_unit[user_id] = total_unit
					
				
		cnt = 0
	return dict_cost,dict_unit,dict_virus_unit,dict_virus_cost

def getFiles(folder):
    fileset = []
    search = '*.txt'
    s = folder + "/" + search
    for f in glob.glob(s):
        fileset.append(f)
    return fileset

def getUsers():
	cnt = 0
	dict={}
	with open("users.txt","r") as fptr:
		lines = fptr.readlines()
		for i in lines:	
			if (cnt > 2):
                		thisline = re.sub(r'[.!,;?]', ' ', i).split()
				name = thisline[1] + " "+ thisline[0]
                		dict[thisline[3]] = name
			cnt +=1
	
	#print dict
	return dict
def main(argv):
	folder = "reports"
	user_dict = getUsers()
	#print user_dict
	report_set = getFiles(folder)
	list_rep = getUserCostList(report_set)
	userSummaryReport(list_rep,user_dict)
	strainSummaryReport(list_rep)



if __name__=='__main__':
    main(sys.argv[1:])
