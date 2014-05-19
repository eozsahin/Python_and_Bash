#! /bin/bash

files=$(find | grep .*\.txt$)
space="    "

cnt=0
for file in $files
do
	echo $file
	while read line
	do
		ln=$line
		course_id=$(echo $ln | cut -f1 -d-)
		prelab=$(echo $ln | cut -d' ' -f2)
		lab=$(echo $ln | cut -d' ' -f3)
		echo $course_id,$prelab,$lab
	
		mv $file points$course_id.txt 
		points$course_id.txt < $prelab+$lab
	done < $file
	let cnt=cnt+1
done 

echo "The total number of students: $cnt"

exit 0
