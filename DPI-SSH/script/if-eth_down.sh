#!/bin/bash

#Max=1000

for((i=1;i<=1000;i++))
do
	ifconfig ens160:$i down
done 
