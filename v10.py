#!/usr/bin/python
# Author: Kishan Bhashyam
# Last modified date: 17th August 2016
# Version: V1.00
# Purpose: This script will parse the TCNZ F5 backup v10 config and extract useful data out of it.
#
# USAGE: ./v10.py
#

import re
import sqlite3
import sys

#SOME VARIABLES DECLARED
seenrule = 'false'
strings = ("pool p", "pool P")

#Table 1 Variables
F5_db = '/..../....../F5conf/F5.sqlite3'
table_name1 = 'PoolTab'
id_column1 = 'Pool_Name'
id_column2 = 'Pool_IP'
new_field = 'my_1st_column'

conn = sqlite3.connect(F5_db)
print "Opened database successfully";
cur = conn.cursor()

#Create Table1 if does not exist already, else delete contents.
cur.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf}, {nf1})'\
        .format(tn=table_name1, nf=id_column1, nf1=id_column2))
cur.execute('DELETE FROM {tn}'\
        .format(tn=table_name1))

#Call BigIP Conf File
File = open("/..../....../F5conf/unzip/config/bigip.conf", "r")

#Read File from desired string
for line in File:
        if line.startswith (strings):
                re.match("(^pool p)", line, re.IGNORECASE)
                a = line.lstrip("pool p")
                ONE = a[:-2]
#               print
#               print "Pool Name:", ONE

#ALL Pool Names
                for line in File:
                        if re.match("(^pool p)", line, re.IGNORECASE):
                                a = line.lstrip("pool p")
                                ONE = a[:-2]
#                               print
#                               print "Pool Name:", ONE
#                               cur.execute("INSERT INTO PoolTab (`Pool_Name`) VALUES (?)", (ONE, ));
#      
#POOL MEMBER IP Regex
                        if re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line):
                                if seenrule == 'false':
                                        x = line.lstrip("members ")
                                        sep = ':'
                                        y = x.split(sep, 1)[0]
#                                       print y
                                        cur.execute("INSERT INTO PoolTab (`Pool_Name`, `Pool_IP`) VALUES (?,?)",(ONE, y));
#                                       cur.execute("INSERT INTO PoolTab (`Pool_IP`) VALUES (?)",(y, ));

                        if re.match("(^rule )", line):
                                seenrule = 'true'


conn.execute("VACUUM")
conn.commit()
conn.close()
print "Pool Table created and stored successfully";
#######################-----------DATABASE ONE [pool_db] DONE-----------#######################

#Table 2 Variables

virtual_db = '/..../....../F5conf/F5.sqlite3'
table_name2 = 'VirTab'
id_column1 = 'Virtual_Name'
id_column2 = 'Virtual_IP'
new_field = 'my_1st_column'

conn = sqlite3.connect(virtual_db)
#print "Opened database successfully";
cur = conn.cursor()

#Create Table2 if does not exist already, else delete contents.
cur.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf}, {nf1})'\
        .format(tn=table_name2, nf=id_column1, nf1=id_column2))
cur.execute('DELETE FROM {tn}'\
        .format(tn=table_name2))

#Call BigIP Conf File
File = open("/..../....../F5conf/unzip/config/bigip.conf", "r")

#Read File from desired string
for line in File:
        if line.startswith (strings):

#ALL Virtual Names
                for line in File:
                        if re.match("(^virtual v)", line):
                                b = line.lstrip("virtual v")
                                TWO =  b[:-2]
#                               print "Virtual Name: ", TWO
#                               cur.execute("INSERT INTO VirTab (`Virtual_Name`) VALUES (?)",(TWO, ));

#ALL Virtual IPs
                        if re.match("(\s{,4}destination\s)", line):
                                c = line.lstrip("destination ")
                                THREE = c.split(':', 1 )[0]
#                               print "Virtual IP  : ", THREE
#                               print
#                               cur.execute("INSERT INTO VirTab (`Virtual_IP`) VALUES (?)",(THREE, ));
                                cur.execute("INSERT INTO VirTab (`Virtual_Name`, `Virtual_IP`) VALUES (?,?)",(TWO, THREE));

conn.execute("VACUUM")
conn.commit()
conn.close()
print "Virtual Table created and stored successfully";
#######################-----------DATABASE ONE [virtual_db] DONE-----------#######################
######END
########OF
###SCRIPT
