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

from app.controllers.wizard_controller import WizardController

class PositivoDisk(WizardController):
    def __init__(self, parent):
        WizardController.__init__(self, parent)
        
    def run(self):
        self.interface_action("global_progress_bar", "max_step=6, message=Iniciando instalação\n")
        self.start_instalation("positivo")
        self.check_password()
        self.confirm_install()
        self.keep_home('/etc/oem-release')
        self.interface_action("global_progress_bar", "message=Instalação iniciada!\nFormatando partição swap\n")
        self.format_swap()
        self.interface_action("global_progress_bar", "message=Partição formatada com sucesso!\nRestaurando partições\n")
        self.restore_parts()
        self.interface_action("global_progress_bar", "message=Partições restauradas!\nInstalando pacotes padrões\n")
        self.install_custom_packages()
        self.interface_action("global_progress_bar", "message=Pacotes instalados com sucesso!\nInstalando pacotes extras\n")
        self.install_extras("/tmp/loop/i586/custom/extras")
        self.interface_action("global_progress_bar", "message=Pacotes extras instalados com sucesso!\nDisabilitando redimensionamento\n")
        self.disable_resize()
        self.interface_action("global_progress_bar", "message=Redimensionamento desativado!\nFinalizando instalação\n")
        self.finish()

class PositivoInstaller(WizardController):
    def __init__(self, parent):
        WizardController.__init__(self, parent)

    def run(self):
        self.interface_action("global_progress_bar", "max_step=10, message=Iniciando instalação\n")
        self.start_instalation("positivo")
        self.confirm_install()
        self.keep_home('/etc/oem-release')
        self.interface_action("global_progress_bar", "message=Instalação iniciada!\nCriando partições\n")
        self.create_part()
        self.interface_action("global_progress_bar", "message=Partições criadas com sucesso!\nFormatando partição swap\n")
        self.format_swap()
        self.interface_action("global_progress_bar", "message=Partição formatada com sucesso!\nRestaurando partições\n")
        self.restore_parts()
        self.interface_action("global_progress_bar", "message=Partições restauradas!\nInstalando pacotes padrões\n")
        self.install_custom_packages()
        self.interface_action("global_progress_bar", "message=Pacotes instalados com sucesso!\nInstalando pacotes extras\n")
        self.install_extras("/tmp/media/i586/custom/extras")
        self.interface_action("global_progress_bar", "message=Pacotes extras instalados com sucesso!\nDisabilitando redimensionamento\n")
        self.disable_resize()
        self.interface_action("global_progress_bar", "message=Redimensionamento desativado!\nGerando imagem de instalação\n")
        self.generate_iso_install()
        self.interface_action("global_progress_bar", "message=Imagem de instalação gerada com sucesso!\nCriando restauração de disco\n")
        self.create_hd_restore()
        self.interface_action("global_progress_bar", "message=Disco de restauração criado!\nCriando log\n")
        self.write_log()
        self.interface_action("global_progress_bar", "message=Log criado!\nRestaurando bootloader\n")
        self.restore_bootloader()
        self.interface_action("global_progress_bar", "message=Bootloader restaurado\nFinalizando instalação\n")
        self.finish()

class PositivoMaster(WizardController):
    def __init__(self, parent):
        WizardController.__init__(self, parent)

    def run(self):
        self.interface_action("global_progress_bar", "max_step=11, message=Iniciando instalação\n")
        self.start_instalation("positivo")
        self.ask_version()
        self.ask_webcam()
#        self.ask_3g()
        self.interface_action("global_progress_bar", "message=Instalação iniciada!\nCriando partições\n")
        self.create_part()
        self.interface_action("global_progress_bar", "message=Partições criadas com sucesso!\nFormatando partição swap\n")
        self.format_swap()
        self.interface_action("global_progress_bar", "message=Partição formatada com sucesso!\nRestaurando partições\n")
        self.restore_parts()
        self.interface_action("global_progress_bar", "message=Partições restauradas!\nInstalando pacotes padrões\n")
        self.install_master_dump()
        self.interface_action("global_progress_bar", "message=Pacotes padrões instalados!\nInstalando pacotes apartir de uma media removível\n")
        self.install_custom_from_device()
        self.interface_action("global_progress_bar", "message=Pacotes processados!\nCopiando arquivos de instalação\n")
        self.copy_install_files()
        self.interface_action("global_progress_bar", "message=Arquivos copiados!\nGerando imagem\n")
        self.generate_iso_master()
        self.interface_action("global_progress_bar", "message=Imagem gerada!\nCriando ponto de restauração de disco\n")
        self.create_hd_restore()
        self.interface_action("global_progress_bar", "message=Disco de restauração criado!\nCriando log\n")
        self.write_log()
        self.interface_action("global_progress_bar", "message=Log criado!\nRestaurando bootloader\n")
        self.restore_bootloader()
        self.interface_action("global_progress_bar", "message=Bootloader restaurado\nFinalizando instalação\n")
        self.finish()

