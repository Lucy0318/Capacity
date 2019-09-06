#!/bin/bash

MAX=1000
a=1
b=2
for((i=1;i<=MAX;i++))
do
		if [ "$b" -ge "254" ]; then
			let a++
		fi
        ifconfig ens160:$i 172.20.$a.$b/16
		ssh -b ens160:$i -X sonicwall@10.7.13.53
		let b++
done 