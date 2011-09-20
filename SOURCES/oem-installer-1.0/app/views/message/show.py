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
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

# This class just show a dialog according the own type
class MessageShow(QtGui.QMessageBox):

    def __init__(self):
        QtGui.QMessageBox.__init__(self)

    def set_fields(self, type, title, message):
        self.setWindowTitle(title)
        self.setText(message)
        self.set_type(type)

    # For eache type, is showed a proper dialog
    def set_type(self, text):
        if text == "information":
            self.setIcon(self.Information)
            self.setStandardButtons(self.Ok)
        elif text == "critical":
            self.setIcon(self.Critical)
            self.setStandardButtons(self.Close)
        elif text == "question":
            self.setIcon(self.Question)
            self.setStandardButtons(self.No | self.Yes)
        elif text == "warning":
            self.setIcon(self.Warning)
            self.setStandardButtons(self.Ok)
    
#        text = text

    def show(self):
        return self.exec_()
        
