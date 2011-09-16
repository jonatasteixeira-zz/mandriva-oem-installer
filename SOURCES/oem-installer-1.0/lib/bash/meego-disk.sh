#!/bin/bash

if grep -q gubed /proc/cmdline; then
	set -x
	exec &> /tmp/debug-install.log
fi

source /usr/sbin/oem-lib.sh

# need some modules first
modprobe dm-mod &>/dev/null
drvinst &> /dev/null

# main (void) :P
if ! grep -q force_no_root_pass /proc/cmdline; then
	        check_password
fi
confirm_install
ask_home
format_swap sda1 || error_msg
restore_parts
killall zenity # oem ...
install_custom_packages
install_extras /tmp/loop/i586/custom/extras
disable_resize || error_msg
finish
