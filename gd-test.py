#!/usr/bin/env python

from qt import *
from kdeui import *
from kdecore import *
from GDebi.GDebiKDE import GDebiKDEInstall
from kparts import konsolePart
import os,sys


app = KApplication(sys.argv,"gd-test")
gdebi = GDebiKDEInstall()
app.setMainWidget(gdebi)
gdebi.show()
app.exec_loop()