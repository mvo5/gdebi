# Copyright (c) 2005-2009 Canonical Ltd
#
# AUTHOR:
# Michael Vogt <mvo@ubuntu.com>
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
# along with GDebi; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


import sys
import os
import string
import warnings
from warnings import warn
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
import apt
import apt_pkg

import pygtk
pygtk.require("2.0")
import glib
import gobject
import gtk
import pango
import vte
import urllib
import fcntl
import posix
import time
import thread
import re

from DebPackage import DebPackage, Cache
from SimpleGtkbuilderApp import SimpleGtkbuilderApp
from apt.progress import InstallProgress
from GDebiCommon import GDebiCommon, utf8
from gettext import gettext as _

# the timeout when the termial is expanded if no activity from dpkg
# is happening 
GDEBI_TERMINAL_TIMEOUT=4*60.0

# HACK - there are two ubuntu specific patches, one for VTE, one
#        for gksu
UBUNTU=False
try:
    import lsb_release
    UBUNTU = lsb_release.get_distro_information()['ID'] == 'Ubuntu'
except Exception, e:
    pass

class GDebi(SimpleGtkbuilderApp, GDebiCommon):

    def __init__(self, datadir, options, file=""):
        GDebiCommon.__init__(self,datadir,options,file)
        localesApp="gdebi"
        localesDir="/usr/share/locale"

        SimpleGtkbuilderApp.__init__(
            self, path=datadir+"/gdebi.ui", domain="gdebi")
        # use a nicer default icon
        icons = gtk.icon_theme_get_default()
        try:
          logo=icons.load_icon("gnome-mime-application-x-deb", 48, 0)
          if logo != "":
            gtk.window_set_default_icon_list(logo)
        except Exception, e:
          print "Error loading logo"
          pass
  
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
        #self.vte_terminal.set_font_from_string("monospace 10")
        
        self.cprogress = self.CacheProgressAdapter(self.progressbar_cache)
        if not self.openCache():
            self.show_alert(gtk.MESSAGE_ERROR, self.error_header, self.error_body)
            sys.exit(1)
        self.statusbar_main.push(self.context, "")
        
        # setup the details treeview
        self.details_list = gtk.ListStore(gobject.TYPE_STRING)
        column = gtk.TreeViewColumn("")
        render = gtk.CellRendererText()
        column.pack_start(render, True)
        column.add_attribute(render, "markup", 0)
        self.treeview_details.append_column(column)
        self.treeview_details.set_model(self.details_list)

        # setup the files treeview
        column = gtk.TreeViewColumn("")
        render = gtk.CellRendererText()
        column.pack_start(render, True)
        column.add_attribute(render, "text", 0)
        self.treeview_files.append_column(column)

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
    
    def on_menuitem_quit_activate(self, widget):
        try:
            gtk.main_quit()
        except:
            # if we are outside of the main loop, just exit
            sys.exit(0)

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
        res = GDebiCommon.open(self, file)
        if res == False:
            self.show_alert(gtk.MESSAGE_ERROR, self.error_header, self.error_body)
            return False
            
        self.statusbar_main.push(self.context, "")

        # set window title
        self.window_main.set_title(_("Package Installer - %s") % 
                                   self._deb.pkgName)

        # set name and ungrey some widgets
        self.label_name.set_markup(self._deb.pkgName)
        self.notebook_details.set_sensitive(True)
        self.hbox_main.set_sensitive(True)

        # set description
        buf = self.textview_description.get_buffer()
        try:
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
            #print long_desc
            # do some regular expression magic on the description
            # Add a newline before each bullet
            p = re.compile(r'^(\s|\t)*(\*|0|-)',re.MULTILINE)
            long_desc = p.sub('\n*', long_desc)
            # replace all newlines by spaces
            p = re.compile(r'\n', re.MULTILINE)
            long_desc = p.sub(" ", long_desc)
            # replace all multiple spaces by
            # newlines
            p = re.compile(r'\s\s+', re.MULTILINE)
            long_desc = p.sub("\n", long_desc)
            # write the descr string to the buffer
            buf.set_text(long_desc)
            # tag the first line with a bold font
            tag = buf.create_tag(None, weight=pango.WEIGHT_BOLD)
            iter = buf.get_iter_at_offset(0)
            (start, end) = iter.forward_search("\n",
                                               gtk.TEXT_SEARCH_TEXT_ONLY,
                                               None)
            buf.apply_tag(tag , iter, end)
        except KeyError:
            buf.set_text("No description is available")

        # set various status bits
        self.label_version.set_text(self._deb["Version"])
        self.label_maintainer.set_text(utf8(self._deb["Maintainer"]))
        self.label_priority.set_text(self._deb["Priority"])
        self.label_section.set_text(utf8(self._deb["Section"]))
        self.label_size.set_text(self._deb["Installed-Size"] + " KB")

        # set file list
        store = gtk.TreeStore(str)
        try:
            header = store.append(None, [_("Package control data")])
            for name in self._deb.control_filelist:
                store.append(header, [name])
            header = store.append(None, [_("Upstream data")])
            for name in self._deb.filelist:
                store.append(header, [name])
        except Exception, e:
            print "Exception while reading the filelist: '%s'" % e
            store.clear()
            store.append(None, [_("Error reading filelist")])
        self.treeview_files.set_model(store)
        self.treeview_files.expand_all()
        # and the file content textview
        font_desc = pango.FontDescription('monospace')
        self.textview_file_content.modify_font(font_desc)

        # check the deps
        if not self._deb.checkDeb():
            self.label_status.set_markup(
                "<span foreground=\"red\" weight=\"bold\">"+
                _("Error: ") +
                glib.markup_escape_text(self._deb._failureString) +
                "</span>")
	    self.button_install.set_label(_("_Install Package"))

            self.button_install.set_sensitive(False)
            self.button_details.hide()
            return
        

        # set version_info_{msg,title} strings
        self.compareDebWithCache()
        self.getChanges()

        if self._deb.compareToVersionInCache() == DebPackage.VERSION_SAME:
            self.label_status.set_text(_("Same version is already installed"))
            self.button_install.set_label(_("_Reinstall Package"))
            self.button_install.grab_default()
            self.button_install.set_sensitive(True)
            self.button_details.hide()
            return

        if self.version_info_title != "" and self.version_info_msg != "":
            msg = "<big><b>%s</b></big>\n\n%s" % (self.version_info_title,
              self.version_info_msg)
            dialog = gtk.MessageDialog(parent=self.window_main,
                                       flags=gtk.DIALOG_MODAL,
                                       type=gtk.MESSAGE_INFO,
                                       buttons=gtk.BUTTONS_CLOSE)
            dialog.set_markup(msg)
            dialog.run()
            dialog.destroy()

        # load changes into (self.install, self.remove, self.unauthenticated)
        if len(self.remove) == len(self.install) == 0:
            self.button_details.hide()
        else:
            self.button_details.show()
            
        self.label_status.set_markup(self.deps)
        #img = gtk.Image()
        #img.set_from_stock(gtk.STOCK_APPLY,gtk.ICON_SIZE_BUTTON)
        #self.button_install.set_image(img)
        self.button_install.set_label(_("_Install Package"))
        self.button_install.set_sensitive(True)
        self.button_install.grab_default()

    def on_treeview_files_cursor_changed(self, treeview):
        " the selection in the files list chanaged "
        model = treeview.get_model()
        (path, col) = treeview.get_cursor()
        name = model[path][0]
        # if we are at the top-level, do nothing
        if len(path) < 2:
            return
        # parent path == 0 means we look at the control information
        # parent path == 1 means we look at the data
        parent_path = path[0]
        if name.endswith("/"):
            data = _("Selection is a directory")
        elif parent_path == 0:
            try:
                data = self._deb.control_content(name)
            except Exception, e:
                data = _("Error reading file content '%s'") % e
        elif parent_path == 1:
            try:
                data = self._deb.data_content(name)
            except Exception, e:
                data = _("Error reading file content '%s'") % e
        else:
            assert False, "NOT REACHED"
        if not data:
            data = _("File content can not be extracted")
        buf = self.textview_file_content.get_buffer()
        buf.set_text(data)

    def on_button_details_clicked(self, widget):
        #print "on_button_details_clicked"
        # sanity check
        if not self._deb:
          return
        self.details_list.clear()
        for rm in self.remove:
            self.details_list.append([_("<b>To be removed: %s</b>") % rm])
        for inst in self.install:
            self.details_list.append([_("To be installed: %s") % inst])
        self.dialog_details.set_transient_for(self.window_main)
        self.dialog_details.run()
        self.dialog_details.hide()

    def on_open_activate(self, widget):
        #print "open"
        # build dialog
        self.window_main.set_sensitive(False)
        fs = gtk.FileChooserDialog(parent=self.window_main,
                                   buttons=(gtk.STOCK_CANCEL, 
                                            gtk.RESPONSE_CANCEL, 
                                            gtk.STOCK_OPEN, 
                                            gtk.RESPONSE_OK),
                                   action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                   title=_("Open Software Package"))
        fs.set_default_response(gtk.RESPONSE_OK)
        # set filter
        filter = gtk.FileFilter()
        filter.add_pattern("*.deb")
        filter.set_name(_("Software packages"))
        #fs.add_filter(filter)
        fs.set_filter(filter)
        # run it!
        if fs.run() == gtk.RESPONSE_OK:
            #print fs.get_filename()
            self.open(fs.get_filename())
        fs.destroy()
        self.window_main.set_sensitive(True)

    def on_refresh_activate(self, widget):
        #print "refresh"
        self.window_main.set_sensitive(False)
        self.openCache()
        if self._deb:
            self.open(self._deb.file)
        self.window_main.set_sensitive(True)

    def on_about_activate(self, widget):
        #print "about"
        from Version import VERSION
        self.dialog_about.set_version(VERSION)
        self.dialog_about.run()
        self.dialog_about.hide()

    def on_button_install_clicked(self, widget):
        self.install_completed=False
        # check if we actually have a deb, see #213725
        if not self._deb:
            err_header = _("File not found")
            err_body = _("You tried to install a file that does not "
                         "(or no longer) exist. ")
            dia = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR,
                                    gtk.BUTTONS_OK, "")
            dia.set_markup("<b><big>%s</big></b>" % err_header)
            dia.format_secondary_text(err_body)
            dia.run()
            dia.destroy()
            return
        # do it
        self.statusbar_main.push(self.context,_("Installing package file..."))
        if widget != None and len(self.unauthenticated) > 0:
            primary = _("Install unauthenticated software?")
            secondary = _("Malicious software can damage your data "
                          "and take control of your system.\n\n"
                          "The packages below are not authenticated and "
                          "could therefore be of malicious nature.")
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
            buf.set_text("\n".join(self.unauthenticated))
            scrolled.add(textview)
            scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrolled.show()
            dialog.vbox.pack_start(scrolled)
            textview.show()
            res = dialog.run()
            dialog.destroy()
            if res != gtk.RESPONSE_YES:
                return

        msg_hdr = _("You need to grant administrative rights to install software")
        msg_bdy = _("""
It is a possible security risk to install packages files manually.
Install software from trustworthy software distributors only.
""")
        if os.getuid() != 0:

            # build command and argument lists
            gksu_cmd = "/usr/bin/gksu"
            gksu_args = ["gksu", "--desktop",
                         "/usr/share/applications/gdebi.desktop",
                         "--message",
                         "<big><b>%s</b></big>\n\n%s" % (msg_hdr,msg_bdy)]
            gdebi_args = ["--", "gdebi-gtk", "--non-interactive",
                          self._deb.file]
            # check if we run on ubuntu and always ask for the password
            # there - we would like to do that on debian too, but this
            # gksu patch is only available on ubuntu currently unfortunately
            if UBUNTU:
                    gksu_args.append("--always-ask-pass")
            os.execv(gksu_cmd, gksu_args+gdebi_args)

        if not self.try_acquire_lock():
            self.statusbar_main.push(self.context,
                                     _("Failed to install package file"))
            self.show_alert(gtk.MESSAGE_ERROR, self.error_header, self.error_body)
            return False
            
        # lock for install
        self.window_main.set_sensitive(False)
        self.button_deb_install_close.set_sensitive(False)
        # clear terminal
        #self.vte_terminal.feed(str(0x1b)+"[2J")
        self.dialog_deb_install.set_transient_for(self.window_main)
        self.dialog_deb_install.show_all()

        if len(self.install) > 0 or len(self.remove) > 0:
            # FIXME: use the new python-apt acquire interface here,
            # or rather use it in the apt module and raise exception
            # when stuff goes wrong!
            if not self.acquire_lock():
              self.show_alert(gtk.MESSAGE_ERROR, self.error_header, self.error_body)
              return False
            fprogress = self.FetchProgressAdapter(self.progressbar_install,
                                                self.label_action,
                                                self.dialog_deb_install)
            iprogress = self.InstallProgressAdapter(self.progressbar_install,
                                                    self.vte_terminal,
                                                    self.label_action,
                                                    self.expander_install)
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
                self.show_alert(gtk.MESSAGE_ERROR, header, body, msg,
                                parent=self.dialog_deb_install)
                    
                self.label_install_status.set_markup("<span foreground=\"red\" weight=\"bold\">%s</span>" % header)
                self.button_deb_install_close.set_sensitive(True)
                self.button_deb_install_close.grab_default()
                self.statusbar_main.push(self.context,_("Failed to install package file"))
                return 
    
        # install the package itself
        self.label_action.set_markup("<b><big>" +
                                     _("Installing %s") % self._deb.pkgName+
                                     "</big></b>")
        dprogress = self.DpkgInstallProgress(self._deb.file,
                                             self.label_install_status,
                                             self.progressbar_install,
                                             self.vte_terminal,
                                             self.expander_install)
        dprogress.commit()
        self.install_completed=True
        #self.label_action.set_markup("<b><big>"+_("Package installed")+"</big></b>")
        # show the button
        self.button_deb_install_close.set_sensitive(True)
        self.button_deb_install_close.grab_default()
        #Close if checkbox is selected
        if self.checkbutton_autoclose.get_active():
            self.on_button_deb_install_close_clicked(None)
        self.label_action.set_markup("<b><big>"+_("Installation finished")+"</big></b>")
        if dprogress.exitstatus == 0:
            self.label_install_status.set_markup("<i>"+_("Package '%s' was installed") % os.path.basename(self._deb.file)+"</i>")
        else:
            self.label_install_status.set_markup("<b>"+_("Failed to install package '%s'") % os.path.basename(self._deb.file)+"</b>")
            self.expander_install.set_expanded(True)
        self.statusbar_main.push(self.context,_("Installation complete"))
        # FIXME: Doesn't stop notifying
        #self.window_main.set_property("urgency-hint", 1)

        # reopen the cache, reread the file
        self.openCache()
        if self._cache._depcache.BrokenCount > 0:
            err_header = _("Failed to completely install all dependencies")
            err_body = _("To fix this run 'sudo apt-get install -f' in a "
                         "terminal window.")
            self.show_alert(gtk.MESSAGE_ERROR, err_header, err_body)
        self.open(self._deb.file)
        
    def on_button_deb_install_close_clicked(self, widget):
        # FIXME: doesn't turn it off
        #self.window_main.set_property("urgency-hint", 0)
        self.dialog_deb_install.hide()
        self.window_main.set_sensitive(True)
    
    def on_checkbutton_autoclose_clicked(self, widget):
        if self.install_completed:
            self.on_button_deb_install_close_clicked(None)            

    def on_window_main_delete_event(self, *args):
        if self.window_main.get_property("sensitive"):
            if gtk.main_level() > 0:
                gtk.main_quit()
            return False
        else: 
            return True

    def show_alert(self, type, header, body=None, details=None, parent=None):
        if parent is not None:
             self.dialog_hig.set_transient_for(parent)
        else:
             self.dialog_hig.set_transient_for(self.window_main)

        message = "<b><big>%s</big></b>" % header
        if not body == None:
             message = "%s\n\n%s" % (message, body)
        self.label_hig.set_markup(message)
  
        if not details == None:
             buffer = self.textview_hig.get_buffer()
             buffer.set_text(str(details))
             self.expander_hig.set_expanded(False)
             self.expander_hig.show()
             
        if type == gtk.MESSAGE_ERROR:
             self.image_hig.set_property("stock", "gtk-dialog-error")
        elif type == gtk.MESSAGE_WARNING:
             self.image_hig.set_property("stock", "gtk-dialog-warning")
        elif type == gtk.MESSAGE_INFO:
             self.image_hig.set_property("stock", "gtk-dialog-info")
             
        res = self.dialog_hig.run()
        self.dialog_hig.hide()
        if res == gtk.RESPONSE_CLOSE:
            return True
        return False
        
    # embedded classes
    class DpkgInstallProgress(object):
        def __init__(self, debfile, status, progress, term, expander):
            self.debfile = debfile
            self.status = status
            self.progress = progress
            self.term = term
            self.term_expander = expander
            self.time_last_update = time.time()
            self.term_expander.set_expanded(False)
        def commit(self):
            def finish_dpkg(term, lock):
                """ helper that is run when dpkg finishes """
                status = term.get_child_exit_status()
                self.exitstatus = posix.WEXITSTATUS(status)
                #print "dpkg finished %s %s" % (pid,status)
                #print "exit status: %s" % self.exitstatus
                #print "was signaled %s" % posix.WIFSIGNALED(status)
                lock.release()

            # get a lock
            lock = thread.allocate_lock()
            lock.acquire()

            # ui
            self.status.set_markup("<i>"+_("Installing '%s'...") % \
                                   os.path.basename(self.debfile)+"</i>")
            self.progress.pulse()
            self.progress.set_text("")

            # prepare reading the pipe
            (readfd, writefd) = os.pipe()
            fcntl.fcntl(readfd, fcntl.F_SETFL,os.O_NONBLOCK)
            #print "fds (%i,%i)" % (readfd,writefd)

            # the command
            cmd = "/usr/bin/dpkg"
            argv = [cmd, "--auto-deconfigure"]
            # ubuntu supports VTE_PTY_KEEP_FD, see 
            # https://bugzilla.gnome.org/320128 for the upstream bug
            if UBUNTU:
                argv += ["--status-fd", "%s"%writefd]
            argv += ["-i", self.debfile]
            env = ["VTE_PTY_KEEP_FD=%s"% writefd,
                   "DEBIAN_FRONTEND=gnome",
                   "APT_LISTCHANGES_FRONTEND=gtk"]
            #print cmd
            #print argv
            #print env
            #print self.term

            # prepare for the fork
            self.term.connect("child-exited", finish_dpkg, lock)
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
                    self.time_last_update = time.time()
                    if read.endswith("\n"):
                        statusl = string.split(read, ":")
                        if len(statusl) < 3:
                            print "got garbage from dpkg: '%s'" % read
                            read = ""
                            break
                        status = statusl[2].strip()
                        #print status
                        if status == "error" or status == "conffile-prompt":
                            self.term_expander.set_expanded(True)
                        read = ""
                self.progress.pulse()
                while gtk.events_pending():
                    gtk.main_iteration()
                time.sleep(0.2)
                # if the terminal has not reacted for some time, do something
                if (not self.term_expander.get_expanded() and 
                    (self.time_last_update + GDEBI_TERMINAL_TIMEOUT) < time.time()):
                  self.term_expander.set_expanded(True)
            self.progress.set_fraction(1.0)
    
    class InstallProgressAdapter(InstallProgress):
        def __init__(self,progress,term,label,term_expander):
            InstallProgress.__init__(self)
            self.progress = progress
            self.term = term
            self.term_expander = term_expander
            self.finished = False
            self.action = label
            self.time_last_update = time.time()
            self.term.connect("child-exited", self.child_exited)
            self.env = ["VTE_PTY_KEEP_FD=%s"% self.writefd,
                        "DEBIAN_FRONTEND=gnome",
                        "APT_LISTCHANGES_FRONTEND=gtk"]
        def child_exited(self,term):
            status = term.get_child_exit_status()
            #print "apt finished %s" % status
            #print "exit status: %s" % posix.WEXITSTATUS(status)
            #print "was signaled %s" % posix.WIFSIGNALED(status)
            self.apt_status = status
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
            self.progress.set_text("")
        def statusChange(self, pkg, percent, status):
            self.progress.set_fraction(percent/100.0)
            self.progress.set_text(status)
            self.time_last_update = time.time()
        def updateInterface(self):
            InstallProgress.updateInterface(self)
            while gtk.events_pending():
                gtk.main_iteration()
            if (not self.term_expander.get_expanded() and 
                (self.time_last_update + GDEBI_TERMINAL_TIMEOUT) < time.time()):
              self.term_expander.set_expanded(True)
            # sleep just long enough to not create a busy loop
            time.sleep(0.01)
        def fork(self):
            pid = self.term.forkpty(self.env)
            if pid == 0:
                # *grumpf* workaround bug in vte here (gnome bug #588871)
                for env in self.env:
                    (key, value) = env.split("=")
                    os.environ[key] = value
            return pid
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
            at_item = min(self.currentItems + 1, self.totalItems)
            if self.currentCPS > 0:
                self.progress.set_text(_("File %s of %s at %sB/s") % (at_item,self.totalItems,apt_pkg.SizeToStr(self.currentCPS)))
            else:
                self.progress.set_text(_("File %s of %s") % (at_item,self.totalItems))
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
    app = GDebi("data/",None)

    pkgs = ["cw"]
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
    fprogress = app.FetchProgressAdapter(app.progressbar_install,
                                         app.label_action,
                                         app.dialog_deb_install)
    iprogress = app.InstallProgressAdapter(app.progressbar_install, 
                                           app.vte_terminal,
                                           app.label_action,
                                           app.expander_install)
    res = app._cache.commit(fprogress,iprogress)
    print "commit retured: %s" % res
    
    gtk.main()
