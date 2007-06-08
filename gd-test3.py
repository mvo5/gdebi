#!/usr/bin/env python
import os,subprocess

cmd = ["sleep","100000"]

output = subprocess.Popen(cmd).stdout
print "mama"
print output