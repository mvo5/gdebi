# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GDebiKDEDialog.ui'
#
# Created: Út čen 19 18:53:40 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from kdecore import KCmdLineArgs, KApplication
from kdeui import *


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

class GDebiKDEDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("GDebiKDEDialog")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(0,0))
        self.setBaseSize(QSize(64,64))
        self.setIcon(self.image0)
        self.setSizeGripEnabled(0)

        GDebiKDEDialogLayout = QVBoxLayout(self,11,6,"GDebiKDEDialogLayout")

        layout18 = QHBoxLayout(None,0,6,"layout18")

        layout17 = QGridLayout(None,1,1,0,6,"layout17")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setMaximumSize(QSize(80,32767))

        layout17.addWidget(self.textLabel1,0,0)

        self.textLabel1_3 = QLabel(self,"textLabel1_3")
        self.textLabel1_3.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Fixed,0,0,self.textLabel1_3.sizePolicy().hasHeightForWidth()))

        layout17.addWidget(self.textLabel1_3,0,1)

        layout15 = QHBoxLayout(None,0,6,"layout15")

        self.textLabel1_3_2 = QLabel(self,"textLabel1_3_2")
        self.textLabel1_3_2.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel1_3_2.sizePolicy().hasHeightForWidth()))
        layout15.addWidget(self.textLabel1_3_2)
        spacer7 = QSpacerItem(31,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout15.addItem(spacer7)

        self.detailsButton = KPushButton(self,"detailsButton")
        self.detailsButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum,0,0,self.detailsButton.sizePolicy().hasHeightForWidth()))
        layout15.addWidget(self.detailsButton)
        spacer6 = QSpacerItem(310,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout15.addItem(spacer6)

        layout17.addLayout(layout15,1,1)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")
        self.textLabel1_2.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.textLabel1_2.sizePolicy().hasHeightForWidth()))

        layout17.addWidget(self.textLabel1_2,1,0)
        layout18.addLayout(layout17)

        self.PackageProgressBar = QProgressBar(self,"PackageProgressBar")
        self.PackageProgressBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.PackageProgressBar.sizePolicy().hasHeightForWidth()))
        layout18.addWidget(self.PackageProgressBar)
        GDebiKDEDialogLayout.addLayout(layout18)
        spacer3 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        GDebiKDEDialogLayout.addItem(spacer3)

        self.tabWidget2 = QTabWidget(self,"tabWidget2")
        self.tabWidget2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,160,0,self.tabWidget2.sizePolicy().hasHeightForWidth()))

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QHBoxLayout(self.tab,11,6,"tabLayout")

        self.DecriptionEdit = QTextEdit(self.tab,"DecriptionEdit")
        self.DecriptionEdit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.DecriptionEdit.sizePolicy().hasHeightForWidth()))
        self.DecriptionEdit.setReadOnly(1)
        tabLayout.addWidget(self.DecriptionEdit)
        self.tabWidget2.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QHBoxLayout(self.tab_2,11,6,"tabLayout_2")

        layout3 = QGridLayout(None,1,1,0,6,"layout3")

        self.DetailsSectionLabel = QLabel(self.tab_2,"DetailsSectionLabel")
        self.DetailsSectionLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsSectionLabel.sizePolicy().hasHeightForWidth()))
        DetailsSectionLabel_font = QFont(self.DetailsSectionLabel.font())
        DetailsSectionLabel_font.setBold(1)
        self.DetailsSectionLabel.setFont(DetailsSectionLabel_font)

        layout3.addWidget(self.DetailsSectionLabel,3,0)

        self.DetailsPriorityLabel = QLabel(self.tab_2,"DetailsPriorityLabel")
        self.DetailsPriorityLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsPriorityLabel.sizePolicy().hasHeightForWidth()))
        DetailsPriorityLabel_font = QFont(self.DetailsPriorityLabel.font())
        DetailsPriorityLabel_font.setBold(1)
        self.DetailsPriorityLabel.setFont(DetailsPriorityLabel_font)

        layout3.addWidget(self.DetailsPriorityLabel,2,0)

        self.DetailsPriority = QLabel(self.tab_2,"DetailsPriority")

        layout3.addWidget(self.DetailsPriority,2,1)

        self.DetailsSection = QLabel(self.tab_2,"DetailsSection")

        layout3.addWidget(self.DetailsSection,3,1)

        self.DetailsVersionLabel = QLabel(self.tab_2,"DetailsVersionLabel")
        self.DetailsVersionLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsVersionLabel.sizePolicy().hasHeightForWidth()))
        DetailsVersionLabel_font = QFont(self.DetailsVersionLabel.font())
        DetailsVersionLabel_font.setBold(1)
        self.DetailsVersionLabel.setFont(DetailsVersionLabel_font)

        layout3.addWidget(self.DetailsVersionLabel,0,0)

        self.DetailsSize = QLabel(self.tab_2,"DetailsSize")

        layout3.addWidget(self.DetailsSize,4,1)

        self.DetailsVersion = QLabel(self.tab_2,"DetailsVersion")

        layout3.addWidget(self.DetailsVersion,0,1)

        self.DetailsSizeLabel = QLabel(self.tab_2,"DetailsSizeLabel")
        self.DetailsSizeLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsSizeLabel.sizePolicy().hasHeightForWidth()))
        DetailsSizeLabel_font = QFont(self.DetailsSizeLabel.font())
        DetailsSizeLabel_font.setBold(1)
        self.DetailsSizeLabel.setFont(DetailsSizeLabel_font)

        layout3.addWidget(self.DetailsSizeLabel,4,0)

        self.DetailsMaintainer = QLabel(self.tab_2,"DetailsMaintainer")

        layout3.addWidget(self.DetailsMaintainer,1,1)

        self.DetailsMaintainerLabel = QLabel(self.tab_2,"DetailsMaintainerLabel")
        self.DetailsMaintainerLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsMaintainerLabel.sizePolicy().hasHeightForWidth()))
        DetailsMaintainerLabel_font = QFont(self.DetailsMaintainerLabel.font())
        DetailsMaintainerLabel_font.setBold(1)
        self.DetailsMaintainerLabel.setFont(DetailsMaintainerLabel_font)

        layout3.addWidget(self.DetailsMaintainerLabel,1,0)
        tabLayout_2.addLayout(layout3)
        self.tabWidget2.insertTab(self.tab_2,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabWidget2,"TabPage")
        TabPageLayout = QHBoxLayout(self.TabPage,11,6,"TabPageLayout")

        self.IncFilesEdit = QTextEdit(self.TabPage,"IncFilesEdit")
        self.IncFilesEdit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.IncFilesEdit.sizePolicy().hasHeightForWidth()))
        self.IncFilesEdit.setReadOnly(1)
        TabPageLayout.addWidget(self.IncFilesEdit)
        self.tabWidget2.insertTab(self.TabPage,QString.fromLatin1(""))
        GDebiKDEDialogLayout.addWidget(self.tabWidget2)

        layout6 = QHBoxLayout(None,0,6,"layout6")
        spacer5 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout6.addItem(spacer5)

        self.infoIcon = QLabel(self,"infoIcon")
        self.infoIcon.setEnabled(1)
        self.infoIcon.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.infoIcon.sizePolicy().hasHeightForWidth()))
        self.infoIcon.setMaximumSize(QSize(32,32))
        self.infoIcon.setScaledContents(1)
        layout6.addWidget(self.infoIcon)

        self.infoBox = QLabel(self,"infoBox")
        self.infoBox.setEnabled(1)
        layout6.addWidget(self.infoBox)
        spacer4 = QSpacerItem(51,31,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout6.addItem(spacer4)
        GDebiKDEDialogLayout.addLayout(layout6)
        spacer2 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        GDebiKDEDialogLayout.addItem(spacer2)

        layout11 = QHBoxLayout(None,0,6,"layout11")
        Horizontal_Spacing2_2 = QSpacerItem(360,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(Horizontal_Spacing2_2)

        self.installButton = KPushButton(self,"installButton")
        layout11.addWidget(self.installButton)

        self.cancelButton = KPushButton(self,"cancelButton")
        layout11.addWidget(self.cancelButton)
        GDebiKDEDialogLayout.addLayout(layout11)

        self.languageChange()

        self.resize(QSize(702,377).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.installButton,SIGNAL("clicked()"),self.installButtonClicked)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.cancelButtonClicked)


    def languageChange(self):
        self.setCaption(self.__tr("Package Installer"))
        self.textLabel1.setText(self.__tr("Package:"))
        self.textLabel1_3.setText(self.__tr("empty"))
        self.textLabel1_3_2.setText(self.__tr("empty"))
        self.detailsButton.setText(self.__tr("Details"))
        self.textLabel1_2.setText(self.__tr("Status:"))
        self.tabWidget2.changeTab(self.tab,self.__tr("&Description"))
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
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Det&ails"))
        self.tabWidget2.changeTab(self.TabPage,self.__tr("I&ncluded Files"))
        self.infoBox.setText(QString.null)
        self.installButton.setText(self.__tr("&Install"))
        self.installButton.setAccel(QKeySequence(self.__tr("Alt+I")))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(QKeySequence(self.__tr("Alt+C")))


    def buttonCancelClicked(self):
        print "GDebiKDEDialog.buttonCancelClicked(): Not implemented yet"

    def cancelButtonclicked(self):
        print "GDebiKDEDialog.cancelButtonclicked(): Not implemented yet"

    def cancelButtonClicked(self):
        print "GDebiKDEDialog.cancelButtonClicked(): Not implemented yet"

    def installButtonClicked(self):
        print "GDebiKDEDialog.installButtonClicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("GDebiKDEDialog",s,c)

if __name__ == "__main__":
    appname     = ""
    description = ""
    version     = ""

    KCmdLineArgs.init (sys.argv, appname, description, version)
    a = KApplication ()

    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = GDebiKDEDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
