from app.views.screen.show_ui import Ui_ScreenShow
from app.views.wait.show import WaitShow
from app.views.message.show import MessageShow

from app.controllers.wizard_controller import WizardController

from PyQt4 import QtCore, QtGui
import time

class ScreenShow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.screen_show = Ui_ScreenShow()
        self.screen_show.setupUi(self)
        
        self.global_step = 0
        self.local_step = 0
        
        self.controller = WizardController()
        self.message_box = MessageShow()
        
        self.button_box = self.screen_show.button_box

        self.connect_signals()
        
    def connect_signals(self):
        self.connect(self.button_box, QtCore.SIGNAL("accepted()"), self.button_box_accepted)
        self.connect(self.button_box, QtCore.SIGNAL("rejected()"), self.button_box_rejected)
    
    def interface_return(self, value):
        self.emit(QtCore.SIGNAL("interface_return(QString)"), str(value))
        
    def button_box_accepted(self):
        print 1
        self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.controller.start("positivo_installer", self)
        self.connect(self.controller.install, QtCore.SIGNAL("interface_action(QString, QString)"), self.interface_action)

    def button_box_rejected(self):
        self.message_box.set_fields("question", "Cancelar", "Voce realmente deseja interromper a instalacao?\nPode haver inconsistencia em seu sistema!")
        ret = self.message_box.show()

        if ret == QtGui.QMessageBox.Yes:
           self.close()
#           self.reboot()
  
    def interface_action(self, action, param=None):
        action = str(action)
        param = str(param)

        if action == "local_progress_bar":
            self.interface_return(self.process_progress("local", param))
        elif action == "global_progress_bar":
            self.interface_return(self.process_progress("global", param))
        elif action == "popup":
            self.interface_return(self.process_popup(param))
        elif action == "close":
            self.close()
      
    def process_popup(self, param):
        type = title = text = None
        if param:
            params = param.split(',')
            for p in params:
                if p.startswith("type=") or p.startswith(" type="):
                    type = p.split('=')[1]
                elif p.startswith("title=") or p.startswith(" title="):
                    title = p.split('=')[1]
                elif p.startswith("text=") or p.startswith(" text="):
                    text = p.split('=')[1]
    
        self.message_box.set_fields(type, title, text)
        return self.message_box.show()
  
    def process_progress(self, which, param):
        max_step = message = None
        if param:
            params = param.split(',')
            for p in params:
                if p.startswith("max_step="):
                    max_step = p.split('=')[1]               
                elif p.startswith("message="):
                    message = p.split('=')[1]
        
        if which == "local":
            self.refresh_local_progress(max_step)
        elif which == "global":
            self.refresh_global_progress(max_step)

        if message:
            self.refresh_message(message)

    def refresh_message(self, message):
        text = self.screen_show.text
        text.insertPlainText(message)

    def refresh_local_progress(self, max_step):
        bar = self.screen_show.local_progress_bar

        if max_step:
            self.local_step = 0
            self.max_local_step = int(max_step)
            bar.setValue(0)
        else:
            self.local_step += 1
            piece = (100 / self.max_local_step)
            if self.local_step == self.max_local_step:
                piece = 100 - piece * (self.max_local_step - 1)
            bar.setValue(bar.value() + piece)

    def refresh_global_progress(self, max_step):
        bar = self.screen_show.global_progress_bar

        if max_step:
            self.global_step = 0
            self.max_global_step = int(max_step)
            bar.setValue(0)
        else:
            self.global_step += 1
            piece = (100 / self.max_global_step)
            if self.global_step == self.max_global_step:
                piece = 100 - piece * (self.max_global_step - 1)
            bar.setValue(bar.value() + piece)
    

