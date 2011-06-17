# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jonatas/wizard/script/../app/views/list/show.ui'
#
# Created: Fri Jun 17 12:51:00 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ListShow(object):
    def setupUi(self, ListShow):
        ListShow.setObjectName("ListShow")
        ListShow.setWindowModality(QtCore.Qt.WindowModal)
        ListShow.resize(350, 200)
        self.gridLayout = QtGui.QGridLayout(ListShow)
        self.gridLayout.setMargin(3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.vertical_layout = QtGui.QVBoxLayout()
        self.vertical_layout.setSpacing(3)
        self.vertical_layout.setObjectName("vertical_layout")
        self.label = QtGui.QLabel(ListShow)
        self.label.setObjectName("label")
        self.vertical_layout.addWidget(self.label)
        self.line = QtGui.QFrame(ListShow)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vertical_layout.addWidget(self.line)
        self.table_widget = QtGui.QTableWidget(ListShow)
        self.table_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_widget.setAlternatingRowColors(False)
        self.table_widget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_widget.setShowGrid(True)
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, item)
        self.table_widget.horizontalHeader().setVisible(True)
        self.table_widget.horizontalHeader().setDefaultSectionSize(167)
        self.table_widget.horizontalHeader().setHighlightSections(True)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.verticalHeader().setDefaultSectionSize(30)
        self.vertical_layout.addWidget(self.table_widget)
        self.button_box = QtGui.QDialogButtonBox(ListShow)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.vertical_layout.addWidget(self.button_box)
        self.gridLayout.addLayout(self.vertical_layout, 0, 0, 1, 1)

        self.retranslateUi(ListShow)
        QtCore.QMetaObject.connectSlotsByName(ListShow)

    def retranslateUi(self, ListShow):
        ListShow.setWindowTitle(QtGui.QApplication.translate("ListShow", "Imagens", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ListShow", "Escolha a imagem:", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("ListShow", "Versão", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("ListShow", "Descrição", None, QtGui.QApplication.UnicodeUTF8))

