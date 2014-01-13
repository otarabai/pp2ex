#!/usr/bin/env python
import cgi
import subprocess
import sys
import os
import random

#content type enables browser output
print "Content-Type: text/html\r\n\r"

#redirect error to browser output (because of missing read log permission)
sys.stderr = sys.stdout

#read data
form = cgi.FieldStorage()
upload = form['sequence']

#path for file
file = os.path.abspath(str(random.getrandbits(64)) + ".arff")

#write data to file
file_data = upload.value
fp = open(file,'wb')
fp.write(file_data)
fp.close()

#eval data
#result = subprocess.check_output(['java', '-jar', 'ppg9.jar', file])
result = file;
#delete file
if os.path.isfile(file):
        os.remove(file)

#print results
print "%s" % result