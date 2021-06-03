# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_main.ui',
# licensing of 'gui_main.ui' applies.
#
# Created: Fri Jul 19 04:09:07 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(694, 354)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.ip_field = QtWidgets.QLineEdit(Form)
        self.ip_field.setObjectName("ip_field")
        self.verticalLayout.addWidget(self.ip_field)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.speed_field = QtWidgets.QLineEdit(Form)
        self.speed_field.setObjectName("speed_field")
        self.verticalLayout.addWidget(self.speed_field)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.name_field = QtWidgets.QLineEdit(Form)
        self.name_field.setObjectName("name_field")
        self.verticalLayout.addWidget(self.name_field)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.pasword_field = QtWidgets.QLineEdit(Form)
        self.pasword_field.setObjectName("pasword_field")
        self.verticalLayout.addWidget(self.pasword_field)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scunButton = QtWidgets.QPushButton(Form)
        self.scunButton.setObjectName("scunButton")
        self.verticalLayout.addWidget(self.scunButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.show_field = QtWidgets.QTextEdit(Form)
        self.show_field.setObjectName("show_field")
        self.verticalLayout_2.addWidget(self.show_field)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "IP", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Інтенсивність сканування (0.001 - 1)", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "І\'мя користувача", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Пароль", None, -1))
        self.scunButton.setText(QtWidgets.QApplication.translate("Form", "Сканувати", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "Знайдені папки", None, -1))

