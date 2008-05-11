#!/bin/bash

file=$1
lines=`wc -l $file | cut -d ' ' -f 1`
counter=`expr $lines - 1`
errorcode=$2
ignore=$3
stepsize=$4

if [ "x$4" = 'x' ]; then
    stepsize=100
fi

echo "$file and $errorcode ignore $ignore"

./pstotext-linux-x86 -ignore $ignore "$file" > /dev/null 2>&1


while [ $? -eq $errorcode ]; do
    head -n $counter $file > $file.tmp.ps 
    echo The counter is $counter
    counter=`expr $counter - $stepsize`
    ./pstotext-linux-x86 -ignore $ignore $file.tmp.ps > /dev/null 2>&1
done
/bin/rm $file.tmp.ps

head -n `expr $counter + $stepsize + $stepsize` $file > $file.lopped
