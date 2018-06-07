#!/bin/bash
tiao=1
for ((i=1;i<=208;i++));
do
echo "****************************$tiao*******************************"
#awk -F "," 'NR==vtiao {print $2}' vtiao=$tiao dlut4.csv
# `awk -F "," 'NR==vtiao {print "python sqlmap.py -u "$1," --data",$2," --batch"}' vtiao=$tiao dlut4.csv`
`awk -F "," 'NR==vtiao {print "python sqlmap.py -u "$1," --data",$2," --batch"}' vtiao=$tiao dlut5.csv `
echo "=========================================================="
let tiao+=1;
done
