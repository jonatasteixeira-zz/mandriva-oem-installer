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

from app.views.password.show_ui import Ui_PasswordShow

from PyQt4 import QtCore, QtGui

# This class just to show a dialog to user set the password
class PasswordShow(QtGui.QDialog):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.password_show = Ui_PasswordShow()
        self.password_show.setupUi(self)

        self.password = self.password_show.password
        self.button_box = self.password_show.button_box

        self.connect_signals()
    
    def connect_signals(self):
        self.connect(self.button_box, QtCore.SIGNAL("accepted()"), self.button_box_accepted)
        self.connect(self.button_box, QtCore.SIGNAL("rejected()"), self.button_box_rejected)
    
    def set_fields(self, title, text):
        self.setWindowTitle(title)
        self.password_show.header.setText(text)
    
    def button_box_accepted(self):
        self.done(1)
        
    def button_box_rejected(self):
        self.done(0)
		
    def get_password(self):
        return self.password.text()

"""
    # Interface Method can't be here
    def wait_for_it(self, message):
    	(while true; do echo ; sleep 1; done) |  $DIALOG --progress --pulsate --text="$1" &
    	killpid=$!

    # Interface Method can't be here
    def error_message(self):
	    $DIALOG --error --text="Ocorreu um erro durante a instalacao, verifique a midia e tente novamente." 
	    reboot
"""
