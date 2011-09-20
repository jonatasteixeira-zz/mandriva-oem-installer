# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jonatas/oem-installer/SOURCES/oem-installer-0.9/script/../app/views/screen/show.ui'
#
# Created: Tue Aug  2 17:09:15 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ScreenShow(object):
    def setupUi(self, ScreenShow):
        ScreenShow.setObjectName("ScreenShow")
        ScreenShow.setWindowModality(QtCore.Qt.WindowModal)
        ScreenShow.resize(800, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScreenShow.sizePolicy().hasHeightForWidth())
        ScreenShow.setSizePolicy(sizePolicy)
        ScreenShow.setStyleSheet("QFrame#background {\n"
"    background-image: url(:/images/images/background.png);\n"
"}")
        self.background = QtGui.QFrame(ScreenShow)
        self.background.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.background.setFrameShape(QtGui.QFrame.StyledPanel)
        self.background.setFrameShadow(QtGui.QFrame.Raised)
        self.background.setObjectName("background")
        self.center = QtGui.QWidget(self.background)
        self.center.setGeometry(QtCore.QRect(200, 0, 600, 550))
        self.center.setObjectName("center")
        self.gridLayout_2 = QtGui.QGridLayout(self.center)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.global_progress_bar = QtGui.QProgressBar(self.center)
        self.global_progress_bar.setProperty("value", 0)
        self.global_progress_bar.setObjectName("global_progress_bar")
        self.gridLayout_2.addWidget(self.global_progress_bar, 3, 0, 1, 1)
        self.line = QtGui.QFrame(self.center)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)
        self.global_progress_label = QtGui.QLabel(self.center)
        self.global_progress_label.setObjectName("global_progress_label")
        self.gridLayout_2.addWidget(self.global_progress_label, 2, 0, 1, 1)
        self.current_process = QtGui.QWidget(self.center)
        self.current_process.setObjectName("current_process")
        self.gridLayout_6 = QtGui.QGridLayout(self.current_process)
        self.gridLayout_6.setContentsMargins(50, 50, 50, 20)
        self.gridLayout_6.setVerticalSpacing(20)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.local_progress_bar = QtGui.QProgressBar(self.current_process)
        self.local_progress_bar.setProperty("value", 0)
        self.local_progress_bar.setObjectName("local_progress_bar")
        self.gridLayout_6.addWidget(self.local_progress_bar, 1, 1, 1, 1)
        self.object_central = QtGui.QGridLayout()
        self.object_central.setObjectName("object_central")
        self.textEdit = QtGui.QTextEdit(self.current_process)
        self.textEdit.setObjectName("textEdit")
        self.object_central.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.object_central, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.current_process, 0, 0, 1, 1)
        self.buttom = QtGui.QWidget(self.background)
        self.buttom.setGeometry(QtCore.QRect(200, 550, 600, 50))
        self.buttom.setObjectName("buttom")
        self.gridLayout_7 = QtGui.QGridLayout(self.buttom)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.button_box = QtGui.QDialogButtonBox(self.buttom)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.gridLayout_7.addWidget(self.button_box, 0, 0, 1, 1)

        self.retranslateUi(ScreenShow)
        QtCore.QMetaObject.connectSlotsByName(ScreenShow)

    def retranslateUi(self, ScreenShow):
        ScreenShow.setWindowTitle(QtGui.QApplication.translate("ScreenShow", "WizardPage", None, QtGui.QApplication.UnicodeUTF8))
        self.global_progress_label.setText(QtGui.QApplication.translate("ScreenShow", "Progresso total:", None, QtGui.QApplication.UnicodeUTF8))

import resources.wizard_rc
