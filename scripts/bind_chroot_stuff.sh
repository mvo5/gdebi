#!/bin/bash
sudo mount -t none -o bind /proc edgy/proc/
sudo mount -t none -o bind /tmp/ edgy/tmp/
sudo mount -t none -o bind /dev/ edgy/dev/
sudo mount -t none -o bind gdebi-kde/ edgy/mnt/
sudo mount -t devpts -orw,gid=5,mode=620 devpts edgy/dev/pts/