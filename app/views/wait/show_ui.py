# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jonatas/wizard/script/../app/views/wait/show.ui'
#
# Created: Thu Jun  9 14:42:17 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_WaitShow(object):
    def setupUi(self, WaitShow):
        WaitShow.setObjectName("WaitShow")
        WaitShow.resize(400, 100)
        WaitShow.setSizeGripEnabled(True)
        WaitShow.setModal(True)
        self.gridLayout = QtGui.QGridLayout(WaitShow)
        self.gridLayout.setObjectName("gridLayout")
        self.progress_bar = QtGui.QProgressBar(WaitShow)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setProperty("value", 60)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setInvertedAppearance(False)
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout.addWidget(self.progress_bar, 1, 0, 1, 1)
        self.button_box = QtGui.QDialogButtonBox(WaitShow)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 3, 0, 1, 1)

        self.retranslateUi(WaitShow)
        QtCore.QMetaObject.connectSlotsByName(WaitShow)

    def retranslateUi(self, WaitShow):
        WaitShow.setWindowTitle(QtGui.QApplication.translate("WaitShow", "Aguarde...", None, QtGui.QApplication.UnicodeUTF8))
        self.progress_bar.setFormat(QtGui.QApplication.translate("WaitShow", "Aguarde", None, QtGui.QApplication.UnicodeUTF8))

