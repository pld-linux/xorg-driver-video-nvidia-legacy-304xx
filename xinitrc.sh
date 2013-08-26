#!/bin/sh

if [ -r "${HOME}/.nvidia-settings-rc" ]; then
	/usr/bin/nvidia-settings -l > /dev/null 2>&1
fi
