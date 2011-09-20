# -*- coding: utf-8 -*-

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


import os
import sys
import time

from lib.oem_lib import OemLib
from PyQt4 import QtGui
from PyQt4 import QtCore


# More datails about interface actions:
# Call interface_action(string, string)
# Where the first string is a type of action that you want, for example:
#   local_progress_bar      : to refresh the progress bar local
#   global_progress_bar     : to refresh the progress bar global
#   global_progress_bar     : to refresh the progress bar global
#   popup                   : to show a popup according to params
#   list                    : to show a list accordin to params

class WizardController(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
        self.oem_lib = OemLib(self.interface_action)

        # This semaphore is used to wait some interface answer before continuing
        # to execute the next instruction
        self.semaphore = QtCore.QSemaphore(1)
        
        self.connect_signals(self.parent)
    
    def connect_signals(self, parent):
        # Signal that interface use to set the return of answers
        self.connect(parent, QtCore.SIGNAL("interface_return(QString)"), self.interface_return)

    # How it works?
    # When the controller ask for some interface action, usually the controller
    # will need to know the interface answer, for example: when the controller
    # ask if user wanna keep your home partition, so is necessary to know if
    # the answer is YES ou NO.
    # This controller is a thread, to allow a assync work, but for all the
    # interactions to viewer is needen to wait. Because that, we use a semaphore
    # and when interface is called the semaphore is acquire, and the interface
    # return your answer the semaphore is released.
        
    def interface_return(self, value):
        # The semaphore only will be unblocked when the interface return signal is called 
        self.return_value = value
        self.semaphore.release()

    def interface_action(self, action, param=""):
        # Whenever some interface action is called the semaphore need to be blocked
        self.semaphore.acquire()
        self.emit(QtCore.SIGNAL("interface_action(QString, QString)"), action, param)
        
        while self.semaphore.available() != 1:
            time.sleep(0.01)
        
        return self.return_value

    def start_instalation(self, version):
        self.oem_lib.start_instalation(version)

    def confirm_install(self):
        ret = self.interface_action(
            "popup",
            "type=question, title=Confirmação, text=Confirma a reinstalação do sistema?\nEste procedimento apagará todos os seus dados!"
        )

        if int(ret) == int(QtGui.QMessageBox.No):
            self.interface_action("close")

    def keep_home(self, where):
        keep_home = False
        if self.oem_lib.ask_home(where):
            ret = self.interface_action(
                "popup",
                "type=question, title=Manter home, text=Deseja salvar os dados do usuário (partição home)?"
            )
            
            if int(ret) == int(QtGui.QMessageBox.Yes):
                keep_home = True
        self.oem_lib.answer_home(keep_home)

    def finish(self):
        ret = self.interface_action(
            "popup",
            "type=information, title=Conclusão, text=Instalação executada com sucesso!\nO sistema será reiniciado."
        )
        self.interface_action("close")
        
    def create_part(self, which=''):
        if not self.oem_lib.create_part(str(which)):
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha ao criar partiçõess."
            )
            self.interface_action("close")
    
    def format_swap(self):
        if not self.oem_lib.format_swap("sda1"):
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha ao formatar."
            )
            self.interface_action("close")

    def restore_parts(self):
        self.oem_lib.restore_parts()
    
    def restore_parts_philco(self):
        self.oem_lib.restore_parts_philco()
    
    def install_custom_packages(self):
        self.oem_lib.install_custom_packages()
    
    def install_extras(self, path):
        if not self.oem_lib.install_extras(path):
            ret = self.interface_action(
                "popup",
                "type=information, title=Customização, text=Alguns pacotes não puderam ser instalados."
            )

    def install_master_dump(self):
        self.oem_lib.install_master_dump()
        
    def install_custom_from_device(self):
        ret = self.interface_action(
            "popup",
            "type=information, title=Customização, text=Insira o pendrive de customização e pressione ENTER para continuar"
        )

        import time
        time.sleep(7)

        if not self.oem_lib.install_custom_from_device():
           self.interface_action(
                "popup",
                "type=information, title=Erro, text=Alguns pacotes não puderam ser instalados ou nenhum dispositivo foi encontrado."
            )

    def copy_install_files(self):
        self.oem_lib.copy_install_files()

    def generate_iso_master(self):
        if not self.oem_lib.generate_iso_master():
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha na geração de imagens."
            )
            self.interface_action("close")

    def disable_resize(self):
        self.oem_lib.disable_resize()

    def generate_iso_install(self):
        if not self.oem_lib.generate_iso_install():
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha na geração de imagens."
            )
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
            self.interface_action("close")

    def restore_bootloader_meego(self):
        if not self.oem_lib.restore_bootloader_meego():
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha ao restaurar bootloader."
            )
            self.interface_action("close")

    def restore_bootloader_philco(self):
        if not self.oem_lib.restore_bootloader_philco():
            ret = self.interface_action(
                "popup",
                "type=critical, title=Erro, text=Falha ao restaurar bootloader."
            )
            self.interface_action("close")

    def check_password(self):
        check = False
        
        while not check:
            password = self.interface_action(
                "popup",
                "type=password, title=Password..., text=Informe a senha de restauração do sistema:"
            )
            if password:
                if self.oem_lib.check_password(password):
                    check = True
                else:
                    ret = self.interface_action(
                        "popup",
                        "type=question, title=Erro, text=A senha não confere. Tentar novamente?"
                    )
                    if int(ret) == int(QtGui.QMessageBox.Yes):
                        continue
                    else:
                        self.interface_action("close")
            else:
                self.interface_action("close")
          


#        while not password:
#            plain_pwd=$($DIALOG --entry --text="Informe a senha para restaurar o Sistema Operacional: " --hide-text)
#            if [ $? != 0 ]; then
#                $DIALOG --info --text="Instalacao abortada!"
#                reboot
#            fi
#            password_1=$(echo $plain_pwd | sha1sum | cut -d " " -f 1)
#            password_2=$(cat /tmp/media/secret)
#            if [ "$password_1" == "$password_2" ]; then
#                password="OK"
#            else
#                $DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Senha nao confere, tentar novamente?"
#                if [ "$?" != "0" ]; then
#                    reboot
#                fi
#            fi

    def ask_version(self):
        ret = self.interface_action(
            "list",
            'positivo,imagem positivo;\
            nobrand,imagem nobrand;\
            unionpc,imagem unionpc;\
            corporativo,imagem corporativo;\
            masterbrand,imagem masterbrand;\
            unique,imagem positivo unique;\
            moboblack,imagem moboblack'
        )

        if str(ret) == '0':
            print "positivo"
            self.oem_lib.set_version("positivo")
        elif str(ret) == '1':
            print "nobrand"
            self.oem_lib.set_version("nobrand")
        elif str(ret) == '2':
            print "unionpc"
            self.oem_lib.set_version("unionpc")
        elif str(ret) == '3':
            print "corporativo"
            self.oem_lib.set_version("corporativo")
        elif str(ret) == '4':
            print "unique"
            self.oem_lib.set_version("unique")
        else:
            self.interface_action("close")

    def ask_webcam(self):
        ret = self.interface_action(
            "popup",
            "type=question, title=Informação de hardware, text=Instalar o suporte a Webcam?"
        )
        if int(ret) == int(QtGui.QMessageBox.Yes):
            self.oem_lib.set_webcam(True)
        elif int(ret) == int(QtGui.QMessageBox.No):
            self.oem_lib.set_webcam(False)

    def ask_3g(self):
        ret = self.interface_action(
            "popup",
            "type=question, title=Informação de hardware, text=Instalar o suporte 3G?"
        )
        if int(ret) == int(QtGui.QMessageBox.Yes):
            self.oem_lib.set_3g(True)
        elif int(ret) == int(QtGui.QMessageBox.No):
            self.oem_lib.set_3g(False)



