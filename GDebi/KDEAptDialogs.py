# -*- coding: utf-8 -*-

# This file is part of GDebi
#
# GDebi is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# GDebi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GDebi; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


import sys
import os
import subprocess
import string
import apt
import apt_pkg
from qt import *
from kdeui import *
from kdecore import *
from kfile import *

import urllib
import fcntl
import posix
import time
import thread
import re
import pty
import select

from DebPackage import DebPackage, Cache
from apt.progress import InstallProgress
from gettext import gettext as gett

from GDebiKDEInstallDialog import GDebiKDEInstallDialog
from GDebiKDEDialog import GDebiKDEDialog
from KDEAptDialogs import *

def _(str):
    return unicode(gett(str), 'UTF-8')


def utf8(str):
  if isinstance(str, unicode):
      return str
  return unicode(str, 'UTF-8')


class KDEDpkgInstallProgress(object):
    # this one is the frontend for dpkg -i
    # there is only 0/100 state for the progress bar
    
    def __init__(self, debfile, status, progress, konsole, parent):
	# an expander would be handy, sadly we don't have one in KDE3
	self.debfile = debfile
	self.status = status
	self.progress = progress
	self.konsole = konsole
	self.parent = parent
	
	# in case there was some progress left from the deps
	self.progress.setProgress(0)
    def timeoutHandler(self,signum, frame):
        # print 'Stopped waiting for I/O ', signum
        raise IOError, "Stopped waiting for I/O."

    def commit(self):
	# ui
	self.status.setText(_("Installing '%s'...") % \
				os.path.basename(self.debfile))
	# the command
	cmd = "/usr/bin/dpkg"
	argv = [cmd, "-i", self.debfile]
	(rNum,wNum) = os.pipe()
	self.child_pid = os.fork()
	
	if self.child_pid == 0:
		# we're the child, call a subprocess, wait for the exit status, use the parent Konsole fd's as stdin/stdout
		exitstatus = subprocess.call(argv,stdin=self.parent.master, stdout=self.parent.slave,stderr=subprocess.STDOUT)
		os.write(wNum,str(exitstatus))
		os._exit(0)
	else:
		self.exitstatus = -5
		while self.exitstatus < 0:
			# okay, so what we're doing now:
			# we're using the select check to see if the pipe is readable. If it is, we're reading it
			# see select(2) or select at libref for more info
			# TODO: implement error checking
			
			try:
				readable = select.select([rNum],[],[],0.001)
				if len(readable[0]) > 0:
					self.exitstatus = int(os.read(rNum,2))

			except (OSError, IOError):
				pass
			KApplication.kApplication().processEvents()
			time.sleep(0.0000001)			
		self.progress.setProgress(100)
    		self.parent.closeButton.setEnabled(True)
		
class KDEInstallProgressAdapter(InstallProgress):
    def __init__(self, progress, action, parent):
	# TODO: implement the term
	InstallProgress.__init__(self)
	self.progress = progress
	self.action = action
	self.parent = parent
	self.finished = False

    def child_exited(self,process):
	print "processExited(self):"
	print "exit status: " + str(process.exitStatus())
	self.finished = True
	self.apt_status = process.exitStatus()

	#print "child_exited: %s %s %s %s" % (self,term,pid,status)
	#se lf.apt_status = posix.WEXITSTATUS(status)
	self.finished = True
    def error(self, pkg, errormsg):
	# FIXME: display a msg
	#self.term_expander.set_expanded(True)
	pass
    def conffile(self, current, new):
	# FIXME: display a msg or expand term
	#self.term_expander.set_expanded(True)
	pass
    def startUpdate(self):
	#print "startUpdate"
	apt_pkg.PkgSystemUnLock()
	self.action.setText(_("Installing dependencies..."))
	self.progress.setProgress(0)
    def statusChange(self, pkg, percent, status):
	self.progress.setProgress(percent)
	print status # mhb debug
	#self.progress.setText(status)
    def finishUpdate(self):
	#print "finished"
	pass
    def updateInterface(self):
	try:
	    InstallProgress.updateInterface(self)
	except ValueError,e:
	    pass
	
	KApplication.kApplication().processEvents()
	time.sleep(0.0000001)
	#while gtk.events_pending():
	#gtk.main_iteration()
    def fork(self):
	self.child_pid = os.fork()
	if self.child_pid == 0:
	    os.setsid()
	    #os.environ["TERM"] = "linux"
	    os.environ["DEBIAN_FRONTEND"] = "kde"
	    os.environ["APT_LISTCHANGES_FRONTEND"] = "none"
	    os.dup2(self.parent.slave, 0)
	    os.dup2(self.parent.slave, 1)
	    os.dup2(self.parent.slave, 2)
	return self.child_pid
    
    def waitChild(self):
        while True:
            try:
                select.select([self.statusfd],[],[], self.selectTimeout)
            except Exception, e:
                #logging.warning("select interrupted '%s'" % e)
                pass
            self.updateInterface()
            (pid, res) = os.waitpid(self.child_pid,os.WNOHANG)
            if pid == self.child_pid:
                break
        return os.WEXITSTATUS(res)

class KDEFetchProgressAdapter(apt.progress.FetchProgress):
    def __init__(self,progress,label,parent):
	self.progress = progress
	self.label = label
	self.parent = parent
    def start(self):
	#print "start()"
	self.label.setText(_("Downloading additional package files..."))
	self.progress.setProgress(0)
    def stop(self):
	#print "stop()"
	pass
    def pulse(self):
	apt.progress.FetchProgress.pulse(self)
        self.progress.setProgress(self.percent)
        currentItem = self.currentItems + 1
        if currentItem > self.totalItems:
            currentItem = self.totalItems
	if self.currentCPS > 0:
	    self.label.setText(_("Downloading additional package files...") + _("File %s of %s at %sB/s" % (self.currentItems,self.totalItems,apt_pkg.SizeToStr(self.currentCPS))))
	else:
	    self.label.setText(_("Downloading additional package files...") + _("File %s of %s" % (self.currentItems,self.totalItems)))
	KApplication.kApplication().processEvents()
	return True
    def mediaChange(self, medium, drive):
        msg = _("Please insert '%s' into the drive '%s'") % (medium,drive)
        change = QMessageBox.question(None, _("Media Change"), msg, QMessageBox.Ok, QMessageBox.Cancel)
        if change == QMessageBox.Ok:
            return True
        return False
	
class CacheProgressAdapter(apt.progress.FetchProgress):
    def __init__(self, progressbar):
	self.progressbar = progressbar
    def update(self, percent):
	self.progressbar.show()
	self.progressbar.setProgress(percent)
    def done(self):
	pass

