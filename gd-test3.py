#!/usr/bin/env python
import os,subprocess

cmd = ["ls","-la"]

output = subprocess.Popen(cmd).stdout
while True:
	try:
		print output.read(1)
	except AttributeError:
		break
	