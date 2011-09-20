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


# This class is just a translate of oem-lib.sh, made by Ednilson Miura
# Some changes were necessary, just to improve the performance and make clean
# and easy to read and understand. Believe me, this code was in the dark side!


# For each action here that possibly need more time, is fair put a interface
# call to user to know what happen.
# To do that you'd the call "interface_action(string, string)"

# Where the first string is a type of action that you want, for example:
#   local_progress_bar      : to refresh the progress bar local
#   global_progress_bar     : to refresh the progress bar global
#   global_progress_bar     : to refresh the progress bar global
#   popup                   : to show a popup according to params
#   list                    : to show a list accordin to params

# Is this file is not a good idea to use all this action.
# To more details, read wizard_controller.py


import os
import subprocess

class OemLib(object):
    def __init__(self, interface_action):
        self.interface_action = interface_action

    def start_instalation(self, version):

        self.interface_action("local_progress_bar", "max_step=5, message=Preparando instalação\n")

        #positivo and meego /*
        self.interface_action("local_progress_bar")
        subprocess.call('modprobe dm-mod', shell=True)

        self.interface_action("local_progress_bar")
        subprocess.call('drvinst', shell=True)
        #positivo and meego */

        self.tmp_mount = "/tmp/vfat"
        self.rootfs_dir = "/mnt/rootfs"
#        self.extra_dir = self.tmp_mount + "/extras"
        self.restore_dir = self.rootfs_dir + "/mnt/restore"

#        self.oem_version = version
        self.set_version(version)

        self.interface_action("local_progress_bar")
        subprocess.call('mkdir ' + self.tmp_mount, shell=True)        
        subprocess.call('mkdir -p ' + self.rootfs_dir, shell=True)
        subprocess.call('mkdir -p ' + self.restore_dir + '/extras', shell=True)

        # should blacklist install media
        self.interface_action("local_progress_bar")
        os.environ['blacklist'] = os.popen('mount | grep "/tmp/media" | cut -d " " -f 1 | sed "s#/dev/##"').read()
        self.install_device = os.popen('cat /proc/mounts | grep "/tmp/media" | cut -d" " -f1').read().rstrip()

        self.interface_action("local_progress_bar")
        if subprocess.call('grep -q from_disk /proc/cmdline', shell=True) == 0:
            os.environ['from_disk'] = "true"

        # Quack!!! Some doubt ask to Santiago, or Miura
        if self.install_device == "/dev/sr0":
            self.install_device = "/dev/scd0"

    # Simple search for all removable devices
    def valid_block_devices(self):
        devs = os.popen('ls /sys/block/ | egrep -i sd.*').read().split()
        loops = str(len(devs) + 1)
        
        self.interface_action("local_progress_bar", "max_step=" + loops + ", message=Obtendo lista de devices.\n")
        
        os.environ['device'] = ""
        for sd in devs:
            self.interface_action("local_progress_bar")
            if subprocess.call('grep -q 1 $i/removable', shell=True) == 0:
                cmd = "echo " + sd + " | cut -d "/" -f 4 | sed s/$blacklist//"
                os.environ['device'] = os.environ['device'] + os.popen('cmd').read()
        self.interface_action("local_progress_bar", "message=Lista obtida.\n")


    # Reads iso using blocksize and blockcounts
    def rawread(self, raw_device, iso_output):

        blocksize = os.popen('isoinfo -d -i ' + raw_device + ' | grep "^Logical block size is:" | cut -d " " -f 5')
        if not blocksize:
            print 'catdevice FATAL ERROR: Blank blocksize'
            return False

        blockcount = os.popen('isoinfo -d -i ' + raw_device + ' | grep "^Volume size is:" | cut -d " " -f 4')
        if not blockcount:
            print 'catdevice FATAL ERROR: Blank blockcount'
            return False

        cmd = "dd if=" + raw_device
        cmd = " of=" + iso_output
        cmd += " bs=" + blocksize
        cmd += " count=" + blockcount
        cmd += " conv=notrunc,noerror"

        subprocess.call(cmd, shell=True)
        return True

    # install custom stuff in master mode (in "extras" dir)
    def install_extras(self, path):
        os.environ['tmp'] = path
        
        steps = 4 + len(os.popen('ls ' + path+ '/*').read().split())
        self.interface_action("local_progress_bar", "max_step=" + str(steps))
        
        self.interface_action("local_progress_bar")
        subprocess.call('mount /dev/sda2 ' + self.rootfs_dir, shell=True)
        subprocess.call('mkdir -p ' + self.restore_dir, shell=True)
        subprocess.call('mount /dev/sda3 ' + self.restore_dir, shell=True)
        subprocess.call('mkdir -p ' + self.restore_dir + '/extras',  shell=True)
        subprocess.call('mount none ' + self.rootfs_dir + '/proc -t proc', shell=True)
        subprocess.call('mount none ' + self.rootfs_dir + '/sys -t sysfs', shell=True)

        self.interface_action("local_progress_bar", "message=Procurando arquivos pacote de otimização:\n")
        
        success = True
        for os.environ['file'] in os.popen('ls ' + path + '/*').read().split():
            os.environ['install'] = os.popen('file $file | cut -d " " -f 2').read()
            subprocess.call('cp -f $file ' + self.restore_dir + '/extras/', shell=True)

            if os.environ['install'] == "gzip":
                self.interface_action("local_progress_bar", "message=\tgzip encontrado!\n\tdescompactando...\n")
                subprocess.call('tar zxf $file -C ' + self.rootfs_dir, shell=True)
            elif os.environ['install'] == "bzip2":
                self.interface_action("local_progress_bar", "message=\ttar encontrado!\n\tdescompactando...\n")
                subprocess.call('tar jxf $file -C ' + self.rootfs_dir, shell=True)
            elif os.environ['install'] == "Zip":
                self.interface_action("local_progress_bar", "message=\tzip encontrado!\n\tdescompactando...\n")
                subprocess.call('unzip -q -o $file -d ' + self.rootfs_dir, shell=True)
            elif os.environ['install'] == "RPM":
                self.interface_action("local_progress_bar", "message=\trpm encontrado!\n\tdescompactando...\n")
                subprocess.call('cp -f $file ' + self.rootfs_dir, shell=True)
                subprocess.call('chroot ' + self.rootfs_dir + ' rpm -U *.[RrPpMm]* --replacepkgs --nodeps', shell=True)
                subprocess.call('rm -f ' + self.rootfs_dir + '/*.[RrPpMm]*', shell=True)
            elif os.environ['install'] == " ":
                subprocess.call('echo vazio', shell=True)
            else:
                self.interface_action("local_progress_bar", "message=\tformato incoerente: " + os.environ['install'] + "!\n")
                success = False

        self.interface_action("local_progress_bar", "message=Otimizacao finalizada!\nFinalizando instalação de pacotes extras.\n")

        subprocess.call('umount ' + self.rootfs_dir + '/proc', shell=True)
        subprocess.call('umount ' + self.rootfs_dir + '/sys', shell=True)
        subprocess.call('umount ' + self.restore_dir, shell=True)
        subprocess.call('umount ' + self.rootfs_dir, shell=True)
        self.interface_action("local_progress_bar")

        return success

    # ask if user wishes to keep its home (last part)
    def ask_home(self, where):
        subprocess.call('mkdir -p ' + self.rootfs_dir, shell=True)
        subprocess.call('mount /dev/sda2 ' + self.rootfs_dir, shell=True)
        
        ret = False
        if os.path.exists(self.rootfs_dir + where):
            ret = True
        
        subprocess.call('umount ' + self.rootfs_dir, shell=True)
        return ret
        
    def answer_home(self, home):
        if home:
            os.environ['keep_home'] = 'true'
            

    def create_part(self, arg):
    
        self.interface_action("local_progress_bar", "max_step=2, message=Verificando home")

        cmd = ''
        
        if 'keep_home' in os.environ and os.environ['keep_home'] == 'true':
            cmd = "cat /tmp/image/data/box/sda.dump" + arg + " | sed -e '/sda4/ s/size=.*,/size= ,/' | sfdisk -f /dev/sda"
        else:
            cmd = "cat /tmp/image/data/box/sda.dump" + arg + " | sfdisk -f /dev/sda"

        subprocess.call(cmd, shell=True)
        self.interface_action("local_progress_bar", "message=Notificando particionamento ao sistema")

        import time
        time.sleep(2)
        status = subprocess.call('sfdisk -R /dev/sda', shell=True)

        return (status == 0)

    # format swap partition
    def format_swap(self, dev):
        ret = subprocess.call('mkswap /dev/' + dev, shell=True)
        return (ret == 0)

    # restore desired partition
    def restore_part(self, arg):
        if 'from_disk' in os.environ and os.environ['from_disk'] == 'true':
            restore_path = '/tmp/loop/i586'
        else:
            restore_path = '/tmp/image'
        os.environ['restore_path'] = restore_path

        cmd = 'fsarchiver -v restfs ' + restore_path + '/data/box/backup.sda' + arg + '.fsa id=0,dest=/dev/sda' + arg + ',mkfs=ext3'

        subprocess.call(cmd, shell=True)

#        self.parse_log()

    # resize desired partition to its maximum size
    def resize_part(self, arg):
        subprocess.call('e2fsck -f -y /dev/sda' + arg, shell=True)
        subprocess.call('resize2fs /dev/sda' + arg, shell=True)

    # loop to restore all partitions
    def restore_parts(self):
        parts = "2"
        if not 'from_disk' in os.environ or os.environ['from_disk'] != 'true':
            parts += " 3"
        if not 'keep_home' in os.environ or os.environ['keep_home'] != 'true':
            parts += " 4"
 
        self.interface_action("local_progress_bar", "max_step=" + str(len(parts.split()) * 2))
        
        for part in parts.split():
            self.restore_part(part)
            self.interface_action("local_progress_bar")
            self.resize_part(part)
            self.interface_action("local_progress_bar")

    # restore in master mode (philco)
    def restore_parts_philco(self):
        parts="2 3"

        import time
        self.interface_action("local_progress_bar", "max_step=7")
        for part in parts.split():
            self.restore_part(part)
            self.interface_action("local_progress_bar")
            self.resize_part(part)
            self.interface_action("local_progress_bar")

        # fscking hack, believe me, dont remove these sleeps
        subprocess.call('sfdisk -R /dev/sda', shell=True)
        self.interface_action("local_progress_bar")
        time.sleep(2)

        subprocess.call('sfdisk -d /dev/sda | sed \'s/Id=93/Id=83/\' | sfdisk -f /dev/sda', shell=True)
        self.interface_action("local_progress_bar")
        time.sleep(2)

        subprocess.call('sfdisk -R /dev/sda', shell=True)
        self.interface_action("local_progress_bar")

    # Installs custom files (duuu)
    def install_custom_packages(self):
    
        self.install_version()
        self.interface_action("local_progress_bar", "max_step=6, message=Checando versão\n")

        if subprocess.call('grep -q master_dump /proc/cmdline', shell=True) != 0:
            self.interface_action("local_progress_bar", "message=Processando pacotes personalizados...\n")
            subprocess.call('mkdir /mnt/proc', shell=True)
            subprocess.call('mkdir /mnt/sys', shell=True)
            subprocess.call('mount /dev/sda2 /mnt', shell=True)
            subprocess.call('mount none /mnt/proc -t proc', shell=True)
            subprocess.call('mount none /mnt/sys -t sysfs', shell=True)
            self.interface_action("local_progress_bar")

            subprocess.call('cp -f /tmp/image/custom/*.rpm /mnt/tmp', shell=True)
            self.interface_action("local_progress_bar")
            
            subprocess.call('chroot /mnt rpm -Uv /tmp/*.rpm --replacepkgs --nodeps', shell=True)
            self.interface_action("local_progress_bar")
            
            subprocess.call('rm -f /mnt/tmp/*.rpm', shell=True)
            self.interface_action("local_progress_bar")

            subprocess.call('umount /mnt/proc', shell=True)
            subprocess.call('umount /mnt/sys', shell=True)
            subprocess.call('umount /mnt', shell=True)
            self.interface_action("local_progress_bar")
        else:
            for _ in range(6):
                self.interface_action("local_progress_bar", "message=Pacotes de personalização não foram instalados")

    def install_master_dump(self):
        if subprocess.call('grep -q master_dump /proc/cmdline', shell=True) != 0:
            self.interface_action("local_progress_bar", "max_step=4, message=Criando estrutura.\n")
            subprocess.call('mkdir /mnt/proc', shell=True)
            subprocess.call('mkdir /mnt/sys', shell=True)
            subprocess.call('mount /dev/sda2 /mnt', shell=True)
            subprocess.call('mount none /mnt/proc -t proc', shell=True)
            subprocess.call('mount none /mnt/sys -t sysfs', shell=True)

            self.interface_action("local_progress_bar", "message=Copiando pacotes.\n")
            subprocess.call('cp -f /tmp/image/custom/*.rpm /mnt/tmp', shell=True)

            self.interface_action("local_progress_bar", "message=Instalando pacotes.\n")
            subprocess.call('chroot /mnt rpm -Uv /tmp/*.rpm --replacepkgs --nodeps', shell=True)
            
            self.interface_action("local_progress_bar", "message=Removendo arquivos temporários.\n")
            
            subprocess.call('rm -f /mnt/tmp/*.rpm', shell=True)

            # For some reason appear a weird device mounted here.. So..

            subprocess.call('sync', shell=True)
            subprocess.call('umount -l /mnt/proc', shell=True)
            subprocess.call('umount -l /mnt/sys', shell=True)
            subprocess.call('umount -l /mnt', shell=True)
            
        else:
            self.interface_action("local_progress_bar", "max_step=1")

        self.interface_action("local_progress_bar", "message=Montando partições de restauração.\n")
        subprocess.call('mount /dev/sda3 ' + self.restore_dir, shell=True)
        subprocess.call('umount -f /tmp/vfat', shell=True)

    def install_custom_from_device(self):
        import time
        self.valid_block_devices()

        ret = False
        
        for dev in os.environ['device'].split():
            cmd = "mount /dev/"
            cmd += os.popen('echo ' + dev + '| tr -d [:space:]').read()
            cmd += "1 "
            cmd += self.tmp_mount
            
            if subprocess.call(cmd, shell=True) == 0:
                ret = self.install_extras("/tmp/vfat/extras")

                break
            else:
                time.sleep(3)
            subprocess.call('umount ' + self.tmp_mount, shell=True)

        return ret

    def copy_install_files(self):
        self.interface_action("local_progress_bar", "max_step=2, message=Montando partições e criando estrutura de diretórios.\n")
        subprocess.call('mount /dev/sda2 ' + self.rootfs_dir, shell=True)
        subprocess.call('mkdir -p ' + self.restore_dir + '/', shell=True)
        subprocess.call('mount /dev/sda3 ' + self.restore_dir, shell=True)
        subprocess.call('mkdir -p ' + self.rootfs_dir + '/tmp/install_media', shell=True)
        subprocess.call('mkdir -p ' + self.rootfs_dir + '/tmp/install_media/i586/custom/extras', shell=True)
        
        self.interface_action("local_progress_bar", "message=Copiando arquivos...\n")
        subprocess.call('cp -fa /tmp/media/* ' + self.rootfs_dir + '/tmp/install_media', shell=True)
        self.interface_action("local_progress_bar")
        subprocess.call('cp -af ' + self.restore_dir + '/extras/* ' + self.rootfs_dir + '/tmp/install_media/i586/custom/extras', shell=True)

        subprocess.call('umount ' + self.restore_dir, shell=True)
        subprocess.call('umount ' + self.rootfs_dir, shell=True)

    def generate_iso_master(self):
        self.interface_action("local_progress_bar", "max_step=5, message=Montando partições raiz.\n")
        subprocess.call('mount /dev/sda2 ' + self.rootfs_dir, shell=True)
        subprocess.call('mount /dev/sda3 ' + self.restore_dir, shell=True)
        
        directory = self.rootfs_dir + '/tmp/install_media/'
        
        subprocess.call('ls', shell=True, cwd=directory)
        
        self.interface_action("local_progress_bar", "message=Removendo arquivos de instalação.\n")
        subprocess.call('rm -rf rr_moved', shell=True, cwd=directory)
        
        self.interface_action("local_progress_bar", "message=Criando imagem...\n")
               
        cmd = 'mkisofs'
        cmd += ' -V ' + self.oem_version
        cmd += ' -o ' + self.restore_dir + '/restore.iso'
        cmd += ' -b i586/isolinux/isolinux.bin -c i586/isolinux/boot.cat'
        cmd += ' -no-emul-boot -boot-load-size 4 -boot-info-table'
        cmd += ' -J -R . 2>&1'

        subprocess.call(cmd, shell=True, cwd=directory)

        directory=None
        extras = ''
        if 'has_3g' in os.environ and os.environ['has_3g'] == 'true':
            extras += '3g'
        if 'has_webcam' in os.environ and os.environ['has_webcam'] == 'true':
            extras += 'cam'

        label = self.oem_version + extras

        self.interface_action("local_progress_bar", "message=Implantando label \"" + label + "\" na imagem.\n")
        if subprocess.call('isolabel -n ' + label + ' ' + self.restore_dir + '/restore.iso', shell=True) != 0:
            return False

        subprocess.call('isohybrid ' + self.restore_dir + '/restore.iso', shell=True)

        self.interface_action("local_progress_bar", "message=Implantando código de integridade na imagem.\n")
        if subprocess.call('implantisomd5 -f ' + self.restore_dir + '/restore.iso', shell=True) != 0:
            return False
        
        self.interface_action("local_progress_bar", "message=Finalizando a criação da imagem.\n")
        subprocess.call('rm -rf  ' + self.rootfs_dir + '/tmp/install_media', shell=True)
        subprocess.call('umount ' + self.restore_dir, shell=True)
        subprocess.call('umount ' + self.rootfs_dir, shell=True)
        subprocess.call('rmdir ' + self.tmp_mount, shell=True)

        return True

    # just generates default install iso (for master, use install extras)
    def generate_iso_install(self):

        self.interface_action("local_progress_bar", "max_step=3, message=Montando partições de restauração.\n")
        subprocess.call('mkdir ' + self.restore_dir, shell=True)
        subprocess.call('mount /dev/sda3 ' + self.restore_dir, shell=True)
        restore_iso = self.restore_dir + '/restore.iso'

        self.interface_action("local_progress_bar", "message=Checando ponto de restauração.\n")

        if self.install_device.startswith('/dev/sd'):
            self.interface_action("local_progress_bar", "message=Salvando imagem de restauração...\n")
            raw_size = os.popen('isosize '+ self.install_device).read()
            blocks = (int(raw_size) / (1048576 * 4)) + 10  # from 'dd' manpage: 1048576 is 1M
            cmd = 'dd if=' + self.install_device + ' of=' + restore_iso + ' bs=4M count=' + str(blocks)
            subprocess.call(cmd, shell=True)
        else:
            self.interface_action("local_progress_bar", "message=Salvando imagem de restauração...")
            if not self.rawread(self.install_device, restore_iso):
                return False
        
        self.interface_action("local_progress_bar", "message=Verificando código de integridade...\n")

        # The return of checkusomd5 is inverse
        if subprocess.call('checkisomd5 ' + restore_iso, shell=True) == 1:
            subprocess.call('umount ' + self.restore_dir, shell=True)
        else:
            return False
        return True

    # parse fsarchiver log (please, improve-me)
    def parse_log(self):
        self.interface_action("local_progress_bar", "max_step=100")
        import time
        time.sleep(5)
        
        fs_pid = os.popen("ps aux | awk '$11 == \"fsarchiver\" { print $2 }'").read()
        
        percent = 0
        while fs_pid != "":
            new_percentage = os.popen('tail -n1 /tmp/fs.log | grep "\-\[00\]" | cut -d "[" -f 3 | tr -d " %]"').read()
            if new_percent != percent:
                percent = new_percent
                print percent
                self.interface_action("local_progress_bar")
            fs_pid = os.popen("ps aux | awk '$11 == \"fsarchiver\" {print $2}'").read()


    def destructor(self):
       # Do a copy of berserker kernel to the windows partition
       subprocess.call('modprobe vfat', shell=True)
       subprocess.call('mkdir /mnt/dos', shell=True)
       subprocess.call('mount /dev/sda1 /mnt/dos', shell=True)
       subprocess.call('cp -f $media_path/custom/kernel /mnt/dos/', shell=True)
       subprocess.call('cp -f $media_path/custom/imagem.img /mnt/dos/imagem.img', shell=True)
       subprocess.call('umount /mnt/dos', shell=True)
       subprocess.call('rmdir /mnt/dos', shell=True)

       subprocess.call('modprobe ntfs', shell=True)
       subprocess.call('mkdir /mnt/windows', shell=True)
       subprocess.call('ntfs-3g /dev/sda4 /mnt/windows', shell=True)
       subprocess.call('cp -f $restore_path/i586/custom/kernel /mnt/windows/linux/kernel', shell=True)
       subprocess.call('cp -f $restore_path/i586/custom/imagem.img /mnt/windows/linux/imagem.img', shell=True)
       subprocess.call('umount /mnt/windows', shell=True)
       subprocess.call('rmdir /mnt/windows', shell=True)

    # disables initrd.resize
    def disable_resize(self):
        self.interface_action("local_progress_bar", "max_step=3")
        
        if 'keep_home' in os.environ and os.environ['keep_home'] == 'true':

            subprocess.call('mkdir -p ' + self.rootfs_dir, shell=True)
            subprocess.call('mount /dev/sda2 ' + self.rootfs_dir, shell=True)
            self.interface_action("local_progress_bar")
            
            subprocess.call('rm -f ' + self.rootfs_dir + '/etc/oem.d/user_files.sh', shell=True)
            directory = self.rootfs_dir + '/boot'
            subprocess.call("ln -sf initrd-$(ls " + self.rootfs_dir + "/lib/modules | sed 's@/@@').img initrd.img", shell=True, cwd=directory)
            directory = None
            self.interface_action("local_progress_bar")
            
            subprocess.call('umount ' + self.rootfs_dir, shell=True)
            self.interface_action("local_progress_bar")
        else:
            for _ in range(3):
                self.interface_action("local_progress_bar")

    # restore grub
    def restore_bootloader(self):
        # restore bootloader
        self.interface_action("local_progress_bar", "max_step=1")

        self.interface_action("local_progress_bar")
        if subprocess.call('echo -e "root (hd0,1)\nfind /boot/grub/menu.lst\nsetup (hd0)\nquit" | grub --batch', shell=True) != 0:
            return False

        return True

    def restore_bootloader_meego(self):
        self.interface_action("local_progress_bar", "max_step=3")
        subprocess.call("umount /mnt/rootfs", shell=True)
        subprocess.call("mkdir /mnt/rootfs", shell=True)
        subprocess.call("mount /dev/sda2 /mnt/rootfs", shell=True)
        subprocess.call("mount none /mnt/rootfs/dev -t devtmpfs", shell=True)
        subprocess.call("mount none /mnt/rootfs/proc -t proc", shell=True)
        subprocess.call("mount none /mnt/rootfs/sys -t sysfs", shell=True)
        
        self.interface_action("local_progress_bar")
        subprocess.call("dd if=/mnt/rootfs/usr/share/syslinux/mbr.bin of=/dev/sda bs=440 count=1", shell=True)

        self.interface_action("local_progress_bar")
        subprocess.call('cp -f /tmp/media/i586/isolinux/alt0/all.rdz /mnt/rootfs/boot', shell=True)
        subprocess.call('cp -f /tmp/media/i586/isolinux/alt0/vmlinuz /mnt/rootfs/boot', shell=True)

        self.interface_action("local_progress_bar")        
        subprocess.call("chroot /mnt/rootfs extlinux -i /boot/extlinux", shell=True)
        subprocess.call("umount /mnt/rootfs/proc", shell=True)
        subprocess.call("umount /mnt/rootfs/sys", shell=True)
        subprocess.call("umount /mnt/rootfs/dev", shell=True)
        subprocess.call("umount /mnt/rootfs", shell=True)

        return True

    # Philco eXclusive
    def restore_bootloader_philco(self):
        self.interface_action("local_progress_bar", "max_step=3")

        subprocess.call("mkdir /mnt/rootfs -p", shell=True)
        subprocess.call("mount /dev/sda3 /mnt/rootfs", shell=True)
        subprocess.call("mkdir /mnt/rootfs/boot", shell=True)

        self.interface_action("local_progress_bar", "message=Extraindo grub")
        subprocess.call("tar xvf $restore_path/custom/grub.tgz -C /mnt/rootfs/boot", shell=True)

        self.interface_action("local_progress_bar", "message=Copiando informações dos sistemas")
        subprocess.call("cp -f $restore_path/custom/kernel /mnt/rootfs/boot/kernel", shell=True)
        subprocess.call("cp -f $restore_path/custom/imagem.img /mnt/rootfs/boot/imagem.img", shell=True)
        subprocess.call("cp -f $restore_path/custom/menu.lst /mnt/rootfs/boot/grub/menu.lst", shell=True)

        self.interface_action("local_progress_bar", "message=Atualizando o grub")
        
        if subprocess.call('echo -e "root (hd0,2)\nfind /boot/grub/menu.lst\nsetup (hd0)\nquit" | grub --batch', shell=True) != 0:
            return False

        subprocess.call("umount /mnt/rootfs", shell=True)
        return True


    # write a log on tmp after install
    def write_log(self):
        self.interface_action("local_progress_bar", "max_step=1, message=Desmontando unidades.\n")
        subprocess.call('umount /mnt/rootfs/proc', shell=True)
        subprocess.call('umount /mnt/rootfs/sys', shell=True)
        subprocess.call('umount /mnt/rootfs', shell=True)
        subprocess.call('mount /dev/sda2 /mnt', shell=True)

        self.interface_action("local_progress_bar", "message=Escrevendo log em /mnt/tmp/install.log\n")
        subprocess.call('echo " 3G $has_3g Webcam $has_webcam Versao ' + self.oem_version + ' " >> /mnt/tmp/install.log', shell=True)
        subprocess.call('umount /mnt', shell=True)

    # discover which positivo brand was installed
    def install_version(self):
        #    mkdir -p "' + self.restore_dir + '"
        #    mount /dev/sda3 "' + self.restore_dir + '"
        
        if 'from_disk' in os.environ and os.environ['from_disk'] == "true":
            dvd_label = os.popen('isolabel -s /tmp/media/restore.iso | tr -d " "').read()
        else:        
            dvd_label = os.popen('isolabel -s '+ self.install_device + ' | tr -d " "').read()

                
        if subprocess.call('echo ' +  dvd_label + ' | grep -q 3g', shell=True) == 0:
            os.environ['has_3g'] = 'true'
        else:
            os.environ['has_3g'] = 'false'
        
        if subprocess.call('echo ' +  dvd_label + ' | grep -q cam', shell=True) == 0:
            os.environ['has_webcam'] = 'true'
        else:
            os.environ['has_webcam'] = 'false'

        self.oem_version = os.popen('echo ' +  dvd_label + ' | sed "s/3g//;s/cam//"'). read()

        os.environ['has_webcam'] = os.environ['has_webcam']
        os.environ['has_3g'] = os.environ['has_3g']
        os.environ['oem_version'] = self.oem_version

        #    umount ' + self.restore_dir + '

    # creates a password based on sha1sum
#    def write_password(self):
    
        #interface method.. Remove from this file
#        while [ "$pwd_ok" != true ]; do
#            password_1=$($DIALOG --entry --text="Informe a senha a ser usada para restaurar o Sistema Operacional:" --hide-text)
#            if [ -z "password_1" ]; then
#                $DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Nao foi informada uma senha valida. Tentar novamente?"
#                if [ $? != 0 ]; then
#                    exit
#               else
#                    pwd_ok=false
#                fi
#            fi
#            password_2=$($DIALOG --entry --text="Confirme a senha:" --hide-text)
#            if [ -z "password_2" ]; then
#                $DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Nao foi informada uma senha valida. Tentar novamente?"
#                if [ $? != 0 ]; then
#                    exit
#                else
#                    pwd_ok=false
#                fi
#            fi
#            if [ "$password_1" == "$password_2" ]; then
#                echo master_pwd=$(echo $password_1 | sha1sum | cut -d " " -f 1) > /mnt/educ/secret
#                pwd_ok=true
#            else
#                $DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Senhas diferem. Tentar novamente?"
#                if [ $? != 0 ]; then
#                    exit
#                else
#                    pwd_ok=false
#                fi
#            fi
#        done

    def check_password(self, string):
        password1 = password2 = None

        subprocess.call('mkdir -p ' + self.restore_dir, shell=True)
        subprocess.call('mount /dev/sda3 ' + self.restore_dir, shell=True)

        import hashlib
        password1 = hashlib.sha1(str(string) + '\n').hexdigest()
        password2 = open("/tmp/media/secret").read().rstrip()

        subprocess.call('umount /dev/sda3', shell=True)

        if password1 == password2:
            return True
        return False
        
    def create_hd_restore(self):
        self.interface_action("local_progress_bar", "max_step=6")

        subprocess.call('mkdir -p ' + self.restore_dir, shell=True)
        subprocess.call('mount /dev/sda3 ' + self.restore_dir, shell=True)
        subprocess.call('mkdir -p ' + self.restore_dir + '/install/stage2', shell=True)
        self.interface_action("local_progress_bar")

        subprocess.call('cp -f /tmp/media/i586/install/stage2/rescue.sqfs ' + self.restore_dir + '/install/stage2', shell=True)
        self.interface_action("local_progress_bar")

        subprocess.call('cp -f /tmp/media/i586/isolinux/alt0/all.rdz ' + self.restore_dir + '/', shell=True)
        self.interface_action("local_progress_bar")

        subprocess.call('cp -f /tmp/media/i586/isolinux/alt0/vmlinuz ' + self.restore_dir + '/', shell=True)
        self.interface_action("local_progress_bar")

        subprocess.call('echo mandriva | sha1sum | tr -d " -" > ' + self.restore_dir + '/secret', shell=True)
        self.interface_action("local_progress_bar")

        subprocess.call('umount ' + self.restore_dir, shell=True)
        subprocess.call('mount /dev/sda2 ' + self.restore_dir, shell=True)
        subprocess.call('umount ' + self.restore_dir, shell=True)
        subprocess.call('rmdir ' + self.restore_dir, shell=True)
        self.interface_action("local_progress_bar")
        
    def set_version(self, version):
    
        if version == "nobrand":
            version = os.popen('dmidecode --string baseboard-version | tr [A-Z] [a-z]'). read()
        
        if not version:
            return False
    
        self.oem_version = version
        os.environ['oem_version'] = version

        return True

    # This var need to keep in environ
    def set_3g(self, value):
        if value:
            os.environ['has_3g'] = 'true'
        else:
            os.environ['has_3g'] = 'false'
            
    # This var need to keep in environ
    def set_webcam(self, value):
        if value:
            os.environ['has_webcam'] = 'true'
        else:
            os.environ['has_webcam'] = 'false'

