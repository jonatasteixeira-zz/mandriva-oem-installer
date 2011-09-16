#!/bin/bash
DIALOG="zenity --title Mandriva_Linux "
tmp_mount="/tmp/vfat"
mkdir "$tmp_mount" &>/dev/null
extra_dir="$tmp_mount/extras"
rootfs_dir="/mnt/rootfs"
mkdir -p $rootfs_dir
restore_dir="$rootfs_dir/mnt/restore"
mkdir -p "$restore_dir/extras" &>/dev/null
# should blacklist install media
blacklist=$(mount | grep "/tmp/media" | cut -d ' ' -f 1 | sed "s#/dev/##")
install_device=$(cat /proc/mounts | grep "/tmp/media" | cut -d' ' -f1)
if grep -q from_disk /proc/cmdline; then
	from_disk=true
fi
# quack !!!!
if [ $install_device == "/dev/sr0" ]; then
        install_device=/dev/scd0
fi

# standard wait for it msg
wait_for_it(){
	(while true; do echo ; sleep 1; done) |  $DIALOG --progress --pulsate --text="$1" &
	killpid=$!
}

# standard error msg
error_msg(){
	$DIALOG --error --text="Ocorreu um erro durante a instalacao, verifique a midia e tente novamente." 
	reboot
}


# simple search for all removable devices
valid_block_devices(){
	for i in /sys/block/sd*; do
        	if grep -q 1 $i/removable; then
            		device="$device $(echo $i | cut -d "/" -f 4 | sed s/$blacklist//)"
        	fi
	done
}


# reads iso using blocksize and blockcounts
rawread(){
	raw_device=$1
	blocksize=`isoinfo -d -i $raw_device | grep "^Logical block size is:" | cut -d " " -f 5`
	if test "$blocksize" = ""; then
        	echo catdevice FATAL ERROR: Blank blocksize >&2
	        exit
	fi
	blockcount=`isoinfo -d -i $raw_device | grep "^Volume size is:" | cut -d " " -f 4`
	if test "$blockcount" = ""; then
        	echo catdevice FATAL ERROR: Blank blockcount >&2
	        exit
	fi
	dd if=$raw_device bs=$blocksize count=$blockcount conv=notrunc,noerror
}


# install custom stuff in master mode (in "extras" dir)
install_extras(){ 
	mount /dev/sda2 "$rootfs_dir"
	mkdir -p "$restore_dir"
	mount /dev/sda3 "$restore_dir"
	mkdir -p "$restore_dir/extras"
	mount none "$rootfs_dir/proc" -t proc
	mount none "$rootfs_dir/sys" -t sysfs
	wait_for_it "Aguarde..." 
	for file in $(ls $1/*); do
		install=$(file "$file" | cut -d " " -f 2)
       		cp -f "$file" "$restore_dir/extras/"
		case "$install" in
       			gzip) tar zxf "$file" -C "$rootfs_dir";;
	        	bzip2) tar jxf "$file" -C "$rootfs_dir";;
       			Zip) unzip -q -o "$file" -d "$rootfs_dir";;
	       		RPM) cp -f "$file" "$rootfs_dir"; chroot "$rootfs_dir" rpm -U *.[RrPpMm]* --replacepkgs --nodeps &>/dev/null; rm -f "$rootfs_dir/*.[RrPpMm]*";;
			" ") echo vazio ;;
			*) $DIALOG --error --text="Arquivo de formato desconhecido";;
		esac
	done
	umount "$rootfs_dir/proc"
	umount "$rootfs_dir/sys"
	umount "$restore_dir"
	umount "$rootfs_dir"
	kill $killpid
}


# installs custom files (duuu)
install_custom_packages(){
	install_version
	if [ -z "$oem_version" ]; then
	        oem_version=positivo
	fi

	wait_for_it "Aguarde..." 
	if ! grep -q master_dump /proc/cmdline; then
		export oem_version
		export has_3g
		export has_webcam
		mkdir /mnt/proc
		mkdir /mnt/sys
		mount /dev/sda2 /mnt
		mount none /mnt/proc -t proc
		mount none /mnt/sys -t sysfs
		cp -f /tmp/image/custom/*.rpm /mnt/tmp
		chroot /mnt rpm -Uv /tmp/*.rpm --replacepkgs --nodeps
		rm -f /mnt/tmp/*.rpm
		umount /mnt/proc
		umount /mnt/sys
		umount /mnt
		kill $killpid
	fi
}


# install extra files in master mode (zip, gzip, bzip2 and rpm are supported)
install_master_files(){
	#duplicity :P
	wait_for_it "Aguarde..." 
	if ! grep -q master_dump /proc/cmdline; then
		mkdir /mnt/proc
		mkdir /mnt/sys
		mount /dev/sda2 /mnt
		mount none /mnt/proc -t proc
		mount none /mnt/sys -t sysfs
		cp -f /tmp/image/custom/*.rpm /mnt/tmp
		chroot /mnt rpm -Uv /tmp/*.rpm --replacepkgs --nodeps
		rm -f /mnt/tmp/*.rpm
		umount /mnt/proc
		umount /mnt/sys
		umount /mnt
	fi

	mount /dev/sda3 "$restore_dir"
	umount -f /tmp/vfat &>/dev/null

	$DIALOG --info --text="Insira o pendrive e pressione ENTER para continuar" 
	sleep 7

	valid_block_devices

	for dev in $(echo $device); do
		mount /dev/$(echo $dev | tr -d [:space:])1 $tmp_mount 
		if [ "$?" != 0 ]; then
			$DIALOG --error --text="Nao foi possivel montar o pendrive" --timeout 3
		else
			install_extras /tmp/vfat/extras
		        break
		fi
    		umount "$tmp_mount"
	done
	kill $killpid
	# disabled, as I cannot remember why this is here :P
	#chroot "$rootfs_dir" rpm -U /tmp/extras/*.rpm --replacepkgs --nodeps &>/dev/null ; rm -f "$rootfs_dir/tmp/extras/*.[RrPpMm]*" &>/dev/null ;
	# remaster the iso to include all 3rd party files
	wait_for_it "Aguarde, copiando arquivos de instalacao" 
	mount /dev/sda2 "$rootfs_dir"
	mkdir -p $restore_dir/
	mount /dev/sda3 "$restore_dir"
	mkdir -p $rootfs_dir/tmp/install_media &>/dev/null
	cp -fa /tmp/media/* $rootfs_dir/tmp/install_media &>/dev/null
	mkdir -p $rootfs_dir/tmp/install_media/i586/custom/extras &>/dev/null
	cp -af $restore_dir/extras/* $rootfs_dir/tmp/install_media/i586/custom/extras  &>/dev/null
	cd $rootfs_dir/tmp/install_media/
	rm -rf rr_moved
	kill $killpid
	mkisofs -V "$oem_version" -o $restore_dir/restore.iso -b i586/isolinux/isolinux.bin -c i586/isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -J -R . 2>&1 | $DIALOG --progress --pulsate --text="Aguarde, gerando iso..." --auto-close
	cd -

	# prepare label, installer parses label to decide if it is a master or a
	# normal install procedure
		
	kill $killpid
	wait_for_it "Finalizando..." 
	if [ "$has_3g" == true ]; then
        	extras=3g
	fi
	if [ "$has_webcam" == true ]; then
	        extras="${extras}cam"
	fi
	label="${oem_version}${extras}"
	isolabel -n "$label" $restore_dir/restore.iso || error_msg
	isohybrid $restore_dir/restore.iso
	implantisomd5 -f $restore_dir/restore.iso || error_msg
	rm -rf  $rootfs_dir/tmp/install_media
	umount "$restore_dir"
	umount "$rootfs_dir"
	rmdir "$tmp_mount"
	kill $killpid
}


# just generates default install iso (for master, use install extras)
gen_iso_install(){
	wait_for_it "Gerando iso de instalacao, aguarde..." 
	mkdir $restore_dir &>/dev/null
	mount /dev/sda3 $restore_dir

	restore_iso=$restore_dir/restore.iso
	
	if [[ "$install_device" =~ /dev/sd ]]; then
	        raw_size=$(isosize $install_device)
	        blocks=$(( raw_size / (1048576 * 4) )) # from 'dd' manpage: 1048576 is 1M
	        dd if=$install_device of=$restore_iso bs=4M count=$((blocks + 10)) # +10 is just to be safe
	else
        	rawread $install_device > $restore_iso

	fi

	checkisomd5 $restore_iso

	if [ $? = 1 ]; then
        	umount $restore_dir
	else
		error_msg
	fi
	kill $killpid
}

# creates new partition table based on dump image
create_part(){
       	if [ "$keep_home" == true ]; then
               	cat /tmp/image/data/box/sda.dump${1} | sed -e '/sda4/ s/size=.*,/size= ,/' | sfdisk -f /dev/sda &> /dev/null
        else
       	        cat /tmp/image/data/box/sda.dump${1} | sfdisk -f /dev/sda &> /dev/null
        fi
        
       	sleep 2
        sfdisk -R /dev/sda
}


# create partitions from sfdisk dump
#create_part(){
#	wait_for_it "Criando tabela de particoes, aguarde..." 
#	# creates new partition table based on dump image
#	cat /tmp/image/data/box/sda.dump | sfdisk -f /dev/sda &> /dev/null
#	sleep 2
#	sfdisk -R /dev/sda
#	kill $killpid
#}


# parse fsarchiver log (please, improve-me)
parse_log(){
        percentage=0
        sleep 5
        fs_pid=$(ps aux | awk '$11 == "fsarchiver" { print $2 }')
        (while [ -n "$fs_pid" ]; do percentage=$(tail -n1 /tmp/fs.log | grep "\-\[00\]" | cut -d "[" -f 3 | tr -d " %]"); if [ -z "$percentage" ]; then percentage=0; fi; echo $percentage ; sleep 1; fs_pid=$(ps aux | awk '$11 == "fsarchiver" {print $2}'); done) | $DIALOG --progress --text "Progresso da instalacao, aguarde..."; zenity_pid=$!
       kill $zenity_pid	
}


# format swap partition
format_swap(){
	mkswap /dev/${1} &>/dev/null
}


# restore desired partition
restore_part(){
        parse_log &
	if [ -n "$from_disk" ]; then
		restore_path="/tmp/loop/i586"
	else
		restore_path="/tmp/image"
	fi
        fsarchiver -v restfs $restore_path/data/box/backup.sda${1}.fsa id=0,dest=/dev/sda${1},mkfs=ext3 &>/tmp/fs.log
}


# resize desired partition to its maximum size
resize_part(){
	e2fsck -f -y /dev/sda${1} &>/dev/null
	resize2fs /dev/sda${1} &>/dev/null
}


# loop to restore all partitions
restore_parts(){
	parts="2"
	if [ -z "$from_disk" ]; then
		parts="$parts 3"
	fi
	if [ -z "$keep_home" ]; then
		parts="$parts 4"
	fi
	for part in $parts; do
		restore_part $part 
		resize_part $part 
	done
}

# restore in master mode (philco)
restore_parts_philco(){
	parts="2 3"
	for part in $parts; do
		restore_part $part 
		resize_part $part 
	done
	# fscking hack
	sfdisk -R /dev/sda
	sleep 2
	sfdisk -d /dev/sda | sed 's/Id=93/Id=83/' | sfdisk -f /dev/sda
	sleep 2
	sfdisk -R /dev/sda
}

destructor(){
       # copia o kernel destruidor para a parti��o windows
       modprobe vfat
       mkdir /mnt/dos &>/dev/null
       mount /dev/sda1 /mnt/dos
       cp -f $restore_path/custom/kernel /mnt/dos/
       cp -f $restore_path/custom/imagem.img /mnt/dos/imagem.img
       umount /mnt/dos
       rmdir /mnt/dos

       modprobe ntfs
       mkdir /mnt/windows &>/dev/null
       ntfs-3g /dev/sda4 /mnt/windows
       cp -f $restore_path/custom/kernel /mnt/windows/linux/kernel
       cp -f $restore_path/custom/imagem.img /mnt/windows/linux/imagem.img
       umount /mnt/windows
       rmdir /mnt/windows
}

# ask for install confirmation or reboot
confirm_install(){
	$DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Confirma a reinstalacao do sistema? Este procedimento apagara todos os seus dados!"
	if [ $? != 0 ]; then 
		reboot
	fi
}


# ask if user wishes to keep its home (last part)
ask_home(){
	mkdir -p $rootfs_dir
	mount /dev/sda2 $rootfs_dir &>/dev/null
	if [ -e $rootfs_dir/etc/oem-release ]; then
		$DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Deseja salvar os dados do usuario (particao home)?"
		if [ $? == 0 ]; then
			keep_home=true
		fi
	fi
	umount $rootfs_dir
}


# disables initrd.resize
disable_resize(){
	if [ "$keep_home" == true ]; then
	    mkdir -p $rootfs_dir 
	    mount /dev/sda2 $rootfs_dir
	    rm -f $rootfs_dir/etc/oem.d/user_files.sh
	    cd $rootfs_dir/boot
	    ln -sf initrd-$(ls $rootfs_dir/lib/modules | sed 's@/@@').img initrd.img
	    cd -
	    umount $rootfs_dir
	fi
}


# restore grub
restore_bootloader(){
	# restore bootloader
	grub --batch <<EOF
	root (hd0,1)
	find /boot/grub/menu.lst
	setup (hd0)
	quit
	EOF
}

# philco eXclusive
restore_bootloader_philco(){
	mkdir /mnt/rootfs -p
	mount /dev/sda3 /mnt/rootfs
	mkdir -p /mnt/rootfs/boot 
	tar xvf $restore_path/custom/grub.tgz -C /mnt/rootfs/boot
	cp -f $restore_path/custom/kernel /mnt/rootfs/boot/kernel
	cp -f $restore_path/custom/imagem.img /mnt/rootfs/boot/imagem.img
	cp -f $restore_path/custom/menu.lst /mnt/rootfs/boot/grub/menu.lst
	grub --batch <<EOF
	root (hd0,2)
	find /boot/grub/menu.lst
	setup (hd0)
	quit
	EOF
	umount /mnt/rootfs
}

# write a log on tmp after install
write_log(){
	# FSCKING LOG!!!!!!!!!!!
	umount /mnt/rootfs/proc &>/dev/null
	umount /mnt/rootfs/sys &>/dev/null
	umount /mnt/rootfs &>/dev/null
	mount /dev/sda2 /mnt
	echo " 3G $has_3g Webcam $has_webcam Versao $oem_version " >> /mnt/tmp/install.log
	umount /mnt
}


# ask positivo desired brand
ask_version(){
	oem_version=$($DIALOG --list --text="Escolha a imagem:" --column="Versao:" --column="Descricao:" positivo "imagem positivo" \
	neopc "imagem neopc" \
	sim "imagem sim+" \
	firstline "imagem firstline" \
	pcdafamilia "imagem pc-da-familia" \
	positivofaces "imagem ipanema" \
	familiafaces "imagem ipanema + pc-da-familia" \
	corporativo "imagem positivo corporativo" \
	masterbrand "imagem positivo master" \
	aureum "imagem notebook aureum" \
	moboblack "imagem netbook mobo" \
	unionpc "imagem unionpc" \
	kennex "imagem kennex" \
	professor-m74 "imagem professor M74xS" \
	unique "imagem positivo unique" \
	moboblackmaster "imagem master mobo" \
	unionmaster "imagem unionpc master") 
	export oem_version
	if [ -z "$oem_version" ]; then
		$DIALOG --warning --text="Instalacao abortada\!" 
		reboot
	fi
}


# discover which positivo brand was installed
install_version(){
#	mkdir -p "$restore_dir"
#	mount /dev/sda3 "$restore_dir"
	if [ -n "$from_disk" ]; then
		dvd_label=$(isolabel -s /tmp/media/restore.iso | tr -d ' ')
	else
		dvd_label=$(isolabel -s "$install_device" | tr -d ' ')
	fi
	if echo "$dvd_label" | grep -q 3g; then
	        has_3g=true
	else
	        has_3g=false
	fi
	if echo "$dvd_label" | grep -q cam; then
	        has_webcam=true
	else
	        has_webcam=false
	fi
	export has_webcam
	export has_3g

	oem_version=$(echo $dvd_label | sed 's/3g//;s/cam//')
	export oem_version
#	umount $restore_dir
}


# creates a password based on sha1sum
write_password(){
	while [ "$pwd_ok" != true ]; do
        	password_1=$($DIALOG --entry --text="Informe a senha a ser usada para restaurar o Sistema Operacional:" --hide-text)
	        if [ -z "password_1" ]; then
        	        $DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Nao foi informada uma senha valida. Tentar novamente?"
	                if [ $? != 0 ]; then
				exit
	                else
	                        pwd_ok=false
	                fi
		fi
        	password_2=$($DIALOG --entry --text="Confirme a senha:" --hide-text)
	        if [ -z "password_2" ]; then
        	        $DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Nao foi informada uma senha valida. Tentar novamente?"
	                if [ $? != 0 ]; then
				exit
	                else
	                        pwd_ok=false
	                fi
		fi
		if [ "$password_1" == "$password_2" ]; then
	                echo master_pwd=$(echo $password_1 | sha1sum | cut -d " " -f 1) > /mnt/educ/secret
	                pwd_ok=true
		else
			$DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Senhas diferem. Tentar novamente?"
			if [ $? != 0 ]; then
                                exit
                        else
                                pwd_ok=false
                        fi
	        fi
	done
}


# checks if the password matches
check_password(){
#	mkdir -p $restore_dir
#	mount /dev/sda3 $restore_dir
	while [ "$password" != "OK" ]; do
                plain_pwd=$($DIALOG --entry --text="Informe a senha para restaurar o Sistema Operacional: " --hide-text)
		if [ $? != 0 ]; then
			$DIALOG --info --text="Instalacao abortada!"
			reboot
		fi
		password_1=$(echo $plain_pwd | sha1sum | cut -d " " -f 1)
		password_2=$(cat /tmp/media/secret)
                if [ "$password_1" == "$password_2" ]; then
                        password="OK"
                else
                        $DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Senha nao confere, tentar novamente?"
                        if [ "$?" != "0" ]; then
                                reboot
                        fi
                fi
	done
}

create_hd_restore(){
	mkdir -p $restore_dir
	mount /dev/sda3 $restore_dir
	mkdir -p $restore_dir/install/stage2
	cp -f /tmp/media/i586/install/stage2/rescue.sqfs $restore_dir/install/stage2
	cp -f /tmp/media/i586/isolinux/alt0/all.rdz $restore_dir/
	cp -f /tmp/media/i586/isolinux/alt0/vmlinuz $restore_dir/
	echo mandriva | sha1sum | tr -d ' -' > $restore_dir/secret

	umount $restore_dir
	mount /dev/sda2 $restore_dir
	umount $restore_dir
	rmdir $restore_dir
}

# ask for 3G icon
ask_3g(){
	$DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Adiciona 3G?"
	if [ $? == 0 ]; then
		has_3g=true
	else
		has_3g=false
	fi
	export has_3g
}


# ask for webcam icon
ask_cam(){
	$DIALOG --question --ok-label=Sim --cancel-label=Nao --text="Suporte a Webcam?"
	if [ $? == 0 ]; then
		has_webcam=true
	else
		has_webcam=false
	fi
	export has_webcam
}


# "happy ending"
finish(){
	killall zenity 
	$DIALOG --info --text="Recuperacao terminou. Pressione ENTER para reiniciar"
	reboot
}

