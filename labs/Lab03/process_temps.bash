#! /bin/bash
#$Author: ee364a09 $
#$Date: 2014-02-04 13:40:24 -0500 (Tue, 04 Feb 2014) $
#$Revision: 64799 $
#$HeadURL: svn+ssh://ece364sv@ecegrid-lnx/home/ecegrid/a/ece364sv/svn/S14/students/ee364a09/Lab03/process_temps.bash $
#$Id: process_temps.bash 64799 2014-02-04 18:40:24Z ee364a09 $

Num_Params=$#
Param_Values=$@

if (($Num_Params!=1))
then
    echo "Usage: process_temps.bash <input file>"
    exit 1
fi

if [ ! -r $1 ]
then 
    echo "Error: $1 is not a readable file."
    exit 1
fi

while read line 
do
    ln_arr=($line)
    k=0
    sum=0
    cnt=0

    if (($start))
    then
        temp=$(echo $ln_arr | cut -d' ' -f1)

        for i in "${ln_arr[@]}"
        do
            if (($k))
            then 
                let sum=$i+sum
                let cnt=1+cnt       
            else
                k=1
            fi    
               
        done

        let average_temp=$sum/$cnt
        echo "Average temperature for time $temp was $average_temp C."


    else 
        start=1    
    fi

    

done < $1

exit 0
