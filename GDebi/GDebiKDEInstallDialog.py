# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './GDebiKDEInstallDialog.ui'
#
# Created: Čt kvě 31 01:39:46 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


from qt import *


class GDebiKDEInstallDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("GDebiKDEInstallDialog")



        self.konsoleFrame = QFrame(self,"konsoleFrame")
        self.konsoleFrame.setGeometry(QRect(10,100,481,1))
        self.konsoleFrame.setFrameShape(QFrame.StyledPanel)
        self.konsoleFrame.setFrameShadow(QFrame.Raised)

        LayoutWidget = QWidget(self,"layout6")
        LayoutWidget.setGeometry(QRect(10,20,490,53))
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

        self.resize(QSize(525,167).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Installing"))
        self.installingLabel.setText(self.__tr("Installing..."))
        self.showDetailsButton.setText(self.__tr("Show &Details"))
        self.showDetailsButton.setAccel(QKeySequence(self.__tr("Alt+D")))


    def __tr(self,s,c = None):
        return qApp.translate("GDebiKDEInstallDialog",s,c)
