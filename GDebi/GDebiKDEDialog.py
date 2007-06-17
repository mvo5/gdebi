# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gdebi-kde/GDebiKDEDialog.ui'
#
# Created: Ne čen 17 00:30:27 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from kdecore import *
from kdeui import *

class GDebiKDEDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("GDebiKDEDialog")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(0,0))
        self.setBaseSize(QSize(64,64))
        self.setIcon(KGlobal.iconLoader().loadIcon("adept_manager",KIcon.NoGroup,KIcon.SizeMedium))
        self.setSizeGripEnabled(0)

        GDebiKDEDialogLayout = QVBoxLayout(self,11,6,"GDebiKDEDialogLayout")

        layout14 = QVBoxLayout(None,0,6,"layout14")

        layout6 = QHBoxLayout(None,0,6,"layout6")

        layout4 = QGridLayout(None,1,1,0,6,"layout4")

        self.textLabel1_2 = QLabel(self,"textLabel1_2")
        self.textLabel1_2.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.textLabel1_2.sizePolicy().hasHeightForWidth()))

        layout4.addWidget(self.textLabel1_2,1,0)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setMaximumSize(QSize(80,32767))

        layout4.addWidget(self.textLabel1,0,0)

        self.textLabel1_3 = QLabel(self,"textLabel1_3")
        self.textLabel1_3.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.textLabel1_3.sizePolicy().hasHeightForWidth()))

        layout4.addWidget(self.textLabel1_3,0,1)

        self.textLabel1_3_2 = QLabel(self,"textLabel1_3_2")
        self.textLabel1_3_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.textLabel1_3_2.sizePolicy().hasHeightForWidth()))

        layout4.addWidget(self.textLabel1_3_2,1,1)
        layout6.addLayout(layout4)

        self.PackageProgressBar = QProgressBar(self,"PackageProgressBar")
        self.PackageProgressBar.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.PackageProgressBar.sizePolicy().hasHeightForWidth()))
        layout6.addWidget(self.PackageProgressBar)
        layout14.addLayout(layout6)
        spacer3 = QSpacerItem(20,15,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout14.addItem(spacer3)

        self.tabWidget2 = QTabWidget(self,"tabWidget2")
        self.tabWidget2.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,160,0,self.tabWidget2.sizePolicy().hasHeightForWidth()))

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
        layout14.addWidget(self.tabWidget2)

        layout6_2 = QHBoxLayout(None,0,6,"layout6_2")
        spacer5 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout6_2.addItem(spacer5)

        self.infoIcon = QLabel(self,"infoIcon")
        self.infoIcon.setEnabled(1)
        self.infoIcon.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.infoIcon.sizePolicy().hasHeightForWidth()))
        self.infoIcon.setMaximumSize(QSize(32,32))
        self.infoIcon.setScaledContents(1)
        layout6_2.addWidget(self.infoIcon)

        self.infoBox = QLabel(self,"infoBox")
        self.infoBox.setEnabled(1)
        layout6_2.addWidget(self.infoBox)
        spacer4 = QSpacerItem(51,31,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout6_2.addItem(spacer4)
        layout14.addLayout(layout6_2)
        spacer2 = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout14.addItem(spacer2)

        layout11 = QHBoxLayout(None,0,6,"layout11")
        Horizontal_Spacing2_2 = QSpacerItem(360,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(Horizontal_Spacing2_2)

        self.installButton = KPushButton(self,"installButton")
        layout11.addWidget(self.installButton)

        self.cancelButton = KPushButton(self,"cancelButton")
        layout11.addWidget(self.cancelButton)
        layout14.addLayout(layout11)
        GDebiKDEDialogLayout.addLayout(layout14)

        self.languageChange()

        self.resize(QSize(622,350).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.installButton,SIGNAL("clicked()"),self.installButtonClicked)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.cancelButtonClicked)


    def languageChange(self):
        self.setCaption(self.__tr("Package Installer"))
        self.textLabel1_2.setText(self.__tr("Status:"))
        self.textLabel1.setText(self.__tr("Package:"))
        self.textLabel1_3.setText(self.__tr("empty"))
        self.textLabel1_3_2.setText(self.__tr("empty"))
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
