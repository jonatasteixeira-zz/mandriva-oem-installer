# -*- coding: utf-8 -*-

from app.controllers.wizard_controller import WizardController

class MeegoDisk(WizardController):
    def __init__(self, parent):
        WizardController.__init__(self, parent)
        
    def run(self):
        self.interface_action("global_progress_bar", "max_step=6, message=Iniciando instalação\n")
        self.start_instalation("meego")
        self.check_password()
        self.confirm_install()
        self.keep_home('/etc/meego-release')
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

class MeegoInstaller(WizardController):
    def __init__(self, parent):
        WizardController.__init__(self, parent)

    def run(self):
        self.interface_action("global_progress_bar", "max_step=11, message=Iniciando instalação\n")
        self.start_instalation("meego")
        self.confirm_install()
        self.keep_home('/etc/meego-release')
        self.interface_action("global_progress_bar", "message=Instalação iniciada!\nCriando partições\n")
        self.create_part(2)
        self.interface_action("global_progress_bar", "message=Partições criadas com sucesso!\nFormatando partição swap\n")
        self.format_swap()
        self.interface_action("global_progress_bar", "message=Partição formatada com sucesso!\nRestaurando partições\n")
        self.restore_parts()
        self.interface_action("global_progress_bar", "message=Partições restauradas!\nInstalando pacotes padroes\n")
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
        self.restore_bootloader_meego()
        self.interface_action("global_progress_bar", "message=Bootloader restaurado\nFinalizando instalação\n")
        self.finish()
        
class MeegoMaster(WizardController):
    def __init__(self, parent):
        WizardController.__init__(self, parent)

    def run(self):
        self.interface_action("global_progress_bar", "max_step=9, message=Iniciando instalação\n")
        self.start_instalation("meego")
        self.confirm_install()
        self.interface_action("global_progress_bar", "message=Instalação iniciada!\nRestaurando partições\n")
        self.restore_parts_philco()
        self.interface_action("global_progress_bar", "message=Partições restauradas!\nInstalando pacotes padroes\n")
        self.install_master_dump()
        self.interface_action("global_progress_bar", "message=Pacotes padroes instalados!\nInstalando pacotes a partir de uma media removível\n")
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
        self.restore_bootloader_philco()
        self.interface_action("global_progress_bar", "message=Bootloader restaurado\nFinalizando instalação\n")
        self.finish()

