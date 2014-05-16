#!/bin/sh

host=`cat machine_list`;
file="/home/work/odp/log/open/open.log.2014051406";

user="sunhaowen";
password="";

if [ -d log ]; then :; else mkdir log; fi
cd log;

for i in $host
do
     if [ -d $i ]; then :; else mkdir $i; fi
     cd $i;
     sshpass -p "${password}" scp ${user}@${host}:${file} .
     cd ..
done