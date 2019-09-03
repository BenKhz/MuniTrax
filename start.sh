#!/usr/bin/bash

rm /tmp/.X0-lock &>/dev/null || true

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
echo "Starting X in 2 seconds"
sleep 2
startx
export DISPLAY=:0

while :
do
	echo "startx failed, so we will just wait here while you debug!"
	sleep 15

done
