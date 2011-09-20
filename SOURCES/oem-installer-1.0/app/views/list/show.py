# Copyright (C) 2011 - Jonatas Teixeira <jonatast@mandriva.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

from app.views.list.show_ui import Ui_ListShow

from PyQt4 import QtCore, QtGui

class ListShow(QtGui.QDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.list_show = Ui_ListShow()
        self.list_show.setupUi(self)

        self.button_box = self.list_show.button_box
        self.table_widget = self.list_show.table_widget
        
        self.connect_signals()
    
    def connect_signals(self):
        self.connect(self.button_box, QtCore.SIGNAL("accepted()"), self.button_box_accepted)
        self.connect(self.button_box, QtCore.SIGNAL("rejected()"), self.button_box_rejected)
    
    
    def add_row(self, version, description):
        position = self.table_widget.rowCount()
        self.table_widget.setRowCount(position + 1)

        self.table_widget.setHorizontalHeaderItem(position, QtGui.QTableWidgetItem(version))
        self.table_widget.setItem(position, 0, QtGui.QTableWidgetItem(version))
        self.table_widget.setItem(position, 1, QtGui.QTableWidgetItem(description))

    def button_box_accepted(self):
        self.done(self.table_widget.currentRow())
        
    def button_box_rejected(self):
        self.done(-1)
        
