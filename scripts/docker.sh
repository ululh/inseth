#!/bin/bash
if [ $UID -ne 0 ]
then
	echo "Not root, exiting..."
	exit 1
fi

# start daemon if not running
if ! ps -ef | grep dockerd | grep -v grep >/dev/null
then
	echo "Starting dockerd"
	nohup dockerd > /dev/null 2>&1 &
	sleep 5
fi

# create volume if not existing
VOLUME=inseth
if ! docker volume list | grep inseth >/dev/null
then
	echo "Creating volume $VOLUME"
	docker volume create $VOLUME
fi

# build and run containers

build () {

	# SUDO_USER OK after sudo su but not sudo su -, where is RUID ??
	cd $(getent passwd $SUDO_USER | cut -d: -f6)/inseth/repo
	echo "Building $1 ...."
	docker build -f $1/Dockerfile -t ${1}_img .
}

run () {

	CONTAINER_ID=$(docker ps -a |grep $1 | awk '{print $1}')
	if [ ! -z $CONTAINER_ID ]
	then
		docker rm --force $CONTAINER_ID
	fi
	echo "Starting $1...."
	docker run -d -v inseth:/data --name $1 ${1}_img
}

build ethereum_collector
run ethereum_collector

# troubleshoot
# docker run -it --entrypoint bash eth_client_img
# docker image history --no-trunc eth_client_img > image_history
