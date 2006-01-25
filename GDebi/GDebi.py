import sys, time, thread, os, fcntl, string, posix
import apt, apt_pkg

from apt.progress import InstallProgress

import pygtk; pygtk.require("2.0")
import gtk, gtk.glade
import gobject
import vte
import gettext
import urllib
import fcntl

from DebPackage import DebPackage, MyCache
from SimpleGladeApp import SimpleGladeApp

from gettext import gettext as _

class GDebi(SimpleGladeApp):

    def __init__(self, datadir, options, file=""):
        SimpleGladeApp.__init__(self, domain="gdebi",
                                path=datadir+"/gdebi.glade")

        # use a nicer default icon
        icons = gtk.icon_theme_get_default()
        logo=icons.load_icon("gnome-mime-application-x-deb", 48, 0)
        if logo != "":
	        gtk.window_set_default_icon_list(logo)

        # set image of button "install"  manually, since it is overriden 
        #by set_label otherwise
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_APPLY,gtk.ICON_SIZE_BUTTON)
        self.button_install.set_image(img)

        # setup status
        self.context=self.statusbar_main.get_context_id("context_main_window")
        self.statusbar_main.push(self.context,_("Loading..."))

        # setup drag'n'drop
        self.window_main.drag_dest_set(gtk.DEST_DEFAULT_MOTION |
                                       gtk.DEST_DEFAULT_HIGHLIGHT |
                                       gtk.DEST_DEFAULT_DROP,
                                       [('text/uri-list',0,0)],
                                       gtk.gdk.ACTION_COPY)

        self.window_main.set_sensitive(False)
        self.notebook_details.set_sensitive(False)
        self.hbox_main.set_sensitive(False)

        # show what we have
        self.window_main.show()

        self.cprogress = self.CacheProgressAdapter(self.progressbar_cache)
        self._cache = MyCache(self.cprogress)
        self.statusbar_main.push(self.context, "")
        self._options = options
        
        # setup the details treeview
        self.details_list = gtk.ListStore(gobject.TYPE_STRING)
        column = gtk.TreeViewColumn("")
        render = gtk.CellRendererText()
        column.pack_start(render, True)
        column.add_attribute(render, "markup", 0)
        self.treeview_details.append_column(column)
        self.treeview_details.set_model(self.details_list)
        
        if file != "" and os.path.exists(file):
            self.window_main.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            while gtk.events_pending(): gtk.main_iteration()        
            self.open(file)
            self.window_main.window.set_cursor(None)
        
        self.window_main.set_sensitive(True)


    def _get_file_path_from_dnd_dropped_uri(self, uri):
        """ helper to get a useful path from a drop uri"""
        path = urllib.url2pathname(uri) # escape special chars
        path = path.strip('\r\n\x00') # remove \r\n and NULL
        # get the path to file
        if path.startswith('file:\\\\\\'): # windows
            path = path[8:] # 8 is len('file:///')
        elif path.startswith('file://'): # nautilus, rox
            path = path[7:] # 7 is len('file://')
        elif path.startswith('file:'): # xffm
            path = path[5:] # 5 is len('file:')
        return path
    
    def on_window_main_drag_data_received(self, widget, context, x, y,
                                          selection, target_type, timestamp):
        """ call when we got a drop event """
        uri = selection.data.strip()
        uri_splitted = uri.split() # we may have more than one file dropped
        for uri in uri_splitted:
            path = self._get_file_path_from_dnd_dropped_uri(uri)
            #print 'path to open', path
            if path.endswith(".deb"):
                self.window_main.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
                while gtk.events_pending(): gtk.main_iteration()        
                self.open(path)
                self.window_main.window.set_cursor(None)

    def open(self, file):
        try:
            self._deb = DebPackage(self._cache, file)
        except (IOError,SystemError),e:
            err_header = _("Could not open \"%s\"" % os.path.basename(file))
            err_body = _("The package might be corrupted or you are not "
                         "allowed to open the file. Check the permissions "
                         "of the file.")
            self.show_alert("error", err_header, err_body)

            return False
            
        self.statusbar_main.push(self.context, "")

        # grey in since we are ready for user input now
        self.window_main.set_sensitive(True)

        # set window titleasddasasdd
        self.window_main.set_title(_("Package Installer - %s" % 
                                   self._deb.pkgName))

        # set name
        self.label_name.set_markup(self._deb.pkgName)
        
        self.notebook_details.set_sensitive(True)
        self.hbox_main.set_sensitive(True)


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
	    self.button_install.set_label(_("_Install Package"))

            self.button_install.set_sensitive(False)
            self.button_details.hide()
            return

        if self._deb.compareToVersionInCache() == DebPackage.VERSION_SAME:
            self.label_status.set_text(_("Version is installed"))
            self.button_install.set_label(_("_Reinstall Package"))
            self.button_install.grab_default()
            self.button_install.set_sensitive(True)
            self.button_details.hide()
            return

        # check if the package is available in the normal sources as well
        res = self._deb.compareToVersionInCache(useInstalled=False)
        if not self._options.non_interactive and res != DebPackage.NO_VERSION:
            pkg = self._cache[self._deb.pkgName]
            title = msg = ""
            
            # FIXME: make this strs better, improve the dialog by
            # providing a option to install from repository directly (when possible)
            if res == DebPackage.VERSION_SAME:
                if self._cache.downloadable(pkg,useCandidate=False):
                    title = "Same version available in repository as well"
                    msg = "The package is available in a repositorysitory as "\
                          "well. It is recommended to install directly "\
                          "from the repository."
            elif res == DebPackage.VERSION_IS_NEWER:
                if self._cache.downloadable(pkg,useCandidate=True):
                    title = "Newer than in the repository"
                    msg = "The package is newer than the version in the "\
                          "cache. While this may be desired it is still "\
                          "recommended to use the version in the repositoryistory "\
                          "because it is "\
                          "usually better tested."
            elif res == DebPackage.VERSION_OUTDATED:
                if self._cache.downloadable(pkg,useCandidate=True):
                    title = "Older than in the repository"
                    msg = "The package is older than the version in the "\
                          "cache. It is strongly recommended to "\
                          "use the version in the repositoryistory because it is "\
                          "usually better tested."

            if title != "" and msg != "":
                msg = "<big><b>%s</b></big>\n\n%s" % (title,msg)
                dialog = gtk.MessageDialog(parent=self.window_main,
                                           flags=gtk.DIALOG_MODAL,
                                           type=gtk.MESSAGE_INFO,
                                           buttons=gtk.BUTTONS_OK)
                dialog.set_markup(msg)
                dialog.run()
                dialog.destroy()

        (install, remove, unauthenticated) = self._deb.requiredChanges
        deps = ""
        if len(remove) == len(install) == 0:
            deps = _("All dependencies satisfied")
            self.button_details.hide()
        else:
            self.button_details.show()
        if len(remove) > 0:
            # FIXME: use ngettext here
            deps += _("Need to <b>remove</b> %s packages from the archive\n" % len(remove))
        if len(install) > 0:
            deps += _("Need to install %s packages from the archive" % len(install))
        self.label_status.set_markup(deps)
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_APPLY,gtk.ICON_SIZE_BUTTON)
        self.button_install.set_image(img)
        self.button_install.set_label(_("_Install Package"))
        self.button_install.set_sensitive(True)
        self.button_install.grab_default()

    def on_button_details_clicked(self, widget):
        #print "on_button_details_clicked"
        (install, remove, unauthenticated) = self._deb.requiredChanges
        self.details_list.clear()
        for rm in remove:
            self.details_list.append([_("<b>To be removed: %s</b>" % rm)])
        for inst in install:
            self.details_list.append([_("To be installed: %s" % inst)])
        self.dialog_details.run()
        self.dialog_details.hide()

    def on_open_activate(self, widget):
        #print "open"
        # build dialog
        fs = gtk.FileChooserDialog(parent=self.window_main,
                                   buttons=(gtk.STOCK_CANCEL, 
                                            gtk.RESPONSE_CANCEL, 
                                            gtk.STOCK_OPEN, 
                                            gtk.RESPONSE_OK),
                                   action=gtk.FILE_CHOOSER_ACTION_OPEN,
				   title="Open Software Package")
        fs.set_default_response(gtk.RESPONSE_OK)
        # set filter
        filter = gtk.FileFilter()
        filter.add_pattern("*.deb")
        filter.set_name(_("Deb packages"))
        #fs.add_filter(filter)
        fs.set_filter(filter)
        # run it!
        if fs.run() == gtk.RESPONSE_OK:
            #print fs.get_filename()
            self.open(fs.get_filename())
        fs.destroy()

    def on_about_activate(self, widget):
        #print "about"
        from Version import VERSION
        self.dialog_about.set_version(VERSION)
        self.dialog_about.run()
        self.dialog_about.hide()

    def on_button_install_clicked(self, widget):
        #print "install"
	self.statusbar_main.push(self.context,_("Installing package file..."))
        (install, remove, unauthenticated) = self._deb.requiredChanges
        if widget != None and len(unauthenticated) > 0:
            primary = _("Unauthenticated packages")
            secondary = _("You are about to install software that "
                          "<b>can't be authenticated</b>! Doing "
                          "this could allow a malicious individual "
                          "to damage or take control of your "
                          "system.\n\n"
                          "The packages below are not authenticated. "
                          "Are you sure you want to continue?")
            msg = "<big><b>%s</b></big>\n\n%s" % (primary, secondary)
            dialog = gtk.MessageDialog(parent=self.dialog_deb_install,
                                       flags=gtk.DIALOG_MODAL,
                                       type=gtk.MESSAGE_WARNING,
                                       buttons=gtk.BUTTONS_YES_NO)
            dialog.set_markup(msg)
            dialog.set_border_width(6)
            scrolled = gtk.ScrolledWindow()
            textview = gtk.TextView()
            textview.set_cursor_visible(False)
            textview.set_editable(False) 
            buf = textview.get_buffer()
            buf.set_text("\n".join(unauthenticated))
            scrolled.add(textview)
            scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrolled.show()
            dialog.vbox.pack_start(scrolled)
            textview.show()
            res = dialog.run()
            dialog.destroy()
            if res != gtk.RESPONSE_YES:
                return
        
        if os.getuid() != 0:
            self.dialog_admin.set_transient_for(self.window_main)
            res = self.dialog_admin.run()
            self.dialog_admin.hide()
            if res == gtk.RESPONSE_OK:
                msg="<b><big>%s</big></b>" % \
                    (_("Enter your password to install %s" % self._deb.pkgName)) 
                os.execl("/usr/bin/gksu", "gksu", "-m", msg,
                         "--", "gdebi-gtk", "--non-interactive", 
                         self._deb.file)
            return
        
        # lock for install
        self.window_main.set_sensitive(False)
        self.button_deb_install_close.set_sensitive(False)
        # clear terminal
        #self._term.feed(str(0x1b)+"[2J")
        self.dialog_deb_install.set_transient_for(self.window_main)
        self.dialog_deb_install.show_all()

        # install the dependecnies
        if len(install) > 0 or len(remove) > 0:
            try:
                apt_pkg.PkgSystemLock()
            except SystemError:
                header = _("Only one software management tool is allowed to"
                           " run at the same time")
                body = _("Please close the other application e.g. \"Update "
                         "Manager\", \"aptitude\" or \"Synaptic\" at first.")
                self.show_alert("error", header, body)
                self.dialog_deb_install.hide()
                self.window_main.set_sensitive(True)
                return
            # FIXME: use the new python-apt acquire interface here,
            # or rather use it in the apt module and raise exception
            # when stuff goes wrong!
            fprogress = self.FetchProgressAdapter(self.progressbar_install,
                                                  self.label_action,
                                                  self.dialog_deb_install)
            iprogress = self.InstallProgressAdapter(self.progressbar_install,
                                                    self._term,
                                                    self.label_action,
                                                    self.expander_install)
            errMsg = None
            try:
                res = self._cache.commit(fprogress,iprogress)
            except IOError, msg:
                res = False
                errMsg = "%s" % msg
                header = _("Failed to fetch dependencies")
                body = _("Failed to fetch the following dependencies:")
            except SystemError, msg:
                res = False
                header = _("Install problem"),
                body = _("Installing the "
                              "dependencies was "
                              "not sucessful. This "
                              "a bug in the archive "
                              "please see the "
                              "terminal window "
                              "for details.")
            if res == False:
                self.show_alert("error", header, body, msg)
                
                self.label_install_status.set_markup("<span foreground=\"red\" weight=\"bold\">%s</span>" % primary)
                self.button_deb_install_close.set_sensitive(True)
                self.button_deb_install_close.grab_default()
		self.statusbar_main.push(self.context,_("Failed to install package file"))
                return 

        # install the package itself
        self.label_action.set_markup("<b><big>"+_("Installing package file")+"</big></b>")
        dprogress = self.DpkgInstallProgress(self._deb.file,
                                             self.label_install_status,
                                             self.progressbar_install,
                                             self._term,
                                             self.expander_install)
        dprogress.commit()
        #self.label_action.set_markup("<b><big>"+_("Package installed")+"</big></b>")
        # show the button
        self.button_deb_install_close.set_sensitive(True)
        self.button_deb_install_close.grab_default()
        if dprogress.exitstatus == 0:
            self.label_install_status.set_markup("<i>"+_("Package \"%s\" is installed") % os.path.basename(self._deb.file)+"</i>")
        else:
            self.label_install_status.set_markup("<b>"+_("Package \"%s\" installation failed") % os.path.basename(self._deb.file)+"</b>")
            self.expander_install.set_expanded(True)
        self.statusbar_main.push(self.context,_("Installation complete"))
        # FIXME: Doesn't stop notifying
        #self.window_main.set_property("urgency-hint", 1)

        # reopen the cache, reread the file, FIXME: add progress reporting
        #self._cache = MyCache(self.cprogress)
        self._cache = MyCache()
        if self._cache._depcache.BrokenCount > 0:
            err_header = _("Dependency problem")
            err_body = _("Internal error, please report this as a bug:\n"
                         "A dependency problem was found after "
                         "installation.\n You have to run: "
                         "'apt-get install -f' to correct the situation")
            self.show_alert("error", err_header, err_body)

            #print "Autsch, please report"
        self.open(self._deb.file)
        
    def on_button_deb_install_close_clicked(self, widget):
        # FIXME: doesn't turn it off
        #self.window_main.set_property("urgency-hint", 0)
        self.dialog_deb_install.hide()
        self.window_main.set_sensitive(True)

    def create_vte(self, arg1,arg2,arg3,arg4):
        #print "create_vte (for the custom glade widget)"
        self._term = vte.Terminal()
        self._term.set_font_from_string("monospace 10")
        return self._term


    def show_alert(self, type, header, body=None, details=None):
        self.dialog_hig.set_transient_for(self.window_main)

        message = "<b><big>%s</big></b>" % header
        if not body == None:
            message = "%s\n\n%s" % (message, body)
        self.label_hig.set_markup(message)
  
        if not details == None:
             buffer = self.textview_hig.get_buffer()
             buffer.set_text(details)
             self.expander_hig.set_expanded(False)
             self.expander_hig.show()
             
        if type == "error":
             self.image_hig.set_property("stock", "gtk-dialog-error")
        elif type == "warn":
             self.image_hig.set_property("stock", "gtk-dialog-warning")
        elif type == "info":
             self.image_hig.set_property("stock", "gtk-dialog-info")
             
        res = self.dialog_hig.run()
        self.dialog_hig.hide()
        if res == gtk.RESPONSE_CLOSE:
            return True

        
    # embedded classes
    class DpkgInstallProgress(object):
        def __init__(self, debfile, status, progress, term, expander):
            self.debfile = debfile
            self.status = status
            self.progress = progress
            self.term = term
            self.expander = expander
            self.expander.set_expanded(False)
        def commit(self):
            def finish_dpkg(term, pid, status, lock):
                " helper "
                self.exitstatus = posix.WEXITSTATUS(status)
                #print "dpkg finished %s %s" % (pid,status)
                #print "exit status: %s" % self.exitstatus
                #print "was signaled %s" % posix.WIFSIGNALED(status)
                lock.release()

            # get a lock
            lock = thread.allocate_lock()
            lock.acquire()

            # ui
            self.status.set_markup("<i>"+_("Installing \"%s\"...") % \
                                   os.path.basename(self.debfile)+"</i>")
            self.progress.pulse()
            self.progress.set_text("")

            # prepare reading the pipe
            (readfd, writefd) = os.pipe()
            fcntl.fcntl(readfd, fcntl.F_SETFL,os.O_NONBLOCK)
            #print "fds (%i,%i)" % (readfd,writefd)

            # the command
            cmd = "/usr/bin/dpkg"
            argv = [cmd,"--status-fd", "%s"%writefd, "-i", self.debfile]
            env = ["VTE_PTY_KEEP_FD=%s"% writefd]
            #print cmd
            #print argv
            #print env
            #print self.term


            # prepare for the fork
            reaper = vte.reaper_get()
            reaper.connect("child-exited", finish_dpkg, lock)
            pid = self.term.fork_command(command=cmd, argv=argv, envv=env)
            read = ""
            while lock.locked():
                while True:
                    try:
                        read += os.read(readfd,1)
                    except OSError, (errno,errstr):
                        # resource temporarly unavailable is ignored
                        if errno != 11:
                            print errstr
                        break
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
                self.progress.pulse()
                while gtk.events_pending():
                    gtk.main_iteration()
                time.sleep(0.2)
            self.progress.set_fraction(1.0)
            
    
    class InstallProgressAdapter(InstallProgress):
        def __init__(self,progress,term,label,term_expander):
            InstallProgress.__init__(self)
            self.progress = progress
            self.term = term
            self.term_expander = term_expander
            self.finished = False
            self.action = label
            reaper = vte.reaper_get()
            reaper.connect("child-exited",self.child_exited)
            self.env = ["VTE_PTY_KEEP_FD=%s"% self.writefd,
                        "DEBIAN_FRONTEND=gnome",
                        "APT_LISTCHANGES_FRONTEND=gtk"]
        def child_exited(self,term, pid, status):
            #print "child_exited: %s %s %s %s" % (self,term,pid,status)
            self.apt_status = posix.WEXITSTATUS(status)
            self.finished = True
        def error(self, pkg, errormsg):
            # FIXME: display a msg
            self.term_expander.set_expanded(True)
        def conffile(self, current, new):
            # FIXME: display a msg or expand term
            self.term_expander.set_expanded(True)
        def startUpdate(self):
            #print "startUpdate"
            apt_pkg.PkgSystemUnLock()
            self.action.set_markup("<i>"+_("Installing dependencies...")+"</i>")
            self.progress.set_fraction(0.0)
        def updateInterface(self):
            InstallProgress.updateInterface(self)
            self.progress.set_fraction(float(self.percent)/100.0)
            self.progress.set_text(self.status)
            while gtk.events_pending():
                gtk.main_iteration()
        def fork(self):
            return self.term.forkpty(envv=self.env)
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
            self.action.set_markup("<i>"+_("Downloading additional package files...")+"</i>")
            self.progress.set_fraction(0)
        def stop(self):
            #print "stop()"
            pass
        def pulse(self):
            self.progress.set_text(_("%s/%s (Speed: %s/s)" % (self.currentItems,self.totalItems,apt_pkg.SizeToStr(self.currentCPS))))
            self.progress.set_fraction(self.currentBytes/self.totalBytes)
            while gtk.events_pending():
                gtk.main_iteration()
            return True
        def mediaChange(self, medium, drive):
            #print "mediaChange %s %s" % (medium, drive)
            msg = _("Please insert '%s' into the drive '%s'" % (medium,drive))
            dialog = gtk.MessageDialog(parent=self.main,
                                       flags=gtk.DIALOG_MODAL,
                                       type=gtk.MESSAGE_QUESTION,
                                       buttons=gtk.BUTTONS_OK_CANCEL)
            dialog.set_markup(msg)
            res = dialog.run()
            #print res
            dialog.destroy()
            if  res == gtk.RESPONSE_OK:
                return True
            return False

    class CacheProgressAdapter(apt.progress.FetchProgress):
        def __init__(self, progressbar):
            self.progressbar = progressbar
        def update(self, percent):
            self.progressbar.show()
            self.progressbar.set_fraction(percent/100.0)
            #self.progressbar.set_text(self.op)
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
    
