# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../data/GDebiKDEDialog.ui'
#
# Created: Pá čen 22 12:16:53 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from kdecore import KCmdLineArgs, KApplication
from kdeui import *



class GDebiKDEDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("GDebiKDEDialog")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(0,0))
        self.setBaseSize(QSize(64,64))
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

        self.desc = QWidget(self.tabWidget2,"desc")
        descLayout = QHBoxLayout(self.desc,11,6,"descLayout")

        self.DecriptionEdit = QTextEdit(self.desc,"DecriptionEdit")
        self.DecriptionEdit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.DecriptionEdit.sizePolicy().hasHeightForWidth()))
        self.DecriptionEdit.setReadOnly(1)
        descLayout.addWidget(self.DecriptionEdit)
        self.tabWidget2.insertTab(self.desc,QString.fromLatin1(""))

        self.det = QWidget(self.tabWidget2,"det")
        detLayout = QHBoxLayout(self.det,11,6,"detLayout")

        layout3 = QGridLayout(None,1,1,0,6,"layout3")

        self.DetailsSectionLabel = QLabel(self.det,"DetailsSectionLabel")
        self.DetailsSectionLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsSectionLabel.sizePolicy().hasHeightForWidth()))
        DetailsSectionLabel_font = QFont(self.DetailsSectionLabel.font())
        DetailsSectionLabel_font.setBold(1)
        self.DetailsSectionLabel.setFont(DetailsSectionLabel_font)

        layout3.addWidget(self.DetailsSectionLabel,3,0)

        self.DetailsPriorityLabel = QLabel(self.det,"DetailsPriorityLabel")
        self.DetailsPriorityLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsPriorityLabel.sizePolicy().hasHeightForWidth()))
        DetailsPriorityLabel_font = QFont(self.DetailsPriorityLabel.font())
        DetailsPriorityLabel_font.setBold(1)
        self.DetailsPriorityLabel.setFont(DetailsPriorityLabel_font)

        layout3.addWidget(self.DetailsPriorityLabel,2,0)

        self.DetailsPriority = QLabel(self.det,"DetailsPriority")

        layout3.addWidget(self.DetailsPriority,2,1)

        self.DetailsSection = QLabel(self.det,"DetailsSection")

        layout3.addWidget(self.DetailsSection,3,1)

        self.DetailsVersionLabel = QLabel(self.det,"DetailsVersionLabel")
        self.DetailsVersionLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsVersionLabel.sizePolicy().hasHeightForWidth()))
        DetailsVersionLabel_font = QFont(self.DetailsVersionLabel.font())
        DetailsVersionLabel_font.setBold(1)
        self.DetailsVersionLabel.setFont(DetailsVersionLabel_font)

        layout3.addWidget(self.DetailsVersionLabel,0,0)

        self.DetailsSize = QLabel(self.det,"DetailsSize")

        layout3.addWidget(self.DetailsSize,4,1)

        self.DetailsVersion = QLabel(self.det,"DetailsVersion")

        layout3.addWidget(self.DetailsVersion,0,1)

        self.DetailsSizeLabel = QLabel(self.det,"DetailsSizeLabel")
        self.DetailsSizeLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsSizeLabel.sizePolicy().hasHeightForWidth()))
        DetailsSizeLabel_font = QFont(self.DetailsSizeLabel.font())
        DetailsSizeLabel_font.setBold(1)
        self.DetailsSizeLabel.setFont(DetailsSizeLabel_font)

        layout3.addWidget(self.DetailsSizeLabel,4,0)

        self.DetailsMaintainer = QLabel(self.det,"DetailsMaintainer")

        layout3.addWidget(self.DetailsMaintainer,1,1)

        self.DetailsMaintainerLabel = QLabel(self.det,"DetailsMaintainerLabel")
        self.DetailsMaintainerLabel.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum,0,0,self.DetailsMaintainerLabel.sizePolicy().hasHeightForWidth()))
        DetailsMaintainerLabel_font = QFont(self.DetailsMaintainerLabel.font())
        DetailsMaintainerLabel_font.setBold(1)
        self.DetailsMaintainerLabel.setFont(DetailsMaintainerLabel_font)

        layout3.addWidget(self.DetailsMaintainerLabel,1,0)
        detLayout.addLayout(layout3)
        self.tabWidget2.insertTab(self.det,QString.fromLatin1(""))

        self.incl = QWidget(self.tabWidget2,"incl")
        inclLayout = QHBoxLayout(self.incl,11,6,"inclLayout")

        self.IncFilesEdit = QTextEdit(self.incl,"IncFilesEdit")
        self.IncFilesEdit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.IncFilesEdit.sizePolicy().hasHeightForWidth()))
        self.IncFilesEdit.setReadOnly(1)
        inclLayout.addWidget(self.IncFilesEdit)
        self.tabWidget2.insertTab(self.incl,QString.fromLatin1(""))
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
        self.connect(self.detailsButton,SIGNAL("clicked()"),self.detailsButtonClicked)


    def languageChange(self):
        self.setCaption(self.__tr("GDebiKDEDialog"))
        self.textLabel1.setText(QString.null)
        self.textLabel1_3.setText(QString.null)
        self.textLabel1_3_2.setText(QString.null)
        self.detailsButton.setText(QString.null)
        self.textLabel1_2.setText(QString.null)
        self.tabWidget2.changeTab(self.desc,QString.null)
        self.DetailsSectionLabel.setText(QString.null)
        self.DetailsPriorityLabel.setText(QString.null)
        self.DetailsPriority.setText(QString.null)
        self.DetailsSection.setText(QString.null)
        self.DetailsVersionLabel.setText(QString.null)
        self.DetailsSize.setText(QString.null)
        self.DetailsVersion.setText(QString.null)
        self.DetailsSizeLabel.setText(QString.null)
        self.DetailsMaintainer.setText(QString.null)
        self.DetailsMaintainerLabel.setText(QString.null)
        self.tabWidget2.changeTab(self.det,QString.null)
        self.tabWidget2.changeTab(self.incl,QString.null)
        self.infoBox.setText(QString.null)
        self.installButton.setText(QString.null)
        self.installButton.setAccel(QKeySequence(QString.null))
        self.cancelButton.setText(QString.null)
        self.cancelButton.setAccel(QKeySequence(QString.null))


    def buttonCancelClicked(self):
        print "GDebiKDEDialog.buttonCancelClicked(): Not implemented yet"

    def cancelButtonclicked(self):
        print "GDebiKDEDialog.cancelButtonclicked(): Not implemented yet"

    def cancelButtonClicked(self):
        print "GDebiKDEDialog.cancelButtonClicked(): Not implemented yet"

    def installButtonClicked(self):
        print "GDebiKDEDialog.installButtonClicked(): Not implemented yet"

    def detailsButtonClicked(self):
        print "GDebiKDEDialog.detailsButtonClicked(): Not implemented yet"

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
