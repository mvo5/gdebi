# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../data/GDebiKDEInstallDialog.ui'
#
# Created: Pá čen 22 14:29:09 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from kdecore import KCmdLineArgs, KApplication
from kdeui import *



class GDebiKDEInstallDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("GDebiKDEInstallDialog")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))

        GDebiKDEInstallDialogLayout = QVBoxLayout(self,11,6,"GDebiKDEInstallDialogLayout")

        layout2 = QVBoxLayout(None,0,6,"layout2")

        self.installingLabel = QLabel(self,"installingLabel")
        self.installingLabel.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Maximum,0,0,self.installingLabel.sizePolicy().hasHeightForWidth()))
        layout2.addWidget(self.installingLabel)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.installationProgres = QProgressBar(self,"installationProgres")
        layout3.addWidget(self.installationProgres)

        self.showDetailsButton = QPushButton(self,"showDetailsButton")
        layout3.addWidget(self.showDetailsButton)
        layout2.addLayout(layout3)
        GDebiKDEInstallDialogLayout.addLayout(layout2)

        self.konsoleFrame = QFrame(self,"konsoleFrame")
        self.konsoleFrame.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.konsoleFrame.sizePolicy().hasHeightForWidth()))
        self.konsoleFrame.setFrameShape(QFrame.StyledPanel)
        self.konsoleFrame.setFrameShadow(QFrame.Raised)
        GDebiKDEInstallDialogLayout.addWidget(self.konsoleFrame)

        layout10 = QHBoxLayout(None,0,6,"layout10")
        spacer6 = QSpacerItem(291,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout10.addItem(spacer6)

        self.closeButton = QPushButton(self,"closeButton")
        layout10.addWidget(self.closeButton)
        GDebiKDEInstallDialogLayout.addLayout(layout10)

        self.languageChange()

        self.resize(QSize(442,110).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.showDetailsButton,SIGNAL("clicked()"),self.showTerminal)
        self.connect(self.closeButton,SIGNAL("clicked()"),self.closeButtonClicked)


    def languageChange(self):
        self.setCaption(self.__tr("Installing"))
        self.installingLabel.setText(QString.null)
        self.showDetailsButton.setText(QString.null)
        self.showDetailsButton.setAccel(QKeySequence(QString.null))
        self.closeButton.setText(QString.null)
        self.closeButton.setAccel(QKeySequence(QString.null))


    def showDetailsButton_clicked(self):
        print "GDebiKDEInstallDialog.showDetailsButton_clicked(): Not implemented yet"

    def showTerminal(self):
        print "GDebiKDEInstallDialog.showTerminal(): Not implemented yet"

    def closeButtonClicked(self):
        print "GDebiKDEInstallDialog.closeButtonClicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("GDebiKDEInstallDialog",s,c)

if __name__ == "__main__":
    appname     = ""
    description = ""
    version     = ""

    KCmdLineArgs.init (sys.argv, appname, description, version)
    a = KApplication ()

    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = GDebiKDEInstallDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
