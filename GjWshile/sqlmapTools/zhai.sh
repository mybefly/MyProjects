#!/bin/bash
cd /Users/zhaichuang/Downloads/sqlmapproject-sqlmap-1c737d7
pwd
int=1
for ((i=1;i<=208;i++))
do      
        shell= python sqlmap.py -u "`awk 'NR==vint {print $(NR-1)}' vint=$int  dlut4.csv `" --data "`awk 'NR==vint {print $NR}' vint=$int dlut4.csv`" --batch >/Users/zhaichuang/Desktop/log.txt
        echo $shell
        let int=$int+1
done
