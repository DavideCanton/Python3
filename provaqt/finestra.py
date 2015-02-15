# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'finestra.ui'
#
# Created: Wed Feb 12 15:51:04 2014
#      by: PyQt5 UI code generator 5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_finestra(object):
    def setupUi(self, finestra):
        finestra.setObjectName("finestra")
        finestra.resize(405, 47)
        self.centralwidget = QtWidgets.QWidget(finestra)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 385, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_edit = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_edit.sizePolicy().hasHeightForWidth())
        self.name_edit.setSizePolicy(sizePolicy)
        self.name_edit.setObjectName("name_edit")
        self.horizontalLayout.addWidget(self.name_edit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saluta = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.saluta.setObjectName("saluta")
        self.horizontalLayout.addWidget(self.saluta)
        finestra.setCentralWidget(self.centralwidget)

        self.retranslateUi(finestra)
        QtCore.QMetaObject.connectSlotsByName(finestra)

    def retranslateUi(self, finestra):
        _translate = QtCore.QCoreApplication.translate
        finestra.setWindowTitle(_translate("finestra", "MainWindow"))
        self.saluta.setText(_translate("finestra", "Click!"))

