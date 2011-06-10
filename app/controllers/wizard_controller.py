import os
import sys

class WizardController(object):
    
    def __init__(self):
        self.install = None

    def reboot(self):
        self.install.reboot()
    
    def start(self, mode, parent):
        if mode == "positivo_installer":
            from app.controllers.positivo import PositivoInstaller
            self.install = PositivoInstaller(parent)
        elif mode == "positivo_master":
            from app.controllers.positivo import PositivoMaster
            self.install = PositivoMaster(parent)
        self.install.start()
        
#    def positivo_master(self):
#        from app.controllers.positivo import PositivoMaster
#        # main (void) :P
#        ask_version || error_msg
#        #ask_3g || error_msg
#        ask_cam || error_msg
#        create_part || error_msg
#        format_swap sda1 || error_msg
#        restore_parts
#        killall zenity # oem ...
#        install_master_files
#        create_hd_restore
#        write_log
#        restore_bootloader || error_msg
#        finish
