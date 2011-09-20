#!/bin/bash

if grep -q gubed /proc/cmdline; then
	set -x
	exec &> /tmp/debug-install.log
fi

source /usr/sbin/oem-lib.sh

# need some modules first
modprobe dm-mod &>/dev/null
#modprobe ext4 &>/dev/null
drvinst &> /dev/null

# main (void) :P
confirm_install
if grep -q partition /proc/cmdline; then
	create_part || error_msg
fi
#format_swap sda1 || error_msg
restore_parts_philco
killall zenity # oem ...
oem_version="philco"
export $oem_version
install_master_files
create_hd_restore
write_log
restore_bootloader_philco || error_msg
finish
