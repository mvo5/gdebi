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
import string
import warnings
from warnings import warn
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
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
from DebPackage import DebPackage, Cache
from apt.progress import InstallProgress
from gettext import gettext as _

def utf8(str):
  return unicode(str, 'latin1').encode('utf-8')
image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x03" \
    "\x07\x49\x44\x41\x54\x38\x8d\x8d\x93\x4b\x68\x54" \
    "\x57\x1c\xc6\xbf\x73\xcf\x9d\xb9\x99\x47\x26\x8f" \
    "\x31\x13\xea\xe4\xa5\xb1\x1a\x1f\x68\x6c\x31\x34" \
    "\x51\xa7\xa1\xad\xe6\x81\x8f\x16\x2a\xe8\x42\x22" \
    "\x22\xe8\x4a\x14\x37\x9a\xad\x4a\xa9\x22\x08\x5d" \
    "\x16\xda\x6e\xba\x10\x54\xba\x2a\x7d\x50\x74\xd1" \
    "\x06\x13\x8a\x28\x92\x4c\x4c\x34\x1a\xcd\xbc\x32" \
    "\x93\xc9\xe4\xde\x7b\xee\x63\xce\xdc\x73\xba\xa9" \
    "\x68\x7c\x80\xdf\xf6\xff\x7d\xbf\xd5\xef\x0f\xbc" \
    "\x47\x54\x40\x7d\xd7\x8d\xbe\x51\x26\xa0\x83\x1f" \
    "\x57\x0f\x04\xfd\x08\x64\x97\xbc\x5c\x7f\x67\xa4" \
    "\x7f\xf8\xc8\xa6\xe1\x5a\xcd\x8b\xe8\x86\xa3\xeb" \
    "\xb6\x34\x24\x20\xdf\x0a\xa8\x0f\xa2\xee\xdc\xd0" \
    "\xc6\xb3\xdf\x5e\x3a\x7a\x79\x5b\x7b\x5d\x4f\x30" \
    "\xd6\xd5\x70\xf2\xd4\xe9\xb3\x3d\x03\x5f\x7f\xbe" \
    "\x2b\xd1\xbe\xef\xc0\xb6\xe0\xfe\xad\x31\xd1\xe9" \
    "\x17\x65\x4d\xb7\x2a\xba\xc5\xa5\x45\x00\x80\x00" \
    "\x64\x63\x93\xb6\xfe\xc2\x99\xde\x8b\x7b\x0e\x0e" \
    "\xee\x95\xcc\xa1\x86\xd8\x8a\x70\x6b\x02\x8a\xaa" \
    "\x81\x31\x1b\xf9\xec\x2c\xc2\xe9\x1b\x68\x2c\x8d" \
    "\xa0\x9c\x4e\xf1\xf1\x47\xc5\x89\x13\xd7\x32\xc7" \
    "\x15\x00\x58\xb5\x42\x69\xfd\xf1\x9b\xc1\x9f\xf6" \
    "\x0f\x7d\xf5\x25\xcd\xa7\xa8\x99\x05\xaa\xe2\xdb" \
    "\x41\x14\x15\xb6\x65\xc3\x62\x0c\x8a\xaf\x06\x59" \
    "\xe5\x23\x98\x79\x03\x7e\x56\xf4\x4d\xa6\xed\x89" \
    "\x64\xbe\x32\x41\x01\xc0\xe1\xd2\x6d\x0c\x89\x86" \
    "\x4f\x56\xd2\x1e\xf2\x64\x52\x65\xf5\x9f\x41\x8b" \
    "\x6f\x06\x33\x4d\x64\xd2\x29\x30\x66\x41\x48\xc0" \
    "\xf1\x34\x90\x67\x77\xe0\xd7\xe7\x9c\xdb\x69\xff" \
    "\x3f\xed\xb5\xfe\x0e\xaa\xa9\xd0\x42\x55\x4a\xb0" \
    "\xb8\x68\x14\xbb\x1a\xec\xae\x98\xf0\x3e\x30\x5a" \
    "\xf6\x00\x35\x71\x64\xd3\x29\x94\x66\xef\x80\xe9" \
    "\x8b\x80\xaf\x0e\xdc\x03\xa8\xf5\x1c\x0d\x2d\xb5" \
    "\xa8\xad\x0e\xaf\xf8\xed\xdf\xd4\xaf\xea\xe1\x2e" \
    "\x7a\xe8\x8b\x9d\x1d\xbb\x77\xf4\x25\x12\xb1\xf8" \
    "\xca\x18\x0a\x0b\x08\x90\x2c\x78\x71\x16\xae\xe3" \
    "\x02\x52\xc0\xf3\x38\x1c\xb7\x8c\x7a\x6f\x16\xcd" \
    "\x51\x1b\x4f\x1f\x16\xd2\xc7\xae\xfc\x3d\x34\x9a" \
    "\x72\x47\xe8\xd4\xbc\x9c\x1e\x9d\x2c\x8d\x4d\x26" \
    "\x9f\x25\x43\xdc\x08\x7d\xd8\xb9\x61\x4d\x60\xe1" \
    "\x1e\x09\x24\xaf\x23\x34\xff\x00\x9c\x54\x43\xd6" \
    "\xb4\x21\xce\xc7\xd1\x96\xbf\x89\x2a\x67\x0e\x0f" \
    "\x92\xb9\xa9\xab\x7f\x65\x2e\x73\x81\xb2\x6a\xba" \
    "\x60\x66\x8e\xcf\x3c\xce\x65\x66\x98\xc5\xed\xde" \
    "\xa1\xc3\x7d\x05\xad\x97\x06\x7d\x77\x11\x36\xc6" \
    "\xb1\x2e\x38\x0d\xee\x3e\x86\x6f\xee\x1e\x88\xe7" \
    "\x40\x2a\x04\xa2\xec\x12\x85\x10\x05\x90\xaf\x19" \
    "\x26\x89\xac\xd8\x5c\x32\xac\x45\x21\xba\x05\x81" \
    "\x68\x1e\x75\xa9\x9f\x11\x5d\xb8\x0d\x62\x16\x21" \
    "\xa4\x00\x27\x02\xa4\xe2\x11\xf2\xd2\xd2\x57\x22" \
    "\x04\xca\x4b\x0e\x14\x5f\x09\x92\x95\xc0\x00\x84" \
    "\x4d\x17\x30\x75\x08\x87\xc1\xf1\x38\x40\x09\x88" \
    "\x50\x5f\xec\x5f\x07\x48\x2a\x8a\x59\x2a\x31\x0a" \
    "\x95\xc6\xc1\x69\x04\xc4\xc8\x00\x96\x0e\xd7\x66" \
    "\xf0\x44\x05\x3e\xbf\x06\xdd\x84\xe1\x49\x88\x37" \
    "\x00\xf9\x45\xa7\x90\xbb\x3f\x32\xd3\xdc\x78\xbf" \
    "\xcd\x93\x01\xaa\x57\xa2\x08\x2d\xdc\x85\x70\x4d" \
    "\x88\xb2\x03\x09\x1f\xfe\x98\xc2\xad\xf3\xb7\x8a" \
    "\xc3\x56\x45\x9a\xff\x5b\xbc\xec\x91\xd4\xa6\x08" \
    "\x6d\xe9\x6e\x0b\xef\xdc\xd5\x51\x3d\xd0\xdd\x42" \
    "\xbb\x9b\x83\x56\x93\x5f\x25\x4a\x7e\xc9\x33\x7f" \
    "\x18\x2b\x7f\xff\xdd\x18\xbb\x34\xef\x88\xec\x8b" \
    "\xcd\x32\xc0\x32\x18\xa0\xb6\x46\xe8\xea\xed\xcd" \
    "\xda\xa7\x3b\x56\x85\x13\x7f\x4e\x9b\xbf\xff\x32" \
    "\x65\x5d\xe3\x12\xfc\xd5\xde\x7f\xc1\xf9\x6f\xcb" \
    "\x88\x15\x93\x72\x00\x00\x00\x00\x49\x45\x4e\x44" \
    "\xae\x42\x60\x82"
image1_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
    "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x04" \
    "\x32\x49\x44\x41\x54\x38\x8d\xb5\x95\x5b\x88\x56" \
    "\x55\x14\xc7\x7f\x6b\xed\x7d\xce\xf7\xcd\x38\x37" \
    "\x1b\xa7\x34\x73\xf2\x52\xa6\xdd\x84\x34\x29\xe8" \
    "\xa1\x06\x0d\xbb\xbc\xf9\x10\xf5\x92\xc9\x88\x41" \
    "\x2f\xfa\x32\x41\x45\x51\x51\x3d\x04\x12\x11\x79" \
    "\x81\x40\xd3\x12\x89\x52\x4b\x84\xe8\x46\xa6\x29" \
    "\x59\x56\x8c\x3a\x96\x8a\x99\x46\x49\x3a\xa8\x39" \
    "\xf3\x7d\xe7\x3b\xdf\xde\xab\x87\x33\xce\xe4\xd8" \
    "\xab\x6b\xb3\x39\x6c\xd6\xe2\xcf\xff\xfc\xff\x6b" \
    "\xef\x25\x66\xc6\x95\x08\x0f\x20\x4b\x13\x08\x02" \
    "\xf5\x14\x4c\x8a\x4c\x08\xb7\x4b\xb0\x4d\xd3\xc6" \
    "\x5e\x3f\x3d\xf1\x09\x56\x97\x22\x67\x0a\x11\x8e" \
    "\x9d\xfa\xf3\x54\x96\x87\x6e\x7c\x69\x3b\x58\x91" \
    "\xcb\x3d\x04\xb0\xcf\x7e\x2b\x80\x2f\x8b\x18\x52" \
    "\x1f\xe3\x07\xcf\x2c\x7c\x76\x7a\x77\x57\x37\xcd" \
    "\xa5\x26\x62\x8c\x00\x88\x08\x79\xc8\xd9\xbc\x7b" \
    "\xdb\x84\x9e\x35\xcf\xbd\x7f\x3e\xab\xdd\x86\xf3" \
    "\x27\x46\x43\xe8\xa5\xa7\x00\x02\xd4\xb3\x5b\x3a" \
    "\xdb\x27\x4d\x7b\xea\xfe\x27\x19\x7f\xd5\x38\xfa" \
    "\xce\xf6\x72\xe4\xc2\x21\x8e\x0e\xfc\xca\xa1\x7f" \
    "\xf6\x23\xa5\xc8\xd2\x05\x8f\x33\x67\xe6\xdc\x56" \
    "\xaa\x03\x5d\xc4\x08\xe1\x52\xa8\x51\x8c\x0d\x24" \
    "\x00\x16\x52\x9f\x9a\x57\xcf\xae\xe3\xbb\xe8\x7a" \
    "\xb7\x8b\x72\xa9\x4c\xea\x53\xce\xe5\xe7\x58\x31" \
    "\x6f\x05\xcb\x67\x2f\xa7\xb1\xa1\x09\x90\x1c\x73" \
    "\x23\x12\x5e\x06\x1c\x83\x27\xcb\xef\x23\x92\x50" \
    "\x65\xfa\x85\xea\x05\x09\x21\xa0\x22\xa4\x9a\x92" \
    "\x6a\x4a\xa2\x09\x5e\x3d\x4e\x1c\x00\x83\x95\x01" \
    "\xa8\x0c\xce\x81\xb4\x9f\x20\x0e\x5f\xde\x8d\x24" \
    "\xfd\x23\xc0\xd1\x6e\x76\xb8\x4f\xa6\x4f\x9a\x31" \
    "\xa5\x94\x34\x10\xab\x39\xd7\xb7\x4f\x91\xd4\x27" \
    "\x44\x8b\x88\xc8\x25\xdb\x28\x3a\xe9\xa6\xeb\xa6" \
    "\x71\x7a\xe6\x9c\x65\x5a\x6e\x5e\x16\xf3\xc8\xe1" \
    "\x13\xc7\x4e\x57\x6a\xf5\x45\xc0\xf6\xa2\x2b\xea" \
    "\x71\x7d\xcf\x43\x4f\x4f\x5d\x76\xff\x32\xda\x1a" \
    "\xdb\x08\x31\xe0\xc4\x91\x26\x09\xbe\x3f\x19\x25" \
    "\x96\x51\xd2\x12\x00\x6f\x76\xbf\x46\x6d\x51\x2e" \
    "\x4e\x95\xac\x9e\xf1\xde\x97\x9b\x3b\x7a\xde\x7a" \
    "\x61\x2d\x70\xb5\x07\x98\xd0\x7a\xed\xcc\x25\xf7" \
    "\x2e\xa1\xa3\x65\x1c\xdb\x0f\x6d\x07\x05\x41\x50" \
    "\x51\xf6\xfd\xb5\x0f\x27\x0e\xa1\x60\x9a\x68\x42" \
    "\xef\x99\x5e\x3e\x3f\xfe\x39\x51\x02\xa2\x4a\x20" \
    "\x70\xf7\x84\xbb\x58\xbc\xe0\x51\x56\x7f\xbc\xbe" \
    "\x7d\x58\x8a\x44\x3d\x4e\x1d\x47\x4e\x1f\xe1\xe1" \
    "\x77\x1e\x06\x07\xe2\x04\xf1\x42\x92\x24\x34\x96" \
    "\x1a\x0b\x09\xcc\x68\x4e\x9a\xd9\x78\x70\x23\x1b" \
    "\xfa\x36\x20\x5e\x50\xa7\x0c\xda\x20\x1f\x3d\xf8" \
    "\x21\xf3\xae\x5e\x80\x73\xc9\x88\x79\x66\x46\x8c" \
    "\x11\x15\xa5\x94\x94\x10\x27\x38\xe7\x50\xa7\x88" \
    "\x2f\x98\xca\xd0\x32\x8c\xc4\x25\xa4\x9a\xa2\x5e" \
    "\x51\xa7\x60\xe0\xc4\x61\x16\x31\x8b\xff\xd7\x6e" \
    "\x20\x2a\xa8\xea\xf0\x16\x64\x74\x09\x8a\x16\x75" \
    "\xa2\x5c\x5c\xa3\xa3\x30\x0f\x41\x44\x09\x16\xa8" \
    "\x0e\x56\xc1\x0d\x65\x1c\xb8\xd4\xd1\xd2\xd0\x32" \
    "\x6c\x9c\xc3\x51\xa9\x57\xc8\xea\x19\xea\x14\xf5" \
    "\x85\x14\xb9\xe5\x88\x28\x22\x32\x02\x1c\x2c\x08" \
    "\x62\x74\xb6\x75\xb2\xe6\x91\xd5\x88\x0a\x20\x78" \
    "\xef\x39\xf0\xf7\x01\x56\xed\x5b\x45\xa2\x09\x2a" \
    "\xca\x40\x7d\x80\x85\x33\x16\x32\x7f\xf2\x7c\x72" \
    "\x72\x54\x95\xba\xe5\xcc\x6e\xbf\x03\x51\xb0\xa1" \
    "\xab\x8f\x99\xe1\x9f\xf0\x07\x5f\xdd\xf6\x9a\x55" \
    "\x6a\x15\x1b\x1d\x3b\x8f\xef\xb4\xf2\x2b\x65\x6b" \
    "\x7b\xbd\xcd\x3a\xde\xe8\x30\xff\xba\xb7\x95\x3f" \
    "\xad\xbc\xac\xce\xa2\xd9\x7b\x5f\x6c\xb1\xd6\x05" \
    "\x37\xf4\x9b\x59\xc1\xb8\xae\x71\xf1\x8b\x9b\x5f" \
    "\xfa\x70\xf3\xf7\x1f\x4f\x18\x53\x6e\x91\xac\x5a" \
    "\x65\xf2\xd8\x49\xac\xec\x7e\x9b\x9a\xd5\x86\xc4" \
    "\xbf\xf8\x11\xb2\x90\x01\xd0\xb3\xf6\x65\x76\xfe" \
    "\xfc\x2d\x69\xb9\x99\x7a\xad\xc6\xfe\xc3\x7d\x67" \
    "\xcf\x65\x83\x4f\x8d\x98\x27\xba\x27\xab\x57\x6f" \
    "\xdc\xfb\xcb\xee\xf9\x18\x2d\x54\x98\xfa\xfb\xf8" \
    "\xce\xe7\xb3\x3c\x53\x27\x97\x1b\x73\xd1\xd0\xbd" \
    "\x87\x7f\x64\xf7\x9e\x4f\x57\xd3\xd0\xba\x83\x40" \
    "\x8e\x6f\xd8\x81\xfa\x53\x97\x76\x85\xf3\x83\x94" \
    "\x6d\x2b\xe6\x81\xec\xd6\xa6\x86\x31\xcf\x39\x75" \
    "\x1a\x62\xa0\x5a\xab\x12\x35\x92\x58\x42\x9e\xe7" \
    "\xe4\x31\x07\xa0\xa9\xdc\x04\x8d\x63\xbe\xa2\xdc" \
    "\xb8\x89\x20\x60\x0e\x82\xfd\x4f\xbb\x99\x32\x04" \
    "\xdc\x10\x42\x90\x48\xe4\xce\x89\x73\xd9\xfa\xd8" \
    "\x16\x9c\x3a\x54\x95\x5a\xcc\x99\x75\xcd\x2c\x00" \
    "\xb2\x3c\x03\xac\x11\x89\x20\x0e\xfe\x33\x8c\x46" \
    "\x01\x27\x45\xd2\x95\x7a\x4f\x9e\x39\xf1\xc7\xba" \
    "\xaf\xd7\x77\x76\x77\x2d\xe6\x81\xa9\x0f\x11\xcd" \
    "\xc0\x0c\x11\xa5\x1e\xeb\x6c\xfa\x66\x0b\x3f\xf4" \
    "\x7d\x37\x48\xa9\x71\x07\xaa\xc5\xcb\x5e\x65\x18" \
    "\x5c\xcc\x0c\x59\x92\x14\xef\xe9\xf0\x68\x12\xa8" \
    "\xd7\xee\x49\x49\xde\xbf\x69\xfc\x8c\x89\x89\x2f" \
    "\x63\x61\x68\xfc\x50\xfc\xee\xd1\x93\xc7\xce\x9d" \
    "\xaf\x54\x96\xe3\xd3\x75\xc3\xc4\xa2\x14\x53\x6a" \
    "\xdb\xc9\x02\xf8\x4a\xc4\xbf\x3d\x8d\xe5\xe8\xfa" \
    "\x47\xc8\x17\x00\x00\x00\x00\x49\x45\x4e\x44\xae" \
    "\x42\x60\x82"

class GDebiKDE(QDialog):
    def __init__(self,datadir,options,file="",parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        self.image1 = QPixmap()
        self.image1.loadFromData(image1_data,"PNG")
        if not name:
            self.setName("GDebiKDE")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setIcon(self.image0)
        self.setSizeGripEnabled(0)


        LayoutWidget = QWidget(self,"Layout1")
        LayoutWidget.setGeometry(QRect(20,287,476,33))
        Layout1 = QHBoxLayout(LayoutWidget,0,6,"Layout1")

        self.buttonHelp = QPushButton(LayoutWidget,"buttonHelp")
        self.buttonHelp.setAutoDefault(1)
        Layout1.addWidget(self.buttonHelp)
        Horizontal_Spacing2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)

        self.buttonOk = QPushButton(LayoutWidget,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        self.buttonOk.setIconSet(QIconSet(self.image1))
        Layout1.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(LayoutWidget,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout1.addWidget(self.buttonCancel)

        LayoutWidget_2 = QWidget(self,"layout4")
        LayoutWidget_2.setGeometry(QRect(30,10,130,50))
        layout4 = QGridLayout(LayoutWidget_2,1,1,11,6,"layout4")

        self.textLabel1_2 = QLabel(LayoutWidget_2,"textLabel1_2")

        layout4.addWidget(self.textLabel1_2,1,0)

        self.textLabel1 = QLabel(LayoutWidget_2,"textLabel1")

        layout4.addWidget(self.textLabel1,0,0)

        self.textLabel1_3 = QLabel(LayoutWidget_2,"textLabel1_3")

        layout4.addWidget(self.textLabel1_3,0,1)

        self.textLabel1_3_2 = QLabel(LayoutWidget_2,"textLabel1_3_2")

        layout4.addWidget(self.textLabel1_3_2,1,1)

        self.PackageProgressBar = QProgressBar(self,"PackageProgressBar")
        self.PackageProgressBar.setGeometry(QRect(402,10,110,25))

        self.tabWidget2 = QTabWidget(self,"tabWidget2")
        self.tabWidget2.setGeometry(QRect(30,80,430,190))

        self.tab = QWidget(self.tabWidget2,"tab")

        self.DecriptionEdit = QTextEdit(self.tab,"DecriptionEdit")
        self.DecriptionEdit.setGeometry(QRect(3,3,420,130))
        self.DecriptionEdit.setReadOnly(1)
        self.tabWidget2.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")

        LayoutWidget_3 = QWidget(self.tab_2,"layout3")
        LayoutWidget_3.setGeometry(QRect(0,10,200,140))
        layout3 = QGridLayout(LayoutWidget_3,1,1,11,6,"layout3")

        self.DetailsSectionLabel = QLabel(LayoutWidget_3,"DetailsSectionLabel")
        DetailsSectionLabel_font = QFont(self.DetailsSectionLabel.font())
        DetailsSectionLabel_font.setBold(1)
        self.DetailsSectionLabel.setFont(DetailsSectionLabel_font)

        layout3.addWidget(self.DetailsSectionLabel,3,0)

        self.DetailsPriorityLabel = QLabel(LayoutWidget_3,"DetailsPriorityLabel")
        DetailsPriorityLabel_font = QFont(self.DetailsPriorityLabel.font())
        DetailsPriorityLabel_font.setBold(1)
        self.DetailsPriorityLabel.setFont(DetailsPriorityLabel_font)

        layout3.addWidget(self.DetailsPriorityLabel,2,0)

        self.DetailsPriority = QLabel(LayoutWidget_3,"DetailsPriority")

        layout3.addWidget(self.DetailsPriority,2,1)

        self.DetailsSection = QLabel(LayoutWidget_3,"DetailsSection")

        layout3.addWidget(self.DetailsSection,3,1)

        self.DetailsVersionLabel = QLabel(LayoutWidget_3,"DetailsVersionLabel")
        DetailsVersionLabel_font = QFont(self.DetailsVersionLabel.font())
        DetailsVersionLabel_font.setBold(1)
        self.DetailsVersionLabel.setFont(DetailsVersionLabel_font)

        layout3.addWidget(self.DetailsVersionLabel,0,0)

        self.DetailsSize = QLabel(LayoutWidget_3,"DetailsSize")

        layout3.addWidget(self.DetailsSize,4,1)

        self.DetailsVersion = QLabel(LayoutWidget_3,"DetailsVersion")

        layout3.addWidget(self.DetailsVersion,0,1)

        self.DetailsSizeLabel = QLabel(LayoutWidget_3,"DetailsSizeLabel")
        DetailsSizeLabel_font = QFont(self.DetailsSizeLabel.font())
        DetailsSizeLabel_font.setBold(1)
        self.DetailsSizeLabel.setFont(DetailsSizeLabel_font)

        layout3.addWidget(self.DetailsSizeLabel,4,0)

        self.DetailsMaintainer = QLabel(LayoutWidget_3,"DetailsMaintainer")

        layout3.addWidget(self.DetailsMaintainer,1,1)

        self.DetailsMaintainerLabel = QLabel(LayoutWidget_3,"DetailsMaintainerLabel")
        DetailsMaintainerLabel_font = QFont(self.DetailsMaintainerLabel.font())
        DetailsMaintainerLabel_font.setBold(1)
        self.DetailsMaintainerLabel.setFont(DetailsMaintainerLabel_font)

        layout3.addWidget(self.DetailsMaintainerLabel,1,0)
        self.tabWidget2.insertTab(self.tab_2,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabWidget2,"TabPage")

        self.IncFilesEdit = QTextEdit(self.TabPage,"IncFilesEdit")
        self.IncFilesEdit.setGeometry(QRect(3,3,420,130))
        self.IncFilesEdit.setReadOnly(1)
        self.tabWidget2.insertTab(self.TabPage,QString.fromLatin1(""))

        self.languageChange()

        self.resize(QSize(529,340).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self.installButtonClicked)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)
        self.show()
	# end autogenerated stuff
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
            self.textLabel1_3_2.set_markup("<span foreground=\"red\" weight=\"bold\">"+
                                         "Error: " +
                                         self._deb._failureString +
                                         "</span>")
	    self.button_install.set_label(_("_Install Package"))

            self.button_install.set_sensitive(False)
            self.button_details.hide()
            return

        if self._deb.compareToVersionInCache() == DebPackage.VERSION_SAME:
            self.textLabel1_3_2.setText(_("Same version is already installed"))
            self.buttonOk.setLabel(_("_Reinstall Package"))
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
	

    def installButtonClicked(self):
        
        print "click" # mhb debug
        # sanity check
        if self._deb is None:
            return
        # do it
        # set the window as disabled
        self.setDisabled(True)
        # if not root, start a new instance
        if os.getuid() != 0:
            os.execl("/usr/bin/kdesu", "kdesu",
                     "/home/martin/processing/projects/soc/gdebi-kde/branch/gdebi-kde/gdebi-kde -n " + self._deb.file)
        # check if we can lock the apt database
        try:
            apt_pkg.PkgSystemLock()
        except SystemError:
            print "cannot be locked" # mhb debug
        apt_pkg.PkgSystemUnLock()
        installDialog = GDebiKDEInstallDialog(self)
        installDialog.show()
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
                                             installDialog.installingLabel,
                                             installDialog.installationProgres,
                                             None,
                                             None)
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


    def languageChange(self):
        self.setCaption(self.__tr("Package Installer"))
        self.buttonHelp.setText(self.__tr("&Help"))
        self.buttonHelp.setAccel(QKeySequence(self.__tr("F1")))
        self.buttonOk.setText(self.__tr("&Install"))
        self.buttonOk.setAccel(QKeySequence(self.__tr("Alt+I")))
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(QKeySequence(QString.null))
        self.textLabel1_2.setText(self.__tr("Status:"))
        self.textLabel1.setText(self.__tr("Package:"))
        self.textLabel1_3.setText(self.__tr("empty"))
        self.textLabel1_3_2.setText(self.__tr("empty"))
        self.tabWidget2.changeTab(self.tab,self.__tr("Description"))
        self.DetailsSectionLabel.setText(self.__tr("Section:"))
        self.DetailsPriorityLabel.setText(self.__tr("Priority:"))
        self.DetailsPriority.setText(QString.null)
        self.DetailsSection.setText(QString.null)
        self.DetailsVersionLabel.setText(self.__tr("Version:"))
        self.DetailsSize.setText(QString.null)
        self.DetailsVersion.setText(QString.null)
        self.DetailsSizeLabel.setText(self.__tr("Size:"))
        self.DetailsMaintainer.setText(QString.null)
        self.DetailsMaintainerLabel.setText(self.__tr("Maintainer:"))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Details"))
        self.tabWidget2.changeTab(self.TabPage,self.__tr("Included Files"))


    def __tr(self,s,c = None):
        return qApp.translate("GDebiKDE",s,c)
    # embedded classes
    class DpkgInstallProgress(object):
        def __init__(self, debfile, status, progress, term, expander):
            self.debfile = debfile
            self.status = status
            self.progress = progress
            self.term = term
            self.expander = expander
            #self.expander.set_expanded(False)
        
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
            self.status.setText("<i>"+_("Installing '%s'...") % \
                                   os.path.basename(self.debfile)+"</i>")
            #self.progress.pulse()
            #self.progress.set_text("")

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
            #reaper = vte.reaper_get()
            #signal_id = reaper.connect("child-exited", finish_dpkg, lock)
            #pid = self.term.fork_command(command=cmd, argv=argv, envv=env)
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
            self.progress.setPercent(1.0)
            reaper.disconnect(signal_id)
    
    class InstallProgressAdapter(InstallProgress):
        def __init__(self,progress,term,label,term_expander):
            # TODO: implement the term
            InstallProgress.__init__(self)
            self.progress = progress
            self.term = term
            self.term_expander = term_expander
            self.finished = False
            self.action = label
            #reaper = vte.reaper_get()
            #reaper.connect("child-exited",self.child_exited)
            #self.env = ["VTE_PTY_KEEP_FD=%s"% self.writefd,
                        #"DEBIAN_FRONTEND=gnome",
                        #"APT_LISTCHANGES_FRONTEND=gtk"]
        def child_exited(self,term, pid, status):
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
            #return self.term.forkpty(envv=self.env)
            pass
        def waitChild(self):
            #while not self.finished:
                #self.updateInterface()
            #return self.apt_status
            pass
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


class GDebiKDEInstallDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("installDialog")

        LayoutWidget = QWidget(self,"layout6")
        LayoutWidget.setGeometry(QRect(7,14,490,53))
        layout6 = QVBoxLayout(LayoutWidget,11,6,"layout6")

        self.installingLabel = QLabel(LayoutWidget,"installingLabel")
        layout6.addWidget(self.installingLabel)

        layout5 = QHBoxLayout(None,0,6,"layout5")

        self.installationProgres = QProgressBar(LayoutWidget,"installationProgres")
        layout5.addWidget(self.installationProgres)

        self.showDetailsButton = QPushButton(LayoutWidget,"showDetailsButton")
        layout5.addWidget(self.showDetailsButton)
        layout6.addLayout(layout5)

        self.languageChange()

        self.resize(QSize(515,82).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Installing"))
        self.installingLabel.setText(self.__tr("Installing..."))
        self.showDetailsButton.setText(self.__tr("Show Details"))
        self.showDetailsButton.setAccel(QKeySequence(QString.null))


    def __tr(self,s,c = None):
        return qApp.translate("installDialog",s,c)
    def newKonsole(self):
        if self.konsole is not None:
            self.konsole.widget().hide()
        self.konsole = konsolePart(self.window_main.konsole_frame, "konsole", self.window_main.konsole_frame, "konsole")
        self.window_main.konsole_frame.setMinimumSize(500, 400)
        self.konsole.setAutoStartShell(False)
        self.konsoleWidget = self.konsole.widget()
        self.konsole_frame_layout.addWidget(self.konsoleWidget)
        self.konsoleWidget.show()

        #prepare for dpkg pty being attached to konsole
        (self.master, self.slave) = pty.openpty()
        self.konsole.setPtyFd(self.master)

        self.window_main.showTerminalButton.setEnabled(True)
    
    def showTerminal(self):
        if self.konsole_frame.isVisible():
            self.konsole_frame.hide()
            self.showTerminalButton.setText(_("Show Terminal"))
        else:
            self.konsole_frame.show()
            self.showTerminalButton.setText(_("Hide Terminal"))
