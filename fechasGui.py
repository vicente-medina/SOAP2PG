# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\vicente\Desktop\bgeo\SOAP2PG\Fechas.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(483, 100)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 60, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBoxDesde = QtWidgets.QGroupBox(Dialog)
        self.groupBoxDesde.setGeometry(QtCore.QRect(10, 10, 221, 51))
        self.groupBoxDesde.setObjectName("groupBoxDesde")
        self.fechaDesde = QtWidgets.QDateTimeEdit(self.groupBoxDesde)
        self.fechaDesde.setGeometry(QtCore.QRect(20, 20, 194, 22))
        self.fechaDesde.setDateTime(QtCore.QDateTime(QtCore.QDate(2016, 7, 1), QtCore.QTime(0, 0, 0)))
        self.fechaDesde.setCalendarPopup(True)
        self.fechaDesde.setObjectName("fechaDesde")
        self.groupBoxHasta = QtWidgets.QGroupBox(Dialog)
        self.groupBoxHasta.setGeometry(QtCore.QRect(250, 10, 221, 51))
        self.groupBoxHasta.setObjectName("groupBoxHasta")
        self.fechaHasta = QtWidgets.QDateTimeEdit(self.groupBoxHasta)
        self.fechaHasta.setGeometry(QtCore.QRect(20, 20, 194, 22))
        self.fechaHasta.setDateTime(QtCore.QDateTime(QtCore.QDate(2016, 7, 1), QtCore.QTime(0, 0, 0)))
        self.fechaHasta.setCalendarPopup(True)
        self.fechaHasta.setObjectName("fechaHasta")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(QtCore.QCoreApplication.instance().quit)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "bgeo MOBA"))
        self.groupBoxDesde.setTitle(_translate("Dialog", "Fecha inicio"))
        self.fechaDesde.setDisplayFormat(_translate("Dialog", "dd/MM/yyyy hh:mm:ss"))
        self.groupBoxHasta.setTitle(_translate("Dialog", "Fecha final"))
        self.fechaHasta.setDisplayFormat(_translate("Dialog", "dd/MM/yyyy hh:mm:ss"))

