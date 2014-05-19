#! /bin/bash
#$Author: ee364a09 $
#$Date: 2014-02-04 14:43:24 -0500 (Tue, 04 Feb 2014) $
#$Revision: 64809 $
#$HeadURL: svn+ssh://ece364sv@ecegrid-lnx/home/ecegrid/a/ece364sv/svn/S14/students/ee364a09/Lab03/sort_temps.bash $
#$Id: sort_temps.bash 64809 2014-02-04 19:43:24Z ee364a09 $

Num_Params=$#
Param_Values=$@
start=0
getMachine=1

if ((Num_Params != 1))
then
	echo "Usage: sort_temps.bash <input file>"
	exit 1
fi 


if [ ! -r $1 ]
then 
	echo "Error: $1 is not a readable file."
	exit 2
fi


if [ -e $1.unsorted ]
then
	echo "Note: removing existing file $1.unsorted"
	rm -f $1.unsorted
fi

if [ -e $1.sorted ]
then
	echo "Note: removing existing file $1.sorted"
	rm -f $1.sorted
fi
 
touch $1.unsorted
touch $1.sorted

process_temps.bash $Param_Values

while read line
do 

	k=0
	counter=0
	
	ln_arr=($line)


	if (($getMachine))
	then 
		
		m_name=($line)
		getMachine=0
	else 
		
		time=$(echo $ln_arr | cut -d' ' -f1)

		for i in "${ln_arr[@]}"
        	do

			if (($k))
			then 
				echo "${m_name[$counter]},$time,$i" >> $1.unsorted
			else 
				k=1
			fi
			let counter=counter+1
		
		done
		
	fi

	
	
done < $1

sort -t"," -k3r  -k1 $1.unsorted > $1.sorted

exit 0



