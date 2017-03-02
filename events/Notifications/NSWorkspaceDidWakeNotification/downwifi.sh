#!/bin/sh

#ifconfig en4 2>/dev/null|grep -q inet 
sleep 5
ifconfig -a 2>/dev/null |grep -i inet -A2|grep -iq 1000base

if [ $? -eq 0 ]
then
	networksetup -setairportpower en0 off
else
	#networksetup -setairportpower en0 on
	/usr/bin/true
fi	
