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
        
