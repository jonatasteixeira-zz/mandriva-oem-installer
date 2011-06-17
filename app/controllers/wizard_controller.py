import os
import sys
import time

from lib.oem_lib import OemLib
from PyQt4 import QtGui
from PyQt4 import QtCore


class WizardController(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
        self.oem_lib = OemLib(self.interface_action)
        self.semaphore = QtCore.QSemaphore(1)
        
        self.connect_signals(self.parent)
        
    def connect_signals(self, parent):
        self.connect(parent, QtCore.SIGNAL("interface_return(QString)"), self.interface_return)
        
    def interface_return(self, value):
        self.return_value = value
        self.semaphore.release()

    def interface_action(self, action, param=""):
        self.semaphore.acquire()
        
        self.emit(QtCore.SIGNAL("interface_action(QString, QString)"), action, param)
        
        while self.semaphore.available() != 1:
            time.sleep(0.01)
        
        return self.return_value

    def reboot(self):
        self.oem_lib.reboot()

    def start_instalation(self):
        self.oem_lib.start_instalation()

    def confirm_install(self):
        ret = self.interface_action(
            "popup",
            "type=question, title=Confirmacao, text=Confirma a reinstalacao do sistema?\n Este procedimento apagara todos os seus dados!"
        )

        if str(ret) == str(QtGui.QMessageBox.No):
#            self.oem_lib.reboot()
            self.interface_action("close")

    def keep_home(self):
        keep_home = False
        if self.oem_lib.ask_home():
            ret = self.interface_action(
                "popup",
                "type=question, title=Manter home, text=Deseja salvar os dados do usuario (particao home)?"
            )
            
            if str(ret) == str(QtGui.QMessageBox.Yes):
                keep_home = True
        self.oem_lib.answer_home(keep_home)

    def finish(self):
        ret = self.interface_action(
            "popup",
            "type=information, title=Conclusao, text=Instalacao executada com sucesso!\nO sistema sera reiniciado."
        )

#        self.oem_lib.reboot()
        self.interface_action("close")
        
    def create_part(self):
        if not self.oem_lib.create_part():
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha ao criar particoes."
            )
#            self.oem_lib.reboot()
            self.interface_action("close")
    
    def format_swap(self):
        if not self.oem_lib.format_swap("sda1"):
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha ao formatar."
            )
#            self.oem_lib.reboot()
            self.interface_action("close")

    def restore_parts(self):
        self.oem_lib.restore_parts()
    
    def install_custom_packages(self):
        self.oem_lib.install_custom_packages()
    
    def install_extras(self):
        self.oem_lib.install_extras("/tmp/media/i586/custom/extras")

    def install_master_files(self):
        self.oem_lib.install_master_files()

    def disable_resize(self):
        self.oem_lib.disable_resize()

    def generate_iso_install(self):
        if not self.oem_lib.gen_iso_install():
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha na geracao de imagens."
            )
#            self.oem_lib.reboot()
            self.interface_action("close")

    def create_hd_restore(self):
        self.oem_lib.create_hd_restore()

    def write_log(self):
        self.oem_lib.write_log()

    def restore_bootloader(self):
        if not self.oem_lib.restore_bootloader():
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha ao restaurar bootloader."
            )
#            self.oem_lib.reboot()
            self.interface_action("close")

    def ask_version(self):
        ret = self.interface_action(
            "list",
            'positivo,imagem positivo;nobrand,imagem nobrand;unionpc,imagem unionpc;corporativo,imagem corporativo;unique,imagem positivo unique'
        )

        if str(ret) == '0':
            self.oem_lib.set_version("positivo")
        elif str(ret) == '1':
            self.oem_lib.set_version("nobrand")
        elif str(ret) == '2':
            self.oem_lib.set_version("unionpc")
        elif str(ret) == '3':
            self.oem_lib.set_version("corporativo")
        elif str(ret) == '4':
            self.oem_lib.set_version("unique")
        else:
#            self.oem_lib.reboot()
            self.interface_action("close")

    def ask_webcam(self):
        ret = self.interface_action(
            "popup",
            "type=question, title=Informacao de hardware, text=Instalar o suporte a Webcam?"
        )
        if str(ret) == "true":
            self.oem_lib.set_webcam(True)
        elif str(ret) == "false":
            self.oem_lib.set_webcam(False)

    def ask_3g(self):
        ret = self.interface_action(
            "popup",
            "type=question, title=Informacao de hardware, text=Instalar o suporte 3G?"
        )
        if str(ret) == "true":
            self.oem_lib.set_3g(True)
        elif str(ret) == "false":
            self.oem_lib.set_3g(False)

class PositivoInstaller(WizardController):
    def __init__(self, parent):
        WizardController.__init__(self, parent)
                
    def run(self):
        self.interface_action("global_progress_bar", "max_step=10, message=Iniciando instalacao\n")
        self.start_instalation()
        self.confirm_install()
        self.keep_home()
        self.interface_action("global_progress_bar", "message=Instalacao iniciada!\nCriando particoes\n")
        self.create_part()
        self.interface_action("global_progress_bar", "message=Particoes criadas com sucesso!\nFormatando particao swap\n")
        self.format_swap()
        self.interface_action("global_progress_bar", "message=Particao formatada com sucesso!\nRestaurando particoes\n")
        self.restore_parts()
        self.interface_action("global_progress_bar", "message=Particoes restauradas!\nInstalando pacotes padroes\n")
        self.install_custom_packages()
        self.interface_action("global_progress_bar", "message=Pacotes instalados com sucesso!\nInstalando pacotes extras\n")
        self.install_extras()
        self.interface_action("global_progress_bar", "message=Pacotes extras instalados com sucesso!\nDisabilitando redimensionamento\n")
        self.disable_resize()
        self.interface_action("global_progress_bar", "message=Redimensionamento desativado!\nGerando imagem de instalacao\n")
        self.generate_iso_install()
        self.interface_action("global_progress_bar", "message=Imagem de instalacao gerada com sucesso!\nCriando restauracao de disco\n")
        self.create_hd_restore()
        self.interface_action("global_progress_bar", "message=Disco de restauracao criado!\nCriando log\n")
        self.write_log()
        self.interface_action("global_progress_bar", "message=Log criado!\nRestaurando bootloader\n")
        self.restore_bootloader()
        self.interface_action("global_progress_bar", "message=Bootloader restaurado\nFinalizando instalacao\n")
        self.finish()


class PositivoMaster(WizardController):
    def __init__(self, parent):
        WizardController.__init__(self, parent)

    def run(self):
        # main (void) :P
        self.ask_version()
        self.ask_webcam()
#        self.ask_3g()
        
        self.create_part()
        self.format_swap()
        self.restore_parts()

        self.install_master_files()

        self.create_hd_restore()
        self.write_log()
        self.restore_bootloader()
        self.finish()
        




