#! /bin/bash
#$Author: ee364a09 $
#$Date: 2014-01-28 15:09:06 -0500 (Tue, 28 Jan 2014) $
#$Revision: 64212 $
#$HeadURL: svn+ssh://ece364sv@ecegrid-lnx/home/ecegrid/a/ece364sv/svn/S14/students/ee364a09/Lab02/summarize_expr.bash $
#$Id: summarize_expr.bash 64212 2014-01-28 20:09:06Z ee364a09 $

Num_Params=$#
Param_Vals=$@

if (($Num_Params < 2))
then 
	echo "Usage: summarize_expr.bash <output file > <input file 1 > [input fil 2] ... [input file N]"
	exit 1
fi

./collect_expr.bash $Param_Vals
if (($?>0))
then
	echo "collect_expr.bash failed to run"	
	exit 1
fi


while read line 
do 
	ln=$line 
	username=$(echo $ln | cut -d' ' -f1)
	sum=$(echo $ln | cut -d' ' -f7)
	average=$(echo $ln | cut -d' ' -f8)
	  
	echo "$username $sum $average" 
	
done < $1

exit 0

