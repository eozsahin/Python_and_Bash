#! /bin/bash
#$Author: ee364a09 $
#$Date: 2014-01-28 15:09:30 -0500 (Tue, 28 Jan 2014) $
#$Revision: 64213 $
#$HeadURL: svn+ssh://ece364sv@ecegrid-lnx/home/ecegrid/a/ece364sv/svn/S14/students/ee364a09/Lab02/collect_expr.bash $
#$Id: collect_expr.bash 64213 2014-01-28 20:09:30Z ee364a09 $

Num_Params=$#
Param_Vals=$@
x=$Num_Params
output=$1


if (($Num_Params < 2))
then 
	echo "Usage: collect_expr.bash <output file > <input file 1 > [input fil 2] ... [input file N]"
	exit 1;
elif [ -e ./$1 ]
then 
	echo "error: output file $1 already exists"
	exit 2;
fi

touch $output


for (( I=$Num_Params; I>1;I--))
do    
	if [ ! -r ./$2 ]
	then 
		echo "error: input file $1 is not readable!"
		exit 2
	fi

	while read line 
	do 
		ln=$line 
		username=$(echo $ln | cut -d' ' -f1)
		data_1=$(echo $ln | cut -d' ' -f2)
	    	data_2=$(echo $ln | cut -d' ' -f3)
	    	data_3=$(echo $ln | cut -d' ' -f4)
		data_4=$(echo $ln | cut -d' ' -f5)
	    	data_5=$(echo $ln | cut -d' ' -f6)
		
		let sum=$data_1+$data_2+$data_3+$data_4+$data_5
		let average=$sum/5
	
		echo "$username $data_1 $data_2 $data_3 $data_4 $data_5 $sum $average" >>$output
	
	done < $2
	shift	 
done 




exit 0 
