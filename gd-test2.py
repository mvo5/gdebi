#!/usr/bin/env python

from qt import *
from kdeui import *
from kdecore import *
from GDebi.GDebiKDE import *
from kparts import konsolePart
import os,sys,subprocess

class SomeDialog(GDebiKDEDialog):
  def __init__(self,parent=None):
    GDebiKDEDialog.__init__(self,parent)
    self.makeAnotherWindow()
    	    
  def installButtonClicked(self):
    print "nazdar"
    
  def makeAnotherWindow(self):
    self.new = GDebiKDEInstall()
    self.new.konsoleFrame.show()
    #self.new.konsole.startProgram('ls',['-la'])
    self.new.show()
    self.letsSubprocess()
  def letsSubprocess(self):
    cmd = ["find","/","-name","\"root\""]
    self.findapp = subprocess.Popen(cmd).stdout
    while True:
      try:
        char = self.findapp.read()
        print char
      except AttributeError:
	pass
app = KApplication(sys.argv,"gd-test")
gdebi = SomeDialog()
app.setMainWidget(gdebi)
gdebi.show()
app.exec_loop()
