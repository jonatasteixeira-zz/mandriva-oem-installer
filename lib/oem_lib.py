import os
import subprocess

class OemLib(object):
    def __init__(self, interface_action):
        self.interface_action = interface_action

    def init_positivo_installer(self):
        self.interface_action("local_progress_bar", "max_step=3, message=Preparando instalacao\n")
        subprocess.call('modprobe dm-mod &>/dev/null', shell=True)

        self.interface_action("local_progress_bar", "message=Levantando modulos")
        subprocess.call('modprobe ext4 &>/dev/null', shell=True)

        self.interface_action("local_progress_bar", "message=...")
        subprocess.call('drvinst &> /dev/null', shell=True)
        
        self.interface_action("local_progress_bar", "message=Feito\n")

    def start_instalation(self):
        self.interface_action("local_progress_bar", "max_step=14")
        
        os.environ['tmp_mount'] = "/tmp/vfat"
        self.interface_action("local_progress_bar")
        
        subprocess.call('mkdir $tmp_mount &>/dev/null', shell=True)
        self.interface_action("local_progress_bar")
        
        os.environ['extra_dir'] = os.environ['tmp_mount'] + "/extras"
        self.interface_action("local_progress_bar")
        
        os.environ['rootfs_dir'] = "/mnt/rootfs"
        self.interface_action("local_progress_bar")
        
        subprocess.call('mkdir -p $rootfs_dir', shell=True)
        self.interface_action("local_progress_bar")
        
        os.environ['restore_dir'] = os.environ['rootfs_dir'] + "/mnt/restore"
        self.interface_action("local_progress_bar")
        
        subprocess.call('mkdir -p $restore_dir/extras &>/dev/null', shell=True)
        self.interface_action("local_progress_bar")
        
        # should blacklist install media
        os.environ['blacklist'] = os.popen('mount | grep "/tmp/media" | cut -d " " -f 1 | sed "s#/dev/##"').read()
        self.interface_action("local_progress_bar")
        
        os.environ['install_device'] = os.popen('cat /proc/mounts | grep "/tmp/media" | cut -d" " -f1').read()
        self.interface_action("local_progress_bar")

        if subprocess.call('grep -q from_disk /proc/cmdline', shell=True) == 0:
            os.environ['from_disk'] = "true"
        self.interface_action("local_progress_bar")

        # Quack!!!
        if os.environ['install_device'] == "/dev/sr0":
            os.environ['install_device'] = "/dev/scd0"
        self.interface_action("local_progress_bar")        

    # Simple search for all removable devices
    def valid_block_devices(self):
        for sd in os.popen('ls /sys/block/ | egrep -i sd.*').read().split():
             if subprocess.call('grep -q 1 $i/removable', shell=True) == 0:
                cmd = "echo " + sd + " | cut -d "/" -f 4 | sed s/$blacklist//"
                os.environ['device'] = os.environ['device'] + os.popen('cmd').read()

    # Reads iso using blocksize and blockcounts
    def rawread(self, raw_device, iso_output):
        os.environ['raw_device'] = raw_device

        os.envirton['blocksize'] = os.popen('isoinfo -d -i $raw_device | grep "^Logical block size is:" | cut -d " " -f 5')
        if subprocess.call('test "$blocksize" = ""', shell=True) == 0:
            subprocess.call('echo catdevice FATAL ERROR: Blank blocksize >&2', shell=True)
            subprocess.call('exit', shell=True)
            return None

        os.environ['blockcount'] = os.popen('isoinfo -d -i $raw_device | grep "^Volume size is:" | cut -d " " -f 4')
        if subprocess.call('test "$blocksize" = ""', shell=True) == 0:
            subprocess.call('echo catdevice FATAL ERROR: Blank blockcount >&2', shell=True)
            subprocess.call('exit', shell=True)
            return None

        cmd = "dd if=" + os.environ['raw_device']
        cmd += " bs=" + os.environ['blocksize']
        cmd += " count=" + os.environ['blockcount'] 
        cmd += " conv=notrunc,noerror"

        os.environ['command'] = cmd
        print cmd + ' ' + iso_output
        subprocess.call('command > ' + iso_output)

    # install custom stuff in master mode (in "extras" dir)
    def install_extras(self, path):
        steps = 17 + len(os.popen('ls $tmp/*').read().split())
        self.interface_action("local_progress_bar", "max_step=" + str(steps))
        
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mount /dev/sda2 $rootfs_dir', shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mkdir -p $restore_dir', shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mount /dev/sda3 $restore_dir', shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mkdir -p $restore_dir/extras',  shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mount none $rootfs_dir/proc -t proc', shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mount none $rootfs_dir/sys -t sysfs', shell=True)
        
        os.environ['tmp'] = path

        self.interface_action("local_progress_bar", "message=Procurando arquivos pacote de otimizacao:\n")
        for os.environ['file'] in os.popen('ls $tmp/*').read().split():
            os.environ['install'] = os.popen('file $file | cut -d " " -f 2').read()
            subprocess.call('cp -f $file $restore_dir/extras/', shell=True)

            if os.environ['install'] == "gzip":
                self.interface_action("local_progress_bar", "message=   gzip encontrado!\n    descompactando...\n")
                subprocess.call('tar zxf $file -C $rootfs_dir', shell=True)
            elif os.environ['install'] == "bzip2":
                self.interface_action("local_progress_bar", "message=   tar encontrado!\n    descompactando...\n")
                subprocess.call('tar jxf $file -C $rootfs_dir', shell=True)
            elif os.environ['install'] == "Zip":
                self.interface_action("local_progress_bar", "message=   zip encontrado!\n    descompactando...\n")
                subprocess.call('unzip -q -o $file -d $rootfs_dir', shell=True)
            elif os.environ['install'] == "RPM":
                self.interface_action("local_progress_bar", "message=   rpm encontrado!\n    descompactando...\n")
                subprocess.call('cp -f $file $rootfs_dir', shell=True)
                subprocess.call('chroot $rootfs_dir rpm -U *.[RrPpMm]* --replacepkgs --nodeps &>/dev/null', shell=True)
                subprocess.call('rm -f $rootfs_dir/*.[RrPpMm]*', shell=True)
            elif os.environ['install'] == " ":
                subprocess.call('echo vazio', shell=True)
            else:
               self.interface_action("local_progress_bar", "message=\n")
                #Interface interact, it can't be here!!!!!
 #               $DIALOG --error --text="Arquivo de formato desconhecido";

        self.interface_action("local_progress_bar", "message=Otimizacao finalizada!\nFinalizando instalacao de pacotes extras.")
        subprocess.call('umount $rootfs_dir/proc', shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('umount $rootfs_dir/proc', shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('umount $rootfs_dir/sys', shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('umount $restore_dir', shell=True)
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('umount $rootfs_dir', shell=True)
        self.interface_action("local_progress_bar", "message=.\n")

    # Installs custom files (duuu)
    def install_custom_packages(self):
    
        self.install_version()

        self.interface_action("local_progress_bar", "max_step=14")

        self.interface_action("local_progress_bar", "message=Checando versao\n")
        if not 'oem_version' in os.environ:
            os.environ['oem_version'] = "positivo"

        self.interface_action("local_progress_bar", "message=Processando pacotes personalizados...\n")
        if subprocess.call('grep -q master_dump /proc/cmdline', shell=True) != 0:
            subprocess.call('mkdir /mnt/proc', shell=True)
            self.interface_action("local_progress_bar", "message=\tmkdir /mnt/proc")
            subprocess.call('mkdir /mnt/sys', shell=True)
            self.interface_action("local_progress_bar", "message=\tmkdir /mnt/sys")
            subprocess.call('mount /dev/sda2 /mnt', shell=True)
            self.interface_action("local_progress_bar", "message=\tmount /dev/sda2 /mnt")
            subprocess.call('mount none /mnt/proc -t proc', shell=True)
            self.interface_action("local_progress_bar", "message=\tmount none /mnt/proc -t proc")
            subprocess.call('mount none /mnt/sys -t sysfs', shell=True)
            self.interface_action("local_progress_bar", "message=\tmount none /mnt/sys -t sysfs")
            subprocess.call('cp -f /tmp/image/custom/*.rpm /mnt/tmp', shell=True)
            self.interface_action("local_progress_bar", "message=\tcp -f /tmp/image/custom/*.rpm /mnt/tmp")
            subprocess.call('chroot /mnt rpm -Uv /tmp/*.rpm --replacepkgs --nodeps', shell=True)
            self.interface_action("local_progress_bar", "message=\tchroot /mnt rpm -Uv /tmp/*.rpm --replacepkgs --nodeps")
            subprocess.call('rm -f /mnt/tmp/*.rpm', shell=True)
            self.interface_action("local_progress_bar", "message=\trm -f /mnt/tmp/*.rpm")
            subprocess.call('umount /mnt/proc', shell=True)
            self.interface_action("local_progress_bar", "message=\tumount /mnt/proc")
            subprocess.call('umount /mnt/sys', shell=True)
            self.interface_action("local_progress_bar", "message=\tumount /mnt/sys")
            subprocess.call('umount /mnt', shell=True)
            self.interface_action("local_progress_bar", "message=\tumount /mnt\n")

    # install extra files in master mode (zip, gzip, bzip2 and rpm are supported)
    def install_master_files(self):
        #duplicity :P
#        self.wait_for_it("Aguarde...")
        
        if subprocess.call('grep -q master_dump /proc/cmdline', shell=True) != 0:
            subprocess.call('mkdir /mnt/proc', shell=True)
            subprocess.call('mkdir /mnt/sys', shell=True)
            subprocess.call('mount /dev/sda2 /mnt', shell=True)
            subprocess.call('mount none /mnt/proc -t proc', shell=True)
            subprocess.call('mount none /mnt/sys -t sysfs', shell=True)
            subprocess.call('cp -f /tmp/image/custom/*.rpm /mnt/tmp', shell=True)
            subprocess.call('chroot /mnt rpm -Uv /tmp/*.rpm --replacepkgs --nodeps', shell=True)
            subprocess.call('rm -f /mnt/tmp/*.rpm', shell=True)
            subprocess.call('umount /mnt/proc', shell=True)
            subprocess.call('umount /mnt/sys', shell=True)
            subprocess.call('umount /mnt', shell=True)


        subprocess.call('mount /dev/sda3 $restore_dir', shell=True)
        subprocess.call('umount -f /tmp/vfat &>/dev/null', shell=True)

        # Interface action, can't be used here!!
#        $DIALOG --info --text="Insira o pendrive e pressione ENTER para continuar" 
#        sleep 7

        self.valid_block_devices()

        for dev in os.popen('echo $device').read().split():
            cmd = "mount /dev/"
            cmd += os.popen('echo ' + dev + '| tr -d [:space:]').read()
            cmd += "1 "
            cmd += os.environ['tmp_mount']
            
            status = subprocess.call(cmd, shell=True)
            
            if status != 0:
                # Interface action, it can't be here!!
                # $DIALOG --error --text="Nao foi possivel montar o pendrive" --timeout 3
                pass
            else:
                self.install_extras("/tmp/vfat/extras")
                break
                
            subprocess.call('umount $tmp_mount', shell=True)
            
        
        subprocess.call('kill $killpid', shell=True)
        
        # disabled, as I cannot remember why this is here :P
        #chroot "$rootfs_dir" rpm -U /tmp/extras/*.rpm --replacepkgs --nodeps &>/dev/null ; rm -f "$rootfs_dir/tmp/extras/*.[RrPpMm]*" &>/dev/null ;

        # remaster the iso to include all 3rd party files
#        self.wait_for_it("Aguarde, copiando arquivos de instalacao")
        
        subprocess.call('mount /dev/sda2 $rootfs_dir', shell=True)
        subprocess.call('mkdir -p $restore_dir/', shell=True)
        subprocess.call('mount /dev/sda3 $restore_dir', shell=True)
        subprocess.call('mkdir -p $rootfs_dir/tmp/install_media &>/dev/null', shell=True)
        subprocess.call('cp -fa /tmp/media/* $rootfs_dir/tmp/install_media &>/dev/null', shell=True)
        subprocess.call('mkdir -p $rootfs_dir/tmp/install_media/i586/custom/extras &>/dev/null', shell=True)
        subprocess.call('cp -af $restore_dir/extras/* $rootfs_dir/tmp/install_media/i586/custom/extras  &>/dev/null', shell=True)
        
        # Simulating a cd command
        # Can be used cwd=path flag or use os.chdir(path) to change current dir
        directory = os.popen('echo $rootfs_dir/tmp/install_media/').read()
#        subprocess.call('cd $rootfs_dir/tmp/install_media/', shell=True, cwd=directory)
        subprocess.call('rm -rf rr_moved', shell=True, cwd=directory)
        subprocess.call('kill $killpid', shell=True, cwd=directory)
        
        
        # There is some action with interface and it can't be here!!
        subprocess.call('mkisofs -V $oem_version -o $restore_dir/restore.iso '
                        + '-b i586/isolinux/isolinux.bin -c i586/isolinux/boot.cat '
                        + '-no-emul-boot -boot-load-size 4 -boot-info-table '
                        + '-J -R . 2>&1 ', shell=True, cwd=directory)
                        
        
        # | $DIALOG --progress --pulsate --text="Aguarde, gerando iso..." --auto-close
        
        directory=None
        # cd -


        # prepare label, installer parses label to decide if it is a master or a
        # normal install procedure

#        self.wait_for_it("Finalizando...")

        os.environ['extras'] = ''

        if 'has_3g' in os.environ:
            if os.environ['has_3g'] == 'true':
                os.environ['extras'] += '3g'
                
        if 'has_webcam' in os.environ:
            if os.environ['has_webcam'] == 'true':
                os.environ['extras'] += 'cam'


        label = os.popen('echo $oem_version$extras').read()

        #Interface action, it can't be here!!
        subprocess.call('1isolabel -n 1' + label + ' $restore_dir/restore.iso', shell=True)
        # || error_msg
        subprocess.call('isohybrid $restore_dir/restore.iso', shell=True)
        
        #Interface action, it can't be here!!
        subprocess.call('implantisomd5 -f $restore_dir/restore.iso', shell=True)
        # || error_msg
        
        subprocess.call('rm -rf  $rootfs_dir/tmp/install_media', shell=True)
        subprocess.call('umount "$restore_dir"', shell=True)
        subprocess.call('umount "$rootfs_dir"', shell=True)
        subprocess.call('rmdir "$tmp_mount"', shell=True)
        subprocess.call('kill $killpid', shell=True)

    # just generates default install iso (for master, use install extras)
    def gen_iso_install(self):
        self.interface_action("local_progress_bar", "max_step=6, message=Criando arvore de diretorios")

        subprocess.call('mkdir $restore_dir &>/dev/null', shell=True)
        self.interface_action("local_progress_bar", "message=...")
        
        subprocess.call('mount /dev/sda3 $restore_dir', shell=True)
        self.interface_action("local_progress_bar", "message=... Feito!\n")

        os.environ['restore_iso'] = os.popen('echo $restore_dir/restore.iso').read()

        self.interface_action("local_progress_bar", "message=Checando instalacao de dispositivos.")
        
        print 'dev/sd =~ ' + os.environ['install_device']
        if '/dev/sd' in os.environ['install_device']:
            self.interface_action("local_progress_bar", "message=Instalando dispositivos...")
            os.environ['raw_size'] = os.popen('isosize $install_device').read()
            blocks = os.popen('echo $(( raw_size / (1048576 * 4) ))').read()
            blocks = int(blocks) + 10
            subprocess.call('dd if=$install_device of=$restore_iso bs=4M count=' + str(blocks) , shell=True)
        else:
            self.interface_action("local_progress_bar", "message=Salvando iso de restauracao...")
            self.rawread(os.environ['install_device'], os.environ['restore_iso'])
        
        self.interface_action("local_progress_bar", "message= Feito!\n")
        
        self.interface_action("local_progress_bar", "message=Verificando codigo de integridade...")
        # The return of checkusomd5 is inverse

        print "checkisomd5 " + os.environ['restore_iso']
        if subprocess.call('checkisomd5 $restore_iso', shell=True) == 1:
            self.interface_action("local_progress_bar", "message= Feito\n")
            subprocess.call('umount $restore_dir', shell=True)
        else:
            self.interface_action("local_progress_bar", "message= Falha na checagem!\n")
            return False

        return True

    def create_part(self):
        self.interface_action("local_progress_bar", "max_step=3")
        self.interface_action("local_progress_bar", "message=Verificando home\n")

        if 'keep_home' in os.environ:
            if os.environ['keep_home'] == 'true':
                subprocess.call("cat /tmp/image/data/box/sda.dump | sed -e '/sda4/ s/size=.*,/size= ,/' | sfdisk -f /dev/sda &> /dev/null", shell=True)
            else:
                subprocess.call('cat /tmp/image/data/box/sda.dump | sfdisk -f /dev/sda &> /dev/null')
        self.interface_action("local_progress_bar", "message=Particionando...")

        status = subprocess.call('sfdisk -R /dev/sda', shell=True)
        self.interface_action("local_progress_bar", "message= Feito!\n")
        
        return (status == 0)
        

# create partitions from sfdisk dump
#create_part(){
#    wait_for_it "Criando tabela de particoes, aguarde..." 
#    # creates new partition table based on dump image
#    cat /tmp/image/data/box/sda.dump | sfdisk -f /dev/sda &> /dev/null
#    sleep 2
#    sfdisk -R /dev/sda
#    kill $killpid
#}

    # parse fsarchiver log (please, improve-me)
    def parse_log(self):
        self.interface_action("local_progress_bar", "max_step=100")
        
        subprocess.call('sleep 5', shell=True)
        
        fs_pid = os.popen("ps aux | awk '$11 == \"fsarchiver\" { print $2 }'").read()
        
        percent = 0
        while fs_pid != "":
            new_percentage = os.popen('tail -n1 /tmp/fs.log | grep "\-\[00\]" | cut -d "[" -f 3 | tr -d " %]"').read()
            if new_percent != percent:
                percent = new_percent
                print percent
                self.interface_action("local_progress_bar")
            fs_pid = os.popen("ps aux | awk '$11 == \"fsarchiver\" {print $2}'").read()


        # format swap partition
    def format_swap(self, dev):
        self.interface_action("local_progress_bar", "max_step=2")
        self.interface_action("local_progress_bar", "message=...")
       
        ret = subprocess.call('mkswap /dev/' + dev + ' &>/dev/null', shell=True)
        self.interface_action("local_progress_bar", "message= Feito\n")
        
        return (ret == 0)

    # restore desired partition
    def restore_part(self, arg):
        if 'from_disk' in os.environ:
            if os.environ['from_disk'] != '':    
                os.environ['restore_path'] = '/tmp/loop'
            else:
                os.environ['restore_path'] = '/tmp/media'

        cmd = 'fsarchiver -v restfs $restore_path/i586/data/box/backup.sda' + arg + '.fsa id=0,dest=/dev/sda' + arg + ' &>/tmp/fs.log'
        subprocess.call(cmd, shell=True)

#        self.parse_log()

    # resize desired partition to its maximum size
    def resize_part(self, arg):
        print "this?"
        subprocess.call('e2fsck -f -y /dev/sda' + arg + ' &>/dev/null', shell=True)
        print "this?"
        subprocess.call('resize2fs /dev/sda' + arg + ' &>/dev/null', shell=True)

    # loop to restore all partitions
    def restore_parts(self):
        parts = "2"
        
        print "inside 1"
        
        if not 'from_disk' in os.environ or os.environ['from_disk'] == '':
            parts += " 3"
        
        print "inside 2"
        if not 'keep_home' in os.environ or os.environ['keep_home'] == '':
            parts += " 4"
 
        print "inside 3"
        self.interface_action("local_progress_bar", "max_step=" + str(len(parts.split()) * 2))
        
        for part in parts.split():
            print part
            print "inside loop a"
            self.restore_part(part)
            self.interface_action("local_progress_bar")
            print "inside loop b"
            self.resize_part(part)
            self.interface_action("local_progress_bar")
        print "inside end"

    def destructor(self):
       # Do a copy of berserker kernel to the windows partition
       subprocess.call('modprobe vfat', shell=True)
       subprocess.call('mkdir /mnt/dos &>/dev/null', shell=True)
       subprocess.call('mount /dev/sda1 /mnt/dos', shell=True)
       subprocess.call('cp -f $media_path/custom/kernel /mnt/dos/', shell=True)
       subprocess.call('cp -f $media_path/custom/imagem.img /mnt/dos/imagem.img', shell=True)
       subprocess.call('umount /mnt/dos', shell=True)
       subprocess.call('rmdir /mnt/dos', shell=True)

       subprocess.call('modprobe ntfs', shell=True)
       subprocess.call('mkdir /mnt/windows &>/dev/null', shell=True)
       subprocess.call('ntfs-3g /dev/sda4 /mnt/windows', shell=True)
       subprocess.call('cp -f $restore_path/i586/custom/kernel /mnt/windows/linux/kernel', shell=True)
       subprocess.call('cp -f $restore_path/i586/custom/imagem.img /mnt/windows/linux/imagem.img', shell=True)
       subprocess.call('umount /mnt/windows', shell=True)
       subprocess.call('rmdir /mnt/windows', shell=True)

    # ask if user wishes to keep its home (last part)
    def ask_home(self):
        subprocess.call('mkdir -p $rootfs_dir', shell=True)
        subprocess.call('mount /dev/sda2 $rootfs_dir &>/dev/null', shell=True)
        
        if os.path.exists(os.environ['rootfs_dir'] + '/etc/oem-release'):
            return True

    def answer_home(self, home):
        if home:
            os.environ['keep_home'] = 'true'

        subprocess.call('umount $rootfs_dir', shell=True)

    # disables initrd.resize
    def disable_resize(self):
        self.interface_action("local_progress_bar", "max_step=7")
        complete_bar = False
        
        if 'keep_home' in os.environ:
            if os.environ['keep_home '] == 'true':
                self.interface_action("local_progress_bar", "message=.")
                subprocess.call('mkdir -p $rootfs_dir', shell=True)
                
                self.interface_action("local_progress_bar", "message=.")
                subprocess.call('mount /dev/sda2 $rootfs_dir', shell=True)
                
                self.interface_action("local_progress_bar", "message=.")
                subprocess.call('rm -f $rootfs_dir/etc/oem.d/user_files.sh', shell=True)
                
                self.interface_action("local_progress_bar", "message=.")
                directory = os.popen=('echo $rootfs_dir/boot').read()
                
                self.interface_action("local_progress_bar", "message=.")
                subprocess.call("ln -sf initrd-$(ls $rootfs_dir/lib/modules | sed 's@/@@').img initrd.img", shell=True, cwd=directoy)
                
                self.interface_action("local_progress_bar", "message=.")
                directory = None
                subprocess.call('umount $rootfs_dir', shell=True)
            else:
                complete_bar = True
        else:
            complete_bar = True
            
        if complete_bar:    
            for _ in range(6):
                self.interface_action("local_progress_bar", "message=.")

        self.interface_action("local_progress_bar", "message=\n")
    
    # restore grub
    def restore_bootloader(self):
        # restore bootloader
        self.interface_action("local_progress_bar", "max_step=2")

        self.interface_action("local_progress_bar")
        if subprocess.call('echo -e "root (hd0,1)\nfind /boot/grub/menu.lst\nsetup (hd0)\nquit" | grub --batch', shell=True) != 0:
            return False
            
        self.interface_action("local_progress_bar")

        return True

    # write a log on tmp after install
    def write_log(self):
        self.interface_action("local_progress_bar", "max_step=7, message=Desmontando unidades.")
        subprocess.call('umount /mnt/rootfs/proc &>/dev/null', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('umount /mnt/rootfs/sys &>/dev/null', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('umount /mnt/rootfs &>/dev/null', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mount /dev/sda2 /mnt', shell=True)

        self.interface_action("local_progress_bar", "message=Escrevendo log em /mnt/tmp/install.log")
        subprocess.call('echo " 3G $has_3g Webcam $has_webcam Versao $oem_version " >> /mnt/tmp/install.log', shell=True)

        self.interface_action("local_progress_bar", "message=. Feito!\n")
        subprocess.call('umount /mnt', shell=True)


    # ask positivo desired brand
#    ask_version(){
#        #interface Action.. It cant be here!!
#        oem_version=$($DIALOG --list --text="Escolha a imagem:" --column="Versao:" --column="Descricao:" positivo "imagem positivo" \
#        nobrand "imagem nobrand" \
#        unionpc "imagem unionpc" \
#        corporativo "imagem corporativo" \
#        unique "imagem positivo unique")

#        if [ "$oem_version" == "nobrand" ]; then
#            oem_version=$(dmidecode --string baseboard-version | tr [A-Z] [a-z])
#        fi
#            export oem_version
#        if [ -z "$oem_version" ]; then
#            $DIALOG --warning --text="Instalacao abortada\!" 
#            reboot
#        fi
#   }

    def reboot(self):
        subprocess.call('reboot', shell=True)

    # discover which positivo brand was installed
    def install_version(self):
        #    mkdir -p "$restore_dir"
        #    mount /dev/sda3 "$restore_dir"
        
        if 'from_disk' in os.environ and os.environ['from_disk'] != "":
            os.environ['dvd_label'] = os.popen('isolabel -s /tmp/media/restore.iso | tr -d " "').read()
        else:        
            os.environ['dvd_label'] = os.popen('isolabel -s $install_device | tr -d " "').read()
                
        if subprocess.call('echo $dvd_label | grep -q 3g', shell=True) == 0:
            os.environ['has_3g'] = 'true'
        else:
            os.environ['has_3g'] = 'false'
        
        
        if subprocess.call('echo $dvd_label | grep -q cam', shell=True) == 0:
            os.environ['has_webcam'] = 'true'
        else:
            os.environ['has_webcam'] = 'false'

        os.environ['oem_version'] = os.popen('echo $dvd_label | sed "s/3g//;s/cam//"'). read()
        
        # export has_webcam
        # export has_3g
        # export oem_version

        #    umount $restore_dir

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


    # checks if the password matches
#    def check_password(self):
    #    mkdir -p $restore_dir
    #    mount /dev/sda3 $restore_dir
#        while [ "$password" != "OK" ]; do
#                    plain_pwd=$($DIALOG --entry --text="Informe a senha para restaurar o Sistema Operacional: " --hide-text)
#            if [ $? != 0 ]; then
#                $DIALOG --info --text="Instalacao abortada!"
#                reboot
#            fi
#            password_1=$(echo $plain_pwd | sha1sum | cut -d " " -f 1)
#            password_2=$(cat /tmp/media/secret)
#                   if [ "$password_1" == "$password_2" ]; then
#                            password="OK"
#                    else
#                            $DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Senha nao confere, tentar novamente?"
#                            if [ "$?" != "0" ]; then
#                                    reboot
#                            fi
#                    fi
#        done
#    }

    def create_hd_restore(self):
        self.interface_action("local_progress_bar", "max_step=11")
        subprocess.call('mkdir -p $restore_dir', shell=True)
        
        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mount /dev/sda3 $restore_dir', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mkdir -p $restore_dir/install/stage2', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('cp -f /tmp/media/i586/install/stage2/rescue.sqfs $restore_dir/install/stage2', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('cp -f /tmp/media/i586/isolinux/alt0/all.rdz $restore_dir/', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('cp -f /tmp/media/i586/isolinux/alt0/vmlinuz $restore_dir/', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('echo mandriva | sha1sum | tr -d " -" > $restore_dir/secret', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('umount $restore_dir', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('mount /dev/sda2 $restore_dir', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('umount $restore_dir', shell=True)

        self.interface_action("local_progress_bar", "message=.")
        subprocess.call('rmdir $restore_dir', shell=True)

        self.interface_action("local_progress_bar", "message=\n")

    def set_3g(self, value):
        if value:
            os.environ['has_3g'] = 'true'
        else:
            os.environ['has_3g'] = 'false'

    def set_webcam(self, value):
        if value:
            os.environ['has_webcam'] = 'true'
        else:
            os.environ['has_webcam'] = 'false'
            
