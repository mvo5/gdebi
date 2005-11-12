import sys, time, thread, os, fcntl, string, posix
import apt, apt_pkg

import pygtk; pygtk.require("2.0")
import gtk, gtk.glade
import gobject
import vte
import subprocess

from DebPackage import DebPackage, MyCache
from SimpleGladeApp import SimpleGladeApp


class GDebi(SimpleGladeApp):

    def __init__(self, datadir, file=""):
        SimpleGladeApp.__init__(self,datadir+"/gdebi.glade")

        self.window_main.show()

        self.cprogress = self.CacheProgressAdapter(self.progressbar_cache)
        self._cache = MyCache(self.cprogress)

        # setup the details treeview
        self.details_list = gtk.ListStore(gobject.TYPE_STRING)
        column = gtk.TreeViewColumn("")
        render = gtk.CellRendererText()
        column.pack_start(render, True)
        column.add_attribute(render, "markup", 0)
        self.treeview_details.append_column(column)
        self.treeview_details.set_model(self.details_list)

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

        # set various status bits
        self.label_version.set_text(self._deb["Version"])
        self.label_maintainer.set_text(self._deb["Maintainer"])
        self.label_priority.set_text(self._deb["Priority"])
        self.label_section.set_text(self._deb["Section"])
        self.label_size.set_text(self._deb["Installed-Size"])

        # set filelist
        buf = self.textview_filelist.get_buffer()
        buf.set_text("\n".join(self._deb.filelist))

        # check the deps
        if not self._deb.checkDeb():
            self.label_status.set_markup("<span foreground=\"red\" weight=\"bold\">"+
                                         "Error: " +
                                         self._deb._failureString +
                                         "</span>")
            self.button_install.set_sensitive(False)
            self.button_details.hide()
            return

        (install, remove) = self._deb.requiredChanges
        deps = ""
        if len(remove) == len(install) == 0:
            deps = "All dependencies satisfied"
            self.button_details.hide()
        else:
            self.button_details.show()
        if len(remove) > 0:
            deps += "Need to <b>remove</b> %s packages from the archive\n" % len(remove)
        if len(install) > 0:
            deps += "Need to install %s packages from the archive" % len(install)
        self.label_status.set_markup(deps)
        self.button_install.set_sensitive(True)

    def on_button_details_clicked(self, widget):
        print "on_button_details_clicked"
        (install, remove) = self._deb.requiredChanges
        self.details_list.clear()
        for rm in remove:
            self.details_list.append(["<b>To be removed: %s</b>" % rm])
        for inst in install:
            self.details_list.append(["To be installed: %s" % inst])
        self.dialog_details.run()
        self.dialog_details.hide()

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
        if os.getuid() != 0:
            str = "<big><b>%s</b></big>\n\n%s" % ("Run as root",
                                                  "To install the selected "
                                                  "package you need to run "
                                                  "this program as root. "
                                                  "Do you want to do this "
                                                  "now?")
            dialog = gtk.MessageDialog(parent=self.window_main,
                                       flags=gtk.DIALOG_MODAL,
                                       type=gtk.MESSAGE_QUESTION,
                                       buttons=gtk.BUTTONS_YES_NO)
            dialog.set_markup(str)
            if dialog.run() == gtk.RESPONSE_YES:
                os.execl("/usr/bin/gksudo","gksudo",
                         "--","gdebi-gtk","--non-interactive",self._deb.file)
            dialog.hide()
            return
        
        # lock for install
        self.window_main.set_sensitive(False)
        self.button_deb_install_close.set_sensitive(False)
        # clear terminal
        #self._term.feed(str(0x1b)+"[2J")
        self.dialog_deb_install.set_transient_for(self.window_main)
        self.dialog_deb_install.show_all()

        # install the dependecnies
        (install, remove) = self._deb.requiredChanges
        if len(install) > 0 or len(remove) > 0:
            apt_pkg.PkgSystemLock()
            fprogress = self.FetchProgressAdapter(self.progressbar_install)
            iprogress = self.InstallProgressAdapter(self.progressbar_install,
                                                    self._term)
            res = self._cache.commit(fprogress,iprogress)
            print "commit retured: %s" % res

        # install the package itself
        dprogress = self.DpkgInstallProgress(self._deb.file,
                                             self.label_install_status,
                                             self.progressbar_install,
                                             self._term)
        dprogress.commit()
        # reopen the cache, reread the file, FIXME: add progress reporting
        self._cache = MyCache()
        self.open(self._deb.file)
        # show the button
        self.button_deb_install_close.set_sensitive(True)
        
    def on_button_deb_install_close_clicked(self, widget):
        self.dialog_deb_install.hide()
        self.window_main.set_sensitive(True)

    def create_vte(self, arg1,arg2,arg3,arg4):
        print "create_vte (for the custom glade widget"
        self._term = vte.Terminal()
        self._term.set_font_from_string("monospace 10")
        return self._term


    # embedded classes
    class DpkgInstallProgress(object):
        def __init__(self, debfile, status, progress, term):
            self.debfile = debfile
            self.status = status
            self.progress = progress
            self.term = term
        def commit(self):
            lock = thread.allocate_lock()
            lock.acquire()
            cmd = "/usr/bin/dpkg"
            argv = [cmd,"-i", self.debfile]
            #print cmd
            #print argv
            print self.term
            def finish_dpkg(term, pid, status, lock):
                print "dpkg finished %s %s" % (pid,status)
                print "exit status: %s" % posix.WEXITSTATUS(status)
                print "was signaled %s" % posix.WIFSIGNALED(status)
                lock.release()
            self.status.set_text("Installing %s" % self.debfile)
            self.progress.pulse()
            self.progress.set_text("")
            reaper = vte.reaper_get()
            reaper.connect("child-exited", finish_dpkg, lock)
            pid = self.term.fork_command(command=cmd,argv=argv)
            while lock.locked():
                self.progress.pulse()
                while gtk.events_pending():
                    gtk.main_iteration()
                time.sleep(0.1)
            self.progress.set_fraction(1.0)
    
    class InstallProgressAdapter(apt.progress.InstallProgress):
        def __init__(self,progress,term):
            print "InstallProgressAdaper.__init__()"
            self.progress = progress
            self.term = term
            self.finished = False
            reaper = vte.reaper_get()
            reaper.connect("child-exited",self.child_exited)
            (read, write) = os.pipe()
            # self.writefd is the magic fd for apt where it will send it
            # status too
            self.writefd=write
            self.status = os.fdopen(read, "r")
            fcntl.fcntl(self.status.fileno(), fcntl.F_SETFL,os.O_NONBLOCK)
            #print "read-fd: %s" % self.status.fileno()
            #print "write-fd: %s" % self.writefd
            # read from fd into this var
            self.read = ""
        def child_exited(self,term, pid, status):
            # FIXME: need to teach vte-terminal to give me pid+status
            print "child_exited: %s %s %s %s" % (self,term,pid,status)
            self.apt_status = posix.WEXITSTATUS(status)
            self.finished = True
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
                    #print s
                    (status, pkg, percent, status_str) = string.split(s, ":")
                    #print "percent: %s %s" % (pkg, float(percent)/100.0)
                    self.progress.set_fraction(float(percent)/100.0)
                    self.progress.set_text(string.strip(status_str))
                    self.read = ""
            while gtk.events_pending():
                gtk.main_iteration()
        def finishUpdate(self):
            print "finishUpdate"
        def fork(self):
            env = ["VTE_PTY_KEEP_FD=%s"%self.writefd]
            #print "fork"
            #print env
            pid = self.term.forkpty(envv=env)
            if pid > 0:
                self.child_pid = pid
            print "pid: %s " % pid
            return pid
        def waitChild(self,pid):
            print "waitChild: %s" % pid
            while not self.finished:
                self.updateInterface()
            # FIXME: return the exit-status of the child
            #        get it from child_exited
            return self.apt_status

    class FetchProgressAdapter(apt.progress.FetchProgress):
        def __init__(self,progress):
            print "FetchProgressAdapter.__init__()"
            self.progress = progress
        def start(self):
            print "start()"
            self.progress.set_fraction(0)
        def stop(self):
            print "stop()"
            pass
        def pulse(self):
            self.progress.set_text("%s/%s (Speed: %s/s)" % (self.currentItems,self.totalItems,apt_pkg.SizeToStr(self.currentCPS)))
            self.progress.set_fraction(self.currentBytes/self.totalBytes)
            while gtk.events_pending():
                gtk.main_iteration()
            return True
        def mediaChange(self, medium, drive):
            print "mediaChange %s %s" % (medium, drive)
            return False

    class CacheProgressAdapter(apt.progress.FetchProgress):
        def __init__(self, progressbar):
            self.progressbar = progressbar
        def update(self, percent):
            self.progressbar.show()
            self.progressbar.set_fraction(percent/100.0)
            self.progressbar.set_text(self.op)
            while gtk.events_pending():
                gtk.main_iteration()
        def done(self):
            self.progressbar.hide()
        
if __name__ == "__main__":
    app = GDebi("data/")

    pkgs = ["3ddesktop"]
    for pkg in pkgs:
        print "installing %s" % pkg
        app._cache[pkg].markInstall()

    for pkg in app._cache:
        if pkg.markedInstall or pkg.markedUpgrade:
            print pkg.name

    apt_pkg.PkgSystemLock()
    app.dialog_deb_install.set_transient_for(app.window_main)
    app.dialog_deb_install.show_all()
 
    # install the dependecnies
    fprogress = app.FetchProgressAdapter(app.progressbar_install)
    iprogress = app.InstallProgressAdapter(app.progressbar_install, app._term)
    res = app._cache.commit(fprogress,iprogress)
    print "commit retured: %s" % res
    
