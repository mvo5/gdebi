#import sys
import os
import subprocess
import string
import re
import pty
import warnings
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
import apt_pkg

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from DebPackage import DebPackage, Cache
import gettext
from GDebiCommon import GDebiCommon
##from GDebiKDEInstallDialog import GDebiKDEInstallDialog
##from GDebiKDEDialog import GDebiKDEDialog
from KDEAptDialogs import *

def _(str):
    return unicode(gettext.gettext(str), 'UTF-8')
def __(catalog,str):
    return unicode(gettext.dgettext(catalog, str), 'UTF-8')
def utf8(str):
  if isinstance(str, unicode):
      return str
  return unicode(str, 'UTF-8')

class GDebiKDEDialog(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		uic.loadUi("data/GDebiKDEDialog.ui", self)

class GDebiKDE(GDebiCommon, GDebiKDEDialog):
    def __init__(self,datadir,options,file="",parent = None,name = None,modal = 0,fl = 0):
        GDebiKDEDialog.__init__(self,parent)
        GDebiCommon.__init__(self,datadir,options,file)
        # load the icon
        ##FIXMEself.setIcon(KGlobal.iconLoader().loadIcon("adept_installer",KIcon.NoGroup,KIcon.SizeLarge))
        # first, we load all the default descriptions -- pyuic doesn't use
        # gettext as default
        self.textLabel1.setText(_("Package:"))
        self.textLabel1_2.setText(_("Status:"))
        self.detailsButton.setText(_("Details"))
        self.tabWidget2.setTabText(0,_("Description"))
        self.tabWidget2.setTabText(1,_("Details"))
        self.tabWidget2.setTabText(2,_("Included Files"))
        self.cancelButton.setText(__("kdelibs","&Cancel"))
        self.installButton.setText(_("&Install Package"))
        self.DetailsVersionLabel.setText(_("<b>Version:</b>"))
        self.DetailsMaintainerLabel.setText(_("<b>Maintainer:</b>"))
        self.DetailsPriorityLabel.setText(_("<b>Priority:</b>"))
        self.DetailsSectionLabel.setText(_("<b>Section:</b>"))
        self.DetailsSizeLabel.setText(_("<b>Size:</b>"))
        # translation finished
        self.setDisabled(True)
        self.PackageProgressBar.setEnabled(True)
        self.detailsButton.hide()
	"""FIXME
        self.installButton.setIconSet(KGlobal.iconLoader().loadIconSet("adept_install",KIcon.NoGroup,KIcon.SizeSmall))
        self.cancelButton.setIconSet(KGlobal.iconLoader().loadIconSet("button_cancel",KIcon.NoGroup,KIcon.SizeSmall))
	"""
        self.show()
        self.kapp = KApplication.kApplication() #incidently, this stops it crashing on quit, no idea why, jriddell
        self.kapp.processEvents() #run because openCache takes a while to do its thing
        self.cprogress = CacheProgressAdapter(self.PackageProgressBar)
        if not self.openCache():
            KMessageBox.error(None, '<b>' + self.error_header + '</b><br>' + self.error_body,
                self.error_header)
	    sys.exit(1)	
        # try to open the file
        if file != "" and os.path.exists(file):
            self.open(file)
        else:
            header = _("The package file does not exist")
            body = _("A nonexistent file has been selected for installation. Please select an existing .deb package file.")
            KMessageBox.error(None, '<b>' + header + '</b><br>' + body, header)
            sys.exit(1)

        self.setEnabled(True)
        self.PackageProgressBar.hide()
	self.connect(self.cancelButton, SIGNAL("clicked()"), self.cancelButtonClicked)

    def open(self, file):
        # load the common core
	print "open"
	res = GDebiCommon.open(self,file)
	if res == False:
	    KMessageBox.error(None, '<b>' + self.error_header + '</b><br>' + self.error_body,
			       self.error_header)
	    return False

        # set name
        self.setWindowTitle(_("Package Installer - %s") % self._deb.pkgName)
        self.textLabel1_3.setText(self._deb.pkgName)

        # set description
        buf = self.DecriptionEdit
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
            buf.setText(_("No description is available"))

        # check deps
        if not self._deb.checkDeb():
            #icon = QPixmap(KGlobal.iconLoader().loadIcon("messagebox_critical",KIcon.NoGroup,KIcon.SizeMedium))
            self.installButton.setEnabled(False)
            self.textLabel1_3_2.setText("<font color=\"#ff0000\"> Error: " + self._deb._failureString + "</font>")
            self.detailsButton.hide()
            return False

        # set version_info_{msg,title} strings
        self.compareDebWithCache()
			
        if self._deb.compareToVersionInCache() == DebPackage.VERSION_SAME:
            #self.textLabel1_3_2.setText(_("Same version is already installed"))
            self.installButton.setText(_("&Reinstall Package"))
	    ##FIXMEself.installButton.setIconSet(KGlobal.iconLoader().loadIconSet("adept_reinstall",KIcon.NoGroup,KIcon.SizeSmall))
            #self.button_install.grab_default()
            #self.button_install.set_sensitive(True)
            #self.button_details.hide()

        # load changes into (self.install, self.remove, self.unauthenticated)
        self.getChanges()

        if self.version_info_title != "" and self.version_info_msg != "":
            ##FIXME icon = QPixmap(KGlobal.iconLoader().loadIcon("messagebox_info",KIcon.NoGroup,KIcon.SizeMedium))
            ##self.infoIcon.setPixmap(icon)
            self.infoBox.setText(self.version_info_title + '\n' + self.version_info_msg)

        if len(self.remove) == len(self.install) == 0:
	    pass # handled by common core
        else:
            self.detailsButton.show()

        self.textLabel1_3_2.setText(self.deps)
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
            self.installButton.setText(_("&Install Package"))
        
        if self._deb.compareToVersionInCache() == DebPackage.VERSION_SAME:
            self.installButton.setText(_("Re&install Package"))

    def cancelButtonClicked(self):
        self.close()
