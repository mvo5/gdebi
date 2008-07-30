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
	"""
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
