# -*- coding: utf-8 -*-

from app.views.screen.show_ui import Ui_ScreenShow

from app.views.password.show import PasswordShow
from app.views.message.show import MessageShow
from app.views.list.show import ListShow

from PyQt4 import QtCore, QtGui
import time
import sys
import subprocess

class ScreenShow(QtGui.QMainWindow):
    def __init__(self, Controller):
        QtGui.QMainWindow.__init__(self)
        
        self.screen_show = Ui_ScreenShow()
        self.screen_show.setupUi(self)
        
        # Global and Local steps are used to controll progress bar
        self.global_step = 0
        self.local_step = 0

        self.controller = Controller(self)

        #Some types of dialogs that could be used during the instalation
        self.message_box = MessageShow()
        self.list_show = ListShow()
        self.password = PasswordShow()

        self.connect_signals()
        
    def connect_signals(self):
        self.connect(self.screen_show.button_box, QtCore.SIGNAL("accepted()"), self.button_box_accepted)
        self.connect(self.screen_show.button_box, QtCore.SIGNAL("rejected()"), self.button_box_rejected)
        
        # This signal is very important to controll the message flow beetween viewer and controller
        self.connect(self.controller, QtCore.SIGNAL("interface_action(QString, QString)"), self.interface_action)
    
    # This method set the return of some interface actions
    def interface_return(self, value):
        self.emit(QtCore.SIGNAL("interface_return(QString)"), str(value))
    
    def button_box_accepted(self):
        self.start()

    def button_box_rejected(self):
        self.message_box.set_fields("question", "Cancelar", "Voce realmente deseja interromper a instalacao?\nPode haver inconsistencias em seu sistema!")
        ret = self.message_box.show()

        if ret == QtGui.QMessageBox.Yes:
            self.finish()

    def start(self):
        self.screen_show.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.controller.start()
        
    def finish(self):
        self.close()
#        subprocess.call('reboot', shell=True)
  

    # Here is received action from controller, and these parameters need to be parsing
    def interface_action(self, action, param=''):
        action = str(action.toAscii())
        param = str(param.toAscii())
        
        if action == "local_progress_bar":
            self.interface_return(self.process_progress("local", param))
        elif action == "global_progress_bar":
            self.interface_return(self.process_progress("global", param))
        elif action == "popup":
            self.interface_return(self.process_popup(param))
        elif action == "list":
            self.interface_return(self.process_list(param))
        elif action == "close":
            self.finish()
        elif action == "debug":
            self.interface_return(self.debug(param))
        else:
            print "interface action cant parse your params"
            print action, param
            self.interface_return(None)

    # Parsing action from list
    def process_list(self, param):
        for par in param.split(";"):
            version, description = par.split(',')
            self.list_show.add_row(version, description)

        return self.list_show.exec_()

    # Parsing all types of dialog that could be showed
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
                    
            title = u"%s" % title.decode('utf-8')
            text = u"%s" % text.decode('utf-8')
            
            if type == "password":
                self.password.set_fields(title, text)
                if self.password.exec_():
                    return self.password.get_password()
                else:
                    return ""
            else:
                self.message_box.set_fields(type, title, text)
                return self.message_box.show()
  
    # Parsin progress bar, to set the limit and wich bar will be updated
    def process_progress(self, which, param):
        max_step = message = None
        if param:
            for p in param.split(','):
                if p.startswith(' '):
                    p = p[1:]
                if p.startswith("max_step="):
                    max_step = p.split('=')[1]
                elif p.startswith("message="):
                    message = p.split('=')[1]
                elif p.startswith("max_step = "):
                    max_step = p.split(' = ')[1]
                elif p.startswith("message = "):
                    max_step = p.split(' = ')[1]
        
        if which == "local":
            self.refresh_local_progress(max_step)
        elif which == "global":
            self.refresh_global_progress(max_step)

        if message:
            self.refresh_message(message)

    # Parsing the text area and update de messages
    def refresh_message(self, message):
        import time
        text = self.screen_show.text
        
        for msg in message.split("\n"):
            if msg != "":
                text_message = time.strftime("[%H:%M:%S] ", time.localtime())
                text_message += msg + "\n"
                text.insertPlainText(u"%s" % text_message.decode('utf-8'))

    # Refreshing local progress bar according the max limit
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

    # Refreshing global progress bar according the max limit
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
    
    def debug(self, message):
        self.refresh_message(message)
