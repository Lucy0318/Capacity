#!/bin/bash

Max=3
a=1
b=2
ReIP=10.7.13.53
password=sonicwall
time=30
for((i=1;i<=$Max;i++))
do
	if [ "$b" -gt "253" ];then
	let a++
	b=1
	fi 
	#ifconfig ens160:$i 172.20.$a.$b netmask 255.255.0.0
	#rm /etc/ssh/script/dpi*
	echo "#!/usr/bin/expect" >>/etc/ssh/dpi-ssh_$i.sh
	echo "#!/bin/bash" >>/etc/ssh/dpi-ssh_$i.sh
	#echo "/usr/bin/expect <<-EOF" >>/etc/ssh/dpi-ssh_$i.sh
	echo "spawn sshpass $password ssh -b 172.20.$a.$b -X sonicwall@$ReIP">>/etc/ssh/dpi-ssh_$i.sh
	#echo "expect {">>/etc/ssh/dpi-ssh_$i.sh
	#echo "\"*yes/no\" {send "yes\n";exp_continue;}">>/etc/ssh/dpi-ssh_$i.sh
	#echo "expect \"*password:\" ">>/etc/ssh/dpi-ssh_$i.sh
	#echo "send \"$password\r\"" >>/etc/ssh/dpi-ssh_$i.sh
	echo "expect \"*#\" ">>/etc/ssh/dpi-ssh_$i.sh
	echo "sleep $time" >>/etc/ssh/dpi-ssh_$i.sh
	echo "send \"exit\r\"" >>/etc/ssh/dpi-ssh_$i.sh
	echo "interact" >>/etc/ssh/dpi-ssh_$i.sh
	echo "exit" >>/etc/ssh/dpi-ssh_$i.sh
	echo "exit" >>/etc/ssh/dpi-ssh_$i.sh
	#echo "eof{exit 0;}">>/etc/ssh/dpi-ssh_$i.sh
	#echo "}">>/etc/ssh/dpi-ssh_$i.sh
	#echo "EOF">>/etc/ssh/dpi-ssh_$i.sh
	chmod 777 /etc/ssh/*
	ifconfig ens160:$i 172.20.$a.$b netmask 255.255.0.0
	gnome-terminal -x bash -c "./dpi-ssh_$i.sh"
	let b++
done
