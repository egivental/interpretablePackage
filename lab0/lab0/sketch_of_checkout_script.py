#!/usr/bin/python

import sys   # for exit()
import commands
project = sys.argv[1]
logins = []
sf = open("/homes/courses/master-setup/Classlists/cs106S19.txt", "r")
logins = logins + sf.read().rstrip("\n").split("\n")
sf.close()

for stu in logins:

    destination_cmd = "mkdir " + stu + "&& cd " + stu + "&& git clone /home/courses/students/" + stu + "/git-cs106/" + project + ".git"	
    result = commands.getstatusoutput(destination_cmd)
        
    if result[0] != 0:
        print "Command " +  destination_cmd + " failed: " + result[1]
