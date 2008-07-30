#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2005-2007 Martin Böhm
# Copyright (c) 2008 Canonical Ltd
#
# AUTHOR:
# Martin Böhm <martin.bohm@ubuntu.com>
#
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import subprocess
import string
import apt
import apt_pkg
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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

def _(str):
    return unicode(gett(str), 'UTF-8')

def utf8(str):
  if isinstance(str, unicode):
      return str
  return unicode(str, 'UTF-8')

class KDEDpkgInstallProgress(object):
    """The frontend for dpkg -i"""
    # there is only 0/100 state for the progress bar

    def __init__(self, debfile, status, progress, konsole, parent):
        # an expander would be handy, sadly we don't have one in KDE3
        self.debfile = debfile
        self.status = status
        self.progress = progress
        self.konsole = konsole
        self.parent = parent

        # in case there was some progress left from the deps
        self.progress.setValue(0)

    def timeoutHandler(self,signum, frame):
        raise IOError, "Stopped waiting for I/O."

    def commit(self):
        # ui
        self.status.setText(_("Installing '%s'...") % os.path.basename(self.debfile))
        # the command
        cmd = "/usr/bin/dpkg"
        argv = [cmd, "-i", self.debfile]
        (rNum,wNum) = os.pipe()
        self.child_pid = os.fork()

        if self.child_pid == 0:
            # we're the child, call a subprocess, wait for the exit status, use the parent Konsole fd's as stdin/stdout
            exitstatus = subprocess.call(argv,stdin=self.parent.master, stdout=self.parent.slave,stderr=subprocess.STDOUT)
            #exitstatus = subprocess.call(argv)
            os.write(wNum,str(exitstatus))
            os._exit(0)
        else:
            self.exitstatus = -5
            while self.exitstatus < 0:
                # okay, so what we're doing now:
                # we're using the select check to see if the pipe is readable. If it is, we're reading it
                # see select(2) or select at libref for more info
                # TODO: implement error checking
                while True:
                    #Read from pty and write to DumbTerminal
                    try:
                        (rlist, wlist, xlist) = select.select([self.parent.master],[],[], 0)
                        if len(rlist) > 0:
                            line = os.read(self.parent.master, 255)
                            self.parent.konsole.insertWithTermCodes(utf8(line))
                        else:
                            break
                    except Exception, e:
                        print e
                    break

                try:
                    readable = select.select([rNum],[],[],0.001)
                    if len(readable[0]) > 0:
                        self.exitstatus = int(os.read(rNum,2))
                except (OSError, IOError):
                    pass

                KApplication.kApplication().processEvents()
                time.sleep(0.0000001)
            self.progress.setValue(100)
            self.parent.closeButton.setEnabled(True)
            self.parent.closeButton.setVisible(True)
            self.parent.installationProgress.setVisible(False)
            QTimer.singleShot(1, self.parent.changeSize)

class KDEInstallProgressAdapter(InstallProgress):
    def __init__(self, progress, action, parent):
        # TODO: implement the term
        InstallProgress.__init__(self)
        self.progress = progress
        self.action = action
        self.parent = parent
        self.finished = False

    def child_exited(self,process):
        self.finished = True
        self.apt_status = process.exitStatus()
        self.finished = True

    def error(self, pkg, errormsg):
        # FIXME: display a msg
        #self.term_expander.set_expanded(True) #FIXME show konsole
        pass

    def conffile(self, current, new):
        # FIXME: display a msg or expand term
        #self.term_expander.set_expanded(True) #FIXME show konsole
        pass

    def startUpdate(self):
        apt_pkg.PkgSystemUnLock()
        self.action.setText(_("Installing dependencies..."))
        self.progress.setValue(0)

    def statusChange(self, pkg, percent, status):
        self.progress.setValue(percent)
        print status # mhb debug
        #self.progress.setText(status) #FIXME set text

    def updateInterface(self):
        # log the output of dpkg (on the master_fd) to the DumbTerminal
        while True:
            try:
                (rlist, wlist, xlist) = select.select([self.master_fd],[],[], 0)
                if len(rlist) > 0:
                    line = os.read(self.master_fd, 255)
                    self.parent.konsole.insertWithTermCodes(utf8(line))
                else:
                    break
            except Exception, e:
                print e
                break
        try:
            InstallProgress.updateInterface(self)
        except ValueError,e:
            pass

        KApplication.kApplication().processEvents()
        time.sleep(0.0000001)

    def fork(self):
        """pty voodoo"""
        (self.child_pid, self.master_fd) = pty.fork()
        if self.child_pid == 0:
            os.environ["TERM"] = "dumb"
            if not os.environ.has_key("DEBIAN_FRONTEND"):
                os.environ["DEBIAN_FRONTEND"] = "noninteractive"
            os.environ["APT_LISTCHANGES_FRONTEND"] = "none"
        return self.child_pid

    def waitChild(self):
        while True:
            try:
                select.select([self.statusfd],[],[], self.selectTimeout)
            except Exception, e:
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
        self.label.setText(_("Downloading additional package files..."))
        self.progress.setValue(0)

    def stop(self):
        pass

    def pulse(self):
        apt.progress.FetchProgress.pulse(self)
        self.progress.setValue(self.percent)
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
        #change = QMessageBox.question(None, _("Media Change"), msg, QMessageBox.Ok, QMessageBox.Cancel)
        change = KMessageBox.questionYesNo(None, _("Media Change"), _("Media Change") + "<br>" + msg, KStandardGuiItem.ok(), KStandardGuiItem.cancel())
        if change == KMessageBox.Yes:
            return True
        return False

class CacheProgressAdapter(apt.progress.FetchProgress):
    def __init__(self, progressbar):
        self.progressbar = progressbar

    def update(self, percent):
        self.progressbar.show()
        self.progressbar.setValue(percent)

    def done(self):
        pass
