#!/usr/bin/env bash

set -e

if [ ! -d anaconda ] ; then
	echo "$0: Installing anaconda..."
	installer=Miniconda3-py38_4.8.3-Linux-x86_64.sh
	wget --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 20 https://repo.anaconda.com/miniconda/$installer
	#wget https://repo.anaconda.com/miniconda/$installer
	bash $installer -b -p anaconda/
	echo "Done"
fi

git clone https://github.com/NVIDIA/NeMo
(
  cd NeMo
  ./reinstall.sh
)
