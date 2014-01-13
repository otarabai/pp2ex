#!/usr/bin/env python
import cgi
import subprocess
import sys
import os
import random

#content type enables browser output
print "Content-Type: text/html\r\n\r"

#redirect error to browser output (for faster debugging)
sys.stderr = sys.stdout

#read data
form = cgi.FieldStorage()
upload = form['sequence']

sequence_input = upload.value

result = subprocess.check_output(["python", "../../pp2ex/final_web.py"], shell=False,stderr=subprocess.STDOUT)
#print results
print "%s" % result