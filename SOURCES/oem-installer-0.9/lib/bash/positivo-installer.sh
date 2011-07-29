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
ask_home
create_part || error_msg
format_swap sda1 || error_msg
restore_parts
killall zenity # oem ...
install_custom_packages
install_extras /tmp/media/i586/custom/extras
disable_resize
if !grep -q from_disk /proc/cmdline; then
	gen_iso_install
	create_hd_restore
fi
write_log
restore_bootloader || error_msg
finish
