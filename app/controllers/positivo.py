from lib.oem_lib import OemLib
from threading import Thread
from PyQt4 import QtGui
from PyQt4 import QtCore
import subprocess

from app.views.message.show import MessageShow

class PositivoInstaller(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        
        self.oem_lib = OemLib(self.interface_action)
        self.connect_signals(parent)
        self.semaphore = QtCore.QSemaphore(1)
        print 2

    
    def connect_signals(self, parent):
        self.connect(parent, QtCore.SIGNAL("interface_return(QString)"), self.interface_return)
        
    def interface_return(self, value):
        self.return_value = value
        self.semaphore.release()
        
    def interface_action(self, action, param=None):
        import time

        self.semaphore.acquire()
        
        if not param:
            param = ""
        self.emit(QtCore.SIGNAL("interface_action(QString, QString)"), action, param)
        
        while self.semaphore.available() != 1:
            time.sleep(0.01)
        
        return self.return_value

    def start_instalation(self):
        self.oem_lib.init_positivo_installer()
        self.oem_lib.start_instalation()

    def confirm_install(self):
        ret = self.interface_action(
            "popup",
            "type=question, title=Confirmacao, text=Confirma a reinstalacao do sistema?\n Este procedimento apagara todos os seus dados!"
        )

        if ret == QtGui.QMessageBox.No:
#            self.oem_lib.reboot()
            self.interface_action("close")

    def keep_home(self):
        keep_home = False
        if self.oem_lib.ask_home():
            ret = self.interface_action(
                "popup",
                "type=question, title=Manter home, text=Deseja salvar os dados do usuario (particao home)?"
            )
            
            if ret == QtGui.QMessageBox.Yes:
                keep_home = True
        self.oem_lib.answer_home(keep_home)

    def finish(self):
        ret = self.interface_action(
            "popup",
            "type=information, title=Conclusao, text=Instalacao executada com sucesso!\nO sistema sera reiniciado."
        )

#        self.oem_lib.reboot()
        self.interface_action("close")
        
    def reboot(self):
        self.oem_lib.reboot()
    
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

    def run(self):
        print 3
        self.interface_action("global_progress_bar", "max_step=11")
        print 4
        self.interface_action("global_progress_bar", "message=Iniciando instalacao\n")        
        print 5
        self.start_instalation()
        print 6
        self.confirm_install()
        print 7
        self.keep_home()
        print 8
        self.interface_action("global_progress_bar", "message=Instalacao iniciada!\nCriando particoes\n")
        print 9
        self.create_part()
        print 10
        self.interface_action("global_progress_bar", "message=Particoes criadas com sucesso!\nFormatando particao swap\n")
        print 11
        self.format_swap()
        print 12
        self.interface_action("global_progress_bar", "message=Particao formatada com sucesso!\nRestaurando particoes\n")
        print 13
        self.restore_parts()
        print 14
        self.interface_action("global_progress_bar", "message=Particoes restauradas!\nInstalando pacotes padroes\n")

        self.install_custom_packages()
        self.interface_action("global_progress_bar", "message=Pacotes instalados com sucesso!\nInstalando pacotes extras\n")
        
        self.install_extras()
        self.interface_action("global_progress_bar", "message=Pacotes extras instalados com sucesso!\nDisabilitando redimensionamento\n")
        
        self.disable_resize()
        self.interface_action("global_progress_bar", "message=Redimensionamento disativado!\nGerando imagem de instalacao\n")
        
        self.generate_iso_install()
        self.interface_action("global_progress_bar", "message=Imagem de instalacao gerada com sucesso!\nCriando restauracao de disco\n")

        self.create_hd_restore()
        self.interface_action("global_progress_bar", "message=Disco de restauracao criado!\nCriando log\n")

        self.write_log()
        self.interface_action("global_progress_bar", "message=Log criado!\nRestaurando bootloader\n")

        self.restore_bootloader()
        self.interface_action("global_progress_bar", "message=Bootloader restaurado\nFinalizando instalacao\n")

        self.finish()

class PositivoMaster(OemLib):

    def __init__(self):
        OemLib.__init__(self)
        
#        if grep -q gubed /proc/cmdline; then
#	        set -x
#	        exec &> /tmp/debug-install.log
#        fi

#        source /usr/sbin/oem-lib.sh

#        # need some modules first
#        modprobe dm-mod &>/dev/null
#        modprobe ext4 &>/dev/null
#        drvinst &> /dev/null
