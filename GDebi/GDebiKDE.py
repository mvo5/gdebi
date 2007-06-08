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
import warnings
from warnings import warn
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
import apt
import apt_pkg
from qt import *
from kdeui import *
from kdecore import *
from kparts import konsolePart,TerminalInterface
from kfile import *

import urllib
import fcntl
import posix
import time
import thread
import re
import pty

from DebPackage import DebPackage, Cache
from apt.progress import InstallProgress
from gettext import gettext as _
from GDebiKDEInstallDialog import GDebiKDEInstallDialog
from GDebiKDEDialog import GDebiKDEDialog
 
def utf8(str):
  return unicode(str, 'latin1').encode('utf-8')

class GDebiKDE(GDebiKDEDialog):
    def __init__(self,datadir,options,file="",parent = None,name = None,modal = 0,fl = 0):
	GDebiKDEDialog.__init__(self,parent,name,modal,fl)
	
	self._deb = None	
        self.setDisabled(True)

        self.cprogress = self.CacheProgressAdapter(self.PackageProgressBar)
        self._cache = Cache(self.cprogress)
        self._options = options
        # try to open the file
        if file != "" and os.path.exists(file):
            self.open(file)
        self.setEnabled(True)
	
    def open(self, file):
        try:
            self._deb = DebPackage(self._cache, file)
        except (IOError,SystemError),e:
            print "system error - open()"
            return False
        # set name
        self.setCaption(_("Package Installer - %s") % self._deb.pkgName)
        self.textLabel1_3.setText(self._deb.pkgName)

        # set description
        buf = self.DecriptionEdit
        try:
            #print self._deb["Description"] # mhb debug
            long_desc = ""
            raw_desc = string.split(utf8(self._deb["Description"]), "\n")
            # append a newline to the summary in the first line
            summary = raw_desc[0]
            raw_desc[0] = ""
            long_desc = "%s\n" % summary
            for line in raw_desc:
                tmp = string.strip(line)
                if tmp == ".":
                    long_desc += "\n"
                else:
                    long_desc += tmp + "\n"
            # do some regular expression magic on the description
            # Add a newline before each bullet
            p = re.compile(r'^(\s|\t)*(\*|0|-)',re.MULTILINE)
            long_desc = p.sub('\n*', long_desc)
            # add the <b> tag to the first line
            long_desc = re.sub(r'\n','</b>\n',long_desc,1)
            # replace all newlines by spaces
            p = re.compile(r'\n', re.MULTILINE)
            long_desc = p.sub(" ", long_desc)
            # replace all multiple spaces by
            # paragraph tags
            p = re.compile(r'\s\s+', re.MULTILINE)
            long_desc = p.sub("</p><p>", long_desc)
            # add the remaining tags
            long_desc = '<p><b>' + long_desc + '</p>'
            # write the descr string to the buffer
            buf.setText(long_desc)
        except KeyError:
            buf.set_text("No description is available")
        
        # check the deps
        if not self._deb.checkDeb():
            #self.textLabel1_3_2.set_markup("<span foreground=\"red\" weight=\"bold\">"+
            #                             "Error: " +
            #                             self._deb._failureString +
            #                             "</span>")
	    self.installButton.setText(_("&Install Package"))

            #self.button_install.set_sensitive(False)
            #self.button_details.hide()
            return

        if self._deb.compareToVersionInCache() == DebPackage.VERSION_SAME:
            #self.textLabel1_3_2.setText(_("Same version is already installed"))
            self.installButton.setText(_("&Reinstall Package"))
            #self.button_install.grab_default()
            #self.button_install.set_sensitive(True)
            #self.button_details.hide()
            return  

        # check if the package is available in the normal sources as well
        res = self._deb.compareToVersionInCache(useInstalled=False)
        if not self._options.non_interactive and res != DebPackage.NO_VERSION:
            pkg = self._cache[self._deb.pkgName]
            title = msg = ""
            
            # FIXME: make this strs better, improve the dialog by
            # providing a option to install from repository directly
            # (when possible)
            if res == DebPackage.VERSION_SAME:
                if self._cache.downloadable(pkg,useCandidate=True):
                    title = _("Same version is available in a software channel")
                    msg = _("You are recommended to install the software "
                            "from the channel instead.")
            elif res == DebPackage.VERSION_IS_NEWER:
                if self._cache.downloadable(pkg,useCandidate=True):
                    title = _("An older version is available in a software channel")
                    msg = _("Generally you are recommended to install "
                            "the version from the software channel, since "
                            "it is usually better supported.")
            elif res == DebPackage.VERSION_OUTDATED:
                if self._cache.downloadable(pkg,useCandidate=True):
                    title = _("A later version is available in a software "
                              "channel")
                    msg = _("You are strongly advised to install "
                            "the version from the software channel, since "
                            "it is usually better supported.")

            if title != "" and msg != "":
                # we should wait for the usability review to finish before setting this up
                print title
                print msg
                #msg = "<big><b>%s</b></big>\n\n%s" % (title,msg)
                #dialog = gtk.MessageDialog(parent=self.window_main,
                                           #flags=gtk.DIALOG_MODAL,
                                           #type=gtk.MESSAGE_INFO,
                                           #buttons=gtk.BUTTONS_CLOSE)
                #dialog.set_markup(msg)
                #dialog.run()
                #dialog.destroy()

        (install, remove, unauthenticated) = self._deb.requiredChanges
        deps = ""
        if len(remove) == len(install) == 0:
            deps = _("All dependencies are satisfied")
            #self.button_details.hide()
        else:
            pass
            #self.button_details.show()
        if len(remove) > 0:
            # FIXME: use ngettext here
            deps += _("Requires the <b>removal</b> of %s packages\n") % len(remove)
        if len(install) > 0:
            deps += _("Requires the installation of %s packages") % len(install)
        self.textLabel1_3_2.setText(deps)
        # set various status bits
        self.DetailsVersion.setText(self._deb["Version"])
        self.DetailsMaintainer.setText(utf8(self._deb["Maintainer"]))
        self.DetailsPriority.setText(self._deb["Priority"])
        self.DetailsSection.setText(utf8(self._deb["Section"]))
        self.DetailsSize.setText(self._deb["Installed-Size"] + " KB")

        # set filelist
        buf = self.IncFilesEdit
        buf.setText("\n".join(self._deb.filelist))

        if not self._deb.checkDeb():
	    self.buttonOk.setText(_("Install Package"))
        
        if self._deb.compareToVersionInCache() == DebPackage.VERSION_SAME:
            self.buttonOk.setText(_("Reinstall Package"))
	
    def cancelButtonClicked(self):
	self.close()
	
    def installButtonClicked(self):
        
        print "click" # mhb debug
	print self._deb.file
        # sanity check
        if self._deb is None:
            return
        # do it
        # set the window as disabled
        self.setDisabled(True)
        # if not root, start a new instance
        if os.getuid() != 0:
            os.execl("/usr/bin/kdesu", "kdesu",
                     "/home/martin/processing/soc/gdebi-kde/branch/gdebi-kde/gdebi-kde -n " + self._deb.file)
        # check if we can lock the apt database
        try:
            apt_pkg.PkgSystemLock()
        except SystemError:
            print "cannot be locked" # mhb debug
        apt_pkg.PkgSystemUnLock()
	
        self.installDialog = GDebiKDEInstall(self)
        self.installDialog.show()

        (install, remove, unauthenticated) = self._deb.requiredChanges
        if len(install) > 0 or len(remove) > 0:
            # check if we can lock the apt database
            try:
                apt_pkg.PkgSystemLock()
            except SystemError:
                #header = _("Only one software management tool is allowed to"
                           #" run at the same time")
                #body = _("Please close the other application e.g. 'Update "
                         #"Manager', 'aptitude' or 'Synaptic' first.")
                print "only one sw management tool..."
                return
            # FIXME: use the new python-apt acquire interface here,
            # or rather use it in the apt module and raise exception
            # when stuff goes wrong!
            fprogress = self.FetchProgressAdapter(installDialog.installationProgres,
                                                  installDialog.installingLabel,
                                                  installDialog)
            iprogress = self.InstallProgressAdapter(installDialog.installationProgres,
                                                    None,
                                                    installDialog.installingLabel,
                                                    None)
            errMsg = None
            try:
                res = self._cache.commit(fprogress,iprogress)
            except IOError, msg:
                res = False
                errMsg = "%s" % msg
                header = _("Could not download all required files")
                body = _("Please check your internet connection or "
                         "installation medium.")
            except SystemError, msg:
                res = False
                header = _("Could not install all dependencies"),
                body = _("Usually this is related to an error of the "
                         "software distributor. See the terminal window for "
                         "more details.")
            if not res:
                #self.show_alert(gtk.MESSAGE_ERROR, header, body, msg,
                                #parent=self.dialog_deb_install)
                print body
                
                #self.label_install_status.set_markup("<span foreground=\"red\" weight=\"bold\">%s</span>" % header)
                #self.button_deb_install_close.set_sensitive(True)
                #self.button_deb_install_close.grab_default()
		#self.statusbar_main.push(self.context,_("Failed to install package file"))
                #return 

        # install the package itself
        #self.label_action.set_markup("<b><big>"+_("Installing package file")+"</big></b>")
        dprogress = self.DpkgInstallProgress(self._deb.file,
                                             self.installDialog.installingLabel,
                                             self.installDialog.installationProgres,
                                             self.installDialog.konsole, self.installDialog)
        dprogress.commit()
        #self.label_action.set_markup("<b><big>"+_("Package installed")+"</big></b>")
        # show the button
        #self.button_deb_install_close.set_sensitive(True)
        #self.button_deb_install_close.grab_default()
        #self.label_action.set_markup("<b><big>"+_("Installation finished")+"</big></b>")
        if dprogress.exitstatus == 0:
            #self.label_install_status.set_markup("<i>"+_("Package '%s' was installed") % os.path.basename(self._deb.file)+"</i>")
            print "was installed"
        else:
            #self.label_install_status.set_markup("<b>"+_("Failed to install package '%s'") % os.path.basename(self._deb.file)+"</b>")
            #self.expander_install.set_expanded(True)
            print "was not installed"
        #self.statusbar_main.push(self.context,_("Installation complete"))
        # FIXME: Doesn't stop notifying
        #self.window_main.set_property("urgency-hint", 1)

        # reopen the cache, reread the file, FIXME: add progress reporting
        #self._cache = Cache(self.cprogress)
        self._cache = Cache()
        if self._cache._depcache.BrokenCount > 0:
            #err_header = _("Failed to completely install all dependencies")
            #err_body = _("To fix this run 'sudo apt-get install -f' in a "
                         #"terminal window.")
            #self.show_alert(gtk.MESSAGE_ERROR, err_header, err_body)
            
            print "Autsch, please report"
        self.open(self._deb.file)


    # embedded classes
    class DpkgInstallProgress(object):
        def __init__(self, debfile, status, progress, konsole, parent):
	    # an expander would be handy, sadly we don't have one in KDE3
            self.debfile = debfile
            self.status = status
            self.progress = progress
            self.konsole = konsole
	    self.parent = parent
            #self.expander = expander
            #self.expander.set_expanded(False)
        def commit(self):
            def finish_ff(self):
                #" helper "
                #self.exitstatus = posix.WEXITSTATUS(status)
                #print " finished %s %s" % (pid,status)
                #print "exit status: %s" % self.exitstatus
                #print "was signaled %s" % posix.WIFSIGNALED(status)
                self.lock.release()
            # get a lock
            self.lock = thread.allocate_lock()
            self.lock.acquire()

            # ui
            self.status.setText("<i>"+_("Installing '%s'...") % \
                                   os.path.basename(self.debfile)+"</i>")
            #self.progress.pulse()
            #self.progress.set_text("")

            # prepare reading the pipe
            #(readfd, writefd) = os.pipe()
            #fcntl.fcntl(readfd, fcntl.F_SETFL,os.O_NONBLOCK)
            #print "fds (%i,%i)" % (readfd,writefd)

            # the command
            cmd = "/usr/bin/dpkg"
            argv = [cmd, "-i", self.debfile]
            #env = ["VTE_PTY_KEEP_FD=%s"% writefd]
            print cmd
            print argv
    	    #print env
            print self.konsole

            # prepare for the fork 
	    self.child_pid = os.fork()
            if self.child_pid == 0:
                os.setsid()
                #os.environ["TERM"] = "linux"
                os.environ["DEBIAN_FRONTEND"] = "kde"
                os.environ["APT_LISTCHANGES_FRONTEND"] = "none"
                os.dup2(self.parent.slave, 0)
                os.dup2(self.parent.slave, 1)
                os.dup2(self.parent.slave, 2)
	        # we're the offspring, let's install like we should
		subprocess.Popen(argv,stdin=self.parent.master, stdout=self.parent.slave,stderr=subprocess.STDOUT)
		os._exit(0)
	    
	    #self.konsole.startProgram(cmd,argv)
            #reaper = vte.reaper_get()
            #signal_id = reaper.connect("child-exited", finish_dpkg, lock)
            #pid = self.term.fork_command(command=cmd, argv=argv, envv=env)
	    # the communication process is as follows:
	    # child installs the package and sends all lines to the parent
            
	    #process = 
	    #readfd = process.stdout
	    #errfd = process.stderr
	    #for line in errfd:
		    #print line
	    #print "readfd"
	    #print readfd
	    # okay, we're the parent
    	    # now that's what I call an infinite loop
	    # better clean that up soon
	    read = ''
            while True:
                    try:
                        #read += readfd.read(1)
           		print read
                    except OSError, (errno,errstr):
                        # resource temporarly unavailable is ignored
                        if errno != 11:
                            print errstr
                        break
		    
			print "exited"
                    if read.endswith("\n"):
                        statusl = string.split(read, ":")
                        if len(statusl) < 2:
                            print "got garbage from dpkg: '%s'" % read
                            read = ""
                            break
                        status = statusl[2].strip()
                        #print status
                        if status == "error" or status == "conffile-prompt":
                            self.expander.set_expanded(True)
                        read = ""
            	    #self.progress.pulse()
            	    #while gtk.events_pending():
            	    #    gtk.main_iteration()
            	    time.sleep(0.2)
            self.progress.setFinished(true)
            #reaper.disconnect(signal_id)
    
    class InstallProgressAdapter(InstallProgress):
        def __init__(self, app, master, slave):
            # TODO: implement the term
            InstallProgress.__init__(self)
            self.app = app
            self.master = master
            self.slave = slave
            self.finished = False
            #reaper = vte.reaper_get()
            #reaper.connect("child-exited",self.child_exited)
            #self.env = ["VTE_PTY_KEEP_FD=%s"% self.writefd,
                        #"DEBIAN_FRONTEND=gnome",
                        #"APT_LISTCHANGES_FRONTEND=gtk"]
        def child_exited(self,process):
            print "processExited(self):"
	    print "exit status: " + str(process.exitStatus())
    	    self.finished = True
    	    self.apt_status = process.exitStatus()

            #print "child_exited: %s %s %s %s" % (self,term,pid,status)
            #self.apt_status = posix.WEXITSTATUS(status)
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
            self.action.setText("<i>"+_("Installing dependencies...")+"</i>")
            self.progress.setPercent(0.0)
        def statusChange(self, pkg, percent, status):
            self.progress.setPercent(percent/100.0)
            self.progress.setText(status)
        def updateInterface(self):
            #InstallProgress.updateInterface(self)
            #while gtk.events_pending():
                #gtk.main_iteration()
            passs
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
            pass
        def waitChild(self):
            while not self.finished:
                self.updateInterface()
            return self.apt_status

    class FetchProgressAdapter(apt.progress.FetchProgress):
        def __init__(self,progress,action,main):
            #print "FetchProgressAdapter.__init__()"
            self.progress = progress
            self.action = action
            self.main = main
        def start(self):
            #print "start()"
            self.action.setText("<i>"+_("Downloading additional package files...")+"</i>")
            self.progress.setPercent(0)
        def stop(self):
            #print "stop()"
            pass
        def pulse(self):
            if self.currentCPS > 0:
                pass # improve once we migrate to KProgressbar
                #self.progress.setText(_("File %s of %s at %sB/s" % (self.currentItems,self.totalItems,apt_pkg.SizeToStr(self.currentCPS))))
            else:
                pass
                #self.progress.setText(_("File %s of %s" % (self.currentItems,self.totalItems)))
            self.progress.setPercent(self.currentBytes/self.totalBytes)
            #while gtk.events_pending():
                #gtk.main_iteration()
            return True
        def mediaChange(self, medium, drive):
            #print "mediaChange %s %s" % (medium, drive)
            #msg = _("Please insert '%s' into the drive '%s'" % (medium,drive))
            #dialog = gtk.MessageDialog(parent=self.main,
                                       #flags=gtk.DIALOG_MODAL,
                                       #type=gtk.MESSAGE_QUESTION,
                                       #buttons=gtk.BUTTONS_OK_CANCEL)
            #dialog.set_markup(msg)
            #res = dialog.run()
            #print res
            #dialog.destroy()
            #if  res == gtk.RESPONSE_OK:
                #return True
            #return False
            return True
    class CacheProgressAdapter(apt.progress.FetchProgress):
        def __init__(self, progressbar):
            self.progressbar = progressbar
        def update(self, percent):
            self.progressbar.show()
            self.progressbar.setProgress(percent)
            #self.progressbar.set_text(self.op)
            #while gtk.events_pending():
                #gtk.main_iteration()
        def done(self):
            #self.progressbar.hide()
            pass


class GDebiKDEInstall(GDebiKDEInstallDialog):
    def __init__(self,parent=None):
	GDebiKDEInstallDialog.__init__(self,parent)
	self.parent = parent
	self.konsole = None
	self.konsoleFrameLayout = QHBoxLayout(self.konsoleFrame)
	self.konsoleFrame.hide()
	self.newKonsole()
	self.connect(self.konsole,SIGNAL("processExited()"),self.unlock)
    def unlock(self,number):
	self.parent.dprogress.lock.unlock()
    def newKonsole(self):
	# this one belong elsewhere, but we need it here for debug
	self.konsoleFrame.show()
        if self.konsole is not None:
            self.konsole.widget().hide()
	print "az tady"
        self.konsole = konsolePart(self.konsoleFrame, "konsole", self.konsoleFrame, "konsole")
	print "az tady"
        self.konsoleFrame.setMinimumSize(500, 400)
        self.konsole.setAutoStartShell(False)
	self.konsole.setAutoDestroy(False)
        self.konsoleWidget = self.konsole.widget()
        self.konsoleWidget.show()
        self.konsoleFrameLayout.addWidget(self.konsoleWidget)

        #prepare for dpkg pty being attached to konsole
        (self.master, self.slave) = pty.openpty()
        self.konsole.setPtyFd(self.master)

        #self.window_main.showTerminalButton.setEnabled(True)
    
    def showTerminal(self):
        if self.konsole_frame.isVisible():
            self.konsole_frame.hide()
            self.showTerminalButton.setText(_("Show Terminal"))
        else:
            self.konsole_frame.show()
            self.showTerminalButton.setText(_("Hide Terminal"))
