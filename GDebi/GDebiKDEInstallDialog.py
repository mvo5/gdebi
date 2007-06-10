# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './GDebiKDEInstallDialog.ui'
#
# Created: So čen 9 02:35:32 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


from qt import *


class GDebiKDEInstallDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("GDebiKDEInstallDialog")



        LayoutWidget = QWidget(self,"layout2")
        LayoutWidget.setGeometry(QRect(9,20,490,70))
        layout2 = QVBoxLayout(LayoutWidget,11,6,"layout2")

        self.installingLabel = QLabel(LayoutWidget,"installingLabel")
        layout2.addWidget(self.installingLabel)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.installationProgres = QProgressBar(LayoutWidget,"installationProgres")
        layout3.addWidget(self.installationProgres)

        self.showDetailsButton = QPushButton(LayoutWidget,"showDetailsButton")
        layout3.addWidget(self.showDetailsButton)
        layout2.addLayout(layout3)

        self.konsoleFrame = QFrame(self,"konsoleFrame")
        self.konsoleFrame.setGeometry(QRect(10,100,481,1))
        self.konsoleFrame.setFrameShape(QFrame.StyledPanel)
        self.konsoleFrame.setFrameShadow(QFrame.Raised)

        self.languageChange()

        self.resize(QSize(525,167).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.showDetailsButton,SIGNAL("clicked()"),self.showTerminal)


    def languageChange(self):
        self.setCaption(self.__tr("Installing"))
        self.installingLabel.setText(self.__tr("Installing..."))
        self.showDetailsButton.setText(self.__tr("Show &Details"))
        self.showDetailsButton.setAccel(QKeySequence(self.__tr("Alt+D")))


    def showDetailsButton_clicked(self):
        print "GDebiKDEInstallDialog.showDetailsButton_clicked(): Not implemented yet"

    def showTerminal(self):
        print "GDebiKDEInstallDialog.showTerminal(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("GDebiKDEInstallDialog",s,c)
