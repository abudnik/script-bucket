#!/bin/bash

searchdir=$1
libname=$2

if [ "$#" -ne 2 ]; then
	echo -e "2 args required\nexample: libusage.sh /usr/bin boost"
	exit
fi

if [ ! -d $searchdir ]; then
	echo "Unknown path: $searchdir"
	exit
fi

declare libs
for file in $( find $searchdir -name "*" -type f 2>/dev/null )
do
	libs=$( ldd $file 2>/dev/null | grep $libname )
	if [ -n "$libs" ]; then
		echo -e "$file \n $libs"
		echo "================"
	fi
done

echo -e "\ndone"
