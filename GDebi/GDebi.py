#!/usr/bin/python2.4

import sys,time,thread,os,fcntl
import apt

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
        self._deb = deb = DebPackage(self._cache, file)
        # set name
        self.label_name.set_text(deb["Package"])
        # set description
        buf = self.textview_description.get_buffer()
        buf.set_text(deb["Description"])

        # check the deps
        if not deb.checkDepends():
            self.label_status.set_markup("<span foreground=\"red\" weight=\"bold\">"+
                                         "Error: " +
                                         deb._failureString +
                                         "</span>")
            self.button_install.set_sensitive(False)
        else:
            deps = "Need to install %s packages from the archive" % len(deb._needPkgs)
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
        self.button_deb_install_close.set_sensitive(False)
        self._term.feed(str(0x1b)+"[2J")
        self.dialog_deb_install.show_all()

        # install the dependecnies
        pkgs = self._deb._needPkgs
        if len(pkgs) > 0:

            # build the cmd
            (r, w) = os.pipe()
            fcntl.fcntl(r, fcntl.F_SETFL, os.O_NONBLOCK)
            print "fds are: %s %s" % (r, w)
            cmd = "/usr/bin/apt-get"
            argv = [cmd,"install",
                    "-o", ("APT::Status-Fd=%s"%w)]
            env = ["VTE_PTY_KEEP_FD=%s"%w]
            for pkg in pkgs:
                argv.append(pkg)

            # create a lock
            lock = thread.allocate_lock()
            lock.acquire()
            def finish_apt(term, lock):
                print "apt finished"
                lock.release()
            id = self._term.connect("child-exited", finish_apt, lock)
            # run command and wait until it's finished
            self._term.fork_command(command=cmd,argv=argv,envv=env)
            while lock.locked():
                s = ""
                while gtk.events_pending():
                    gtk.main_iteration()
                try:
                    s = os.read(r,1)
                    print s,
                except OSError:
                    pass
                time.sleep(0.01)
            self._term.disconnect(id)

        # install the package itself
        cmd = "/usr/bin/dpkg"
        argv = [cmd,"-i", self._deb._debfile]
        def finish_dpkg(term, win):
            print "dpkg finished"
            self.button_deb_install_close.set_sensitive(True)
        self._term.connect("child-exited", finish_dpkg,self.dialog_deb_install)
        self._term.fork_command(command=cmd,argv=argv)

    def on_button_deb_install_close_clicked(self, widget):
        self.dialog_deb_install.hide()

    def create_vte(self, arg1,arg2,arg3,arg4):
        print "create_vte"
        self._term = vte.Terminal()
        self._term.set_font_from_string("monospace 10")
        return self._term
