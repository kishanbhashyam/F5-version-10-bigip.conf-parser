#!/usr/bin/python
# Author: Kishan Bhashyam
# Last modified date: 17th August 2016
# Version: V1.00
# Purpose: This script will parse the F5 backup v10 config and extract useful data out of it.
#
# USAGE: ./v10.py
#


import re
import sqlite3

#Creating SQL TABLE
sqlite_file = '/F5conf/F5ver10.sqlite3'
table_name1 = 'table1'
id_column = 'Virtual_Name'
new_column1 = 'Virtual_IP'
new_column2 = 'Pool_Name'
new_column3 = 'Pool_IP'
new_field = 'my_1st_column'
seenrule = 'false'

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf}, {nf1}, {nf2}, {nf3})'\
        .format(tn=table_name1, nf=id_column, nf1=new_column1, nf2=new_column2, nf3=new_column3))

cur.execute('DELETE FROM {tn}'\
        .format(tn=table_name1))

File = open("/F5conf/unzip/config/bigip.conf", "r")
for i in xrange(2348):
        File.next()

#ALL Pool Names
for line in File:
        if re.match("(^pool p)", line, re.IGNORECASE):
                a = line.lstrip("pool p")
                ONE = a[:-2]
#                print
#                print "Pool Name:", ONE

#POOL MEMBER IP Regex
	if re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line):
		if seenrule == 'false':
			x = line.lstrip("members ")
			sep = ':'
			y = x.split(sep, 1)[0]
#			print y
			cur.execute("INSERT INTO table1 (`Pool_Name`, `Pool_IP`) VALUES (?,?)",(ONE, y));

	if re.match("(^rule )", line):
		seenrule = 'true'
		
#ALL Virtual Names
	if re.match("(^virtual v)", line):
               b = line.lstrip("virtual v")
               TWO =  b[:-2]
#               print "Virtual Name: ", TWO	

	
#ALL Virtual IPs
	if re.match("(\s{,4}destination\s)", line):
                c = line.lstrip("destination ")
                THREE = c.split(':', 1 )[0]
#                print "Virtual IP  : ", THREE
#                print	
		cur.execute("INSERT INTO table1 (`Virtual_Name`, `Virtual_IP`) VALUES (?,?)",(TWO, THREE));

conn.execute("VACUUM")
conn.commit()
conn.close()
print "Result Printed into database /home/t816874/F5conf/F5ver10.sqlite3"
