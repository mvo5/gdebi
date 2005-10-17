#!/usr/bin/python2.4

import sys, time, thread, os, fcntl, string
import apt, apt_pkg

import pygtk; pygtk.require("2.0")
import gtk, gtk.glade
import vte

from DebPackage import DebPackage
from SimpleGladeApp import SimpleGladeApp


class GDebi(SimpleGladeApp):

    def __init__(self, datadir, file=""):
        SimpleGladeApp.__init__(self,datadir+"/gdebi.glade")

        # fixme, do graphic cache check
        self._cache = apt.Cache()

        if file != "":
            self.open(file)


        
    def open(self, file):
        self._deb = DebPackage(self._cache, file)
        # set name
        self.label_name.set_text(self._deb.pkgName)
        # set description
        buf = self.textview_description.get_buffer()
        try:
            buf.set_text(self._deb["Description"])
        except KeyError:
            buf.set_text("No description found in the package")

        # check the deps
        if not self._deb.checkDepends():
            self.label_status.set_markup("<span foreground=\"red\" weight=\"bold\">"+
                                         "Error: " +
                                         self._deb._failureString +
                                         "</span>")
            self.button_install.set_sensitive(False)
        else:
            deps = "Need to install %s packages from the archive" % len(self._deb.missingDeps)
            self.label_status.set_text(deps)
            self.button_install.set_sensitive(True)
        

    def on_open_activate(self, widget):
        print "open"
        # build dialog
        fs = gtk.FileChooserDialog(parent=self.window_main,
                                   buttons=(gtk.STOCK_CANCEL, 
                                            gtk.RESPONSE_CANCEL, 
                                            gtk.STOCK_OPEN, 
                                            gtk.RESPONSE_OK),
                                   action=gtk.FILE_CHOOSER_ACTION_OPEN)
        fs.set_default_response(gtk.RESPONSE_OK)
        # set filter
        filter = gtk.FileFilter()
        filter.set_name("Deb packages")
        filter.add_pattern("*.deb")
        fs.add_filter(filter)
        # run it!
        if fs.run() == gtk.RESPONSE_OK:
            print fs.get_filename()
            self.open(fs.get_filename())
        fs.destroy()

    def on_about_activate(self, widget):
        print "about"
        self.dialog_about.run()
        self.dialog_about.hide()

    def on_button_install_clicked(self, widget):
        print "install"
        self.window_main.set_sensitive(False)
        self.button_deb_install_close.set_sensitive(False)
        # clear terminal
        #self._term.feed(str(0x1b)+"[2J")
        self.dialog_deb_install.set_transient_for(self.window_main)
        self.dialog_deb_install.show_all()

        # install the dependecnies
        pkgs = self._deb.missingDeps
        if len(pkgs) > 0:
            fprogress = self.FetchProgressAdapter(self.progressbar_install)
            iprogress = self.InstallProgressAdapter(self.progressbar_install,
                                                    self._term)
            for pkg in pkgs:
                self._cache[pkg].markInstall()
            self._cache.commit(fprogress,iprogress)
        

        # install the package itself
        dprogress = self.DpkgInstallProgress(self._deb.file,
                                             self.label_install_status,
                                             self.progressbar_install,
                                             self._term)
        dprogress.commit()
        self.open(self._deb.file)
        self.button_deb_install_close.set_sensitive(True)
        
    def on_button_deb_install_close_clicked(self, widget):
        self.dialog_deb_install.hide()
        self.window_main.set_sensitive(True)

    def create_vte(self, arg1,arg2,arg3,arg4):
        print "create_vte"
        self._term = vte.Terminal()
        self._term.set_font_from_string("monospace 10")
        return self._term


    # embedded classes
    class DpkgInstallProgress(object):
        def __init__(self, debfile, status, progress,term):
            self.debfile = debfile
            self.status = status
            self.progress = progress
            self.term = term
        def commit(self):
            lock = thread.allocate_lock()
            lock.acquire()
            cmd = "/usr/bin/dpkg"
            argv = [cmd,"-i", self.debfile]
            def finish_dpkg(term, lock):
                print "dpkg finished"
                lock.release()
            self.status.set_text("Installing %s" % self.debfile)
            self.progress.pulse()
            self.progress.set_text("")
            self.term.connect("child-exited", finish_dpkg, lock)
            self.term.fork_command(command=cmd,argv=argv)
            while lock.locked():
                self.progress.pulse()
                while gtk.events_pending():
                    gtk.main_iteration()
                time.sleep(0.05)
            self.progress.set_fraction(1.0)
    
    class InstallProgressAdapter(apt.progress.InstallProgress):
        def __init__(self,progress,term):
            self.finished = False
            self.progress = progress
            self.term = term
            (read, write) = os.pipe()
            # self.writefd is the magic fd for apt where it will send it
            # status too
            self.writefd=write
            self.status = os.fdopen(read, "r")
            fcntl.fcntl(self.status.fileno(), fcntl.F_SETFL,os.O_NONBLOCK)
            print "read-fd: %s" % self.status.fileno()
            print "write-fd: %s" % self.writefd
            # read from fd into this var
            self.read = ""
        def startUpdate(self):
            print "startUpdate"
        def updateInterface(self):
            if self.status != None:
                try:
                    self.read += os.read(self.status.fileno(),1)
                except OSError, (errno,errstr):
                    # resource temporarly unavailable is ignored
                    if errno != 11: 
                        print errstr
                if self.read.endswith("\n"):
                    s = self.read
                    print s
                    (status, pkg, percent, status_str) = string.split(s, ":")
                    print "percent: %s %s" % (pkg, float(percent)/100.0)
                    self.progress.set_fraction(float(percent)/100.0)
                    self.progress.set_text(string.strip(status_str))
                    self.read = ""
            while gtk.events_pending():
                gtk.main_iteration()
        def finishUpdate(self):
            self.finished = True
        def fork(self):
            print "fork"
            env = ["VTE_PTY_KEEP_FD=%s"%self.writefd]
            print env
            pid = self.term.forkpty(envv=env)
            print "After fork: %s " % pid
            return pid


    class FetchProgressAdapter(apt.progress.FetchProgress):
        def __init__(self,progress):
            self.progress = progress
        def start(self):
            self.progress.set_fraction(0)
        def stop(self):
            pass
        def pulse(self):
            self.progress.set_text("%s/%s (Speed: %s/s)" % (self.currentItems,self.totalItems,apt_pkg.SizeToStr(self.currentCPS)))
            self.progress.set_fraction(self.currentBytes/self.totalBytes)
            while gtk.events_pending():
                gtk.main_iteration()
            return True
