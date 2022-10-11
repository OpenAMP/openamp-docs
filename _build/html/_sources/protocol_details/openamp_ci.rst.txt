================
Using OpenAMP CI
================

The OpenAMP CI solution is just in it's infancy at the moment and this doc is a work-in-progress. Please keep it up to date and don't keep historical information (that is what wiki history is for).

Running the Xilinx QEMU in Docker
*********************************

Get Docker on your machine
--------------------------

You will need docker on your machine. Google for howto setup on your machine.

Example for Ubuntu 18.04:

::

   $ sudo apt update; sudo apt install docker.io docker-doc; sudo adduser myuser docker

Then logout and log back in.

Your life will be easier if you are not behind a corporate firewall. If you are checkout: https://www.serverlab.ca/tutorials/containers/docker/how-to-set-the-proxy-for-docker-on-ubuntu/

run QEMU inside docker
----------------------

::

   $ docker run -it --name oaci edmooring/qemu:xilinx-qemu

This will:

   - pull the image from docker hub
   - start the container
   - attach your interactive terminal to the container
   - run a script that will launch the QEMU session
   - your terminal will become the simulated SOC's serial console
   - you will see the kernel boot messages
   - you will see the remoteproc driver for the zyncmp R5 core probe
   - you will get a login prompt
   - hit enter once to get a new login prompt (why?)
   - login with user of root and password also of root
   - you will have a minimal but pretty standard image based on PetaLinux 2019.02
   - you can install more software with: (if not behind a firewall)

::

   # dnf install tar less mc

Explore the system

::

   $ uname -a
   $ zcat /proc/config.gz

To run the rpmsg echo test do the following:

::

   $ echo image_echo_test >/sys/class/remoteproc/remoteproc0/firmware
   $ echo start >/sys/class/remoteproc/remoteproc0/state
   $ echo_test

Detach from the container with the key sequence ^P ^Q

look around the container
-------------------------

::

   $ docker ps
   $ docker exec -it oaci /bin/bash

You will now be root in the container. The container is a very minimal Debian 9 system but it does have dpkg and apt. If you are not behind a firewall you can:

::

   # apt update; apt install less tar procps mc

In any case you can checkout the important parts of the container

::

   # find /opt/arm
   /opt/arm
   /opt/arm/libexec
   /opt/arm/libexec/qemu-bridge-helper
   /opt/arm/bin
   /opt/arm/bin/qemu-system-aarch64
   /opt/arm/bin/qemu-pr-helper
   /opt/arm/bin/qemu-aarch64
   /opt/arm/bin/qemu-img
   /opt/arm/bin/ivshmem-client
   /opt/arm/bin/qemu-system-arm
   /opt/arm/bin/qemu-ga
   /opt/arm/bin/ivshmem-server
   /opt/arm/bin/qemu-microblazeel
   /opt/arm/bin/qemu-io
   /opt/arm/bin/qemu-system-microblazeel
   /opt/arm/bin/qemu-arm
   /opt/arm/bin/qemu-nbd
   /opt/arm/share
   /opt/arm/share/qemu
   /opt/arm/share/qemu/pxe-e1000.rom
   /opt/arm/share/qemu/spapr-rtas.bin
   /opt/arm/share/qemu/qemu_logo_no_text.svg
   /opt/arm/share/qemu/efi-vmxnet3.rom
   /opt/arm/share/qemu/pxe-ne2k_pci.rom
   /opt/arm/share/qemu/pxe-eepro100.rom
   /opt/arm/share/qemu/vgabios-qxl.bin
   /opt/arm/share/qemu/s390-netboot.img
   /opt/arm/share/qemu/efi-e1000.rom
   /opt/arm/share/qemu/vgabios-vmware.bin
   /opt/arm/share/qemu/slof.bin
   /opt/arm/share/qemu/u-boot.e500
   /opt/arm/share/qemu/s390-ccw.img
   /opt/arm/share/qemu/efi-pcnet.rom
   /opt/arm/share/qemu/QEMU,tcx.bin
   /opt/arm/share/qemu/vgabios.bin
   /opt/arm/share/qemu/pxe-pcnet.rom
   /opt/arm/share/qemu/openbios-sparc32
   /opt/arm/share/qemu/bios.bin
   /opt/arm/share/qemu/keymaps
   /opt/arm/share/qemu/keymaps/pt-br
   /opt/arm/share/qemu/keymaps/nl-be
   /opt/arm/share/qemu/keymaps/es
   ...
   # find /usr/local -type f
   /usr/local/bin/start-qemu
   # cat /usr/local/bin/start-qemu
   mkdir -p /tmp/qemu-tmp
   /opt/arm/bin/qemu-system-microblazeel -M microblaze-fdt -display none \
      -serial mon:stdio -serial /dev/null \
      -hw-dtb /var/lib/qemu/images/zynqmp-qemu-multiarch-pmu.dtb \
      -kernel /var/lib/qemu/images/pmu_rom_qemu_sha3.elf \
      -device loader,file=/var/lib/qemu/images/pmufw.elf \
      -machine-path /tmp/qemu-tmp \
      -device loader,addr=0xfd1a0074,data=0x1011003,data-len=4 -device loader,addr=0xfd1a007C,data=0x1010f03,data-len=4 &
   /opt/arm/bin/qemu-system-aarch64 -M arm-generic-fdt -serial mon:stdio -serial /dev/null -display none \
     -device loader,file=/var/lib/qemu/images/bl31.elf,cpu-num=0 \
     -device loader,file=/var/lib/qemu/images/Image,addr=0x00080000 \
     -device loader,file=/var/lib/qemu/images/openamp.dtb,addr=0x1407f000 \
     -device loader,file=/var/lib/qemu/images/linux-boot.elf \
     -gdb tcp::9002 \
     -dtb /var/lib/qemu/images/openamp.dtb \
     -net nic \
     -net nic \
     -net nic \
     -net nic,vlan=1 \
     -net user,vlan=1,tftp=/tftpboot \
     -hw-dtb /var/lib/qemu/images/zynqmp-qemu-multiarch-arm.dtb \
     -machine-path /tmp/qemu-tmp \
     -global xlnx,zynqmp-boot.cpu-num=0 \
     -global xlnx,zynqmp-boot.use-pmufw=true \
     -m 4G
   # find /var/lib/qemu
   /var/lib/qemu
   /var/lib/qemu/images
   /var/lib/qemu/images/system.dtb
   /var/lib/qemu/images/bl31.elf
   /var/lib/qemu/images/zynqmp-qemu-multiarch-pmu.dtb
   /var/lib/qemu/images/system.bit
   /var/lib/qemu/images/u-boot.elf
   /var/lib/qemu/images/bl31.bin
   /var/lib/qemu/images/pxelinux.cfg
   /var/lib/qemu/images/pxelinux.cfg/default
   /var/lib/qemu/images/linux-boot.elf
   /var/lib/qemu/images/boot.scr
   /var/lib/qemu/images/Image
   /var/lib/qemu/images/u-boot.bin
   /var/lib/qemu/images/zynqmp-qemu-multiarch-arm.dtb
   /var/lib/qemu/images/System.map.linux
   /var/lib/qemu/images/zynqmp-qemu-arm.dtb
   /var/lib/qemu/images/zynqmp_fsbl.elf
   /var/lib/qemu/images/openamp.dtb
   /var/lib/qemu/images/pmu_rom_qemu_sha3.elf
   /var/lib/qemu/images/pmufw.elf

reattach to qemu serial console
-------------------------------

::

   # echo I am still root in the container
   # exit
   $ echo I am now back to the host
   $ docker attach oaci
   # echo now I am in QEMU system
   ^P ^Q
   $ echo back at host prompt

kill and cleanup
----------------

In order to reuse the same name, we need to stop the container and remove it. You can use 'stop' instead of 'kill' for a graceful stop

::

   $ docker kill oaci || true
   $ docker rm oaci || true

Items for improvement
*********************

Priority Items
--------------

   - The SOC rootfs is an initramfs built into the kernel image, this is not convenient
      * load initramfs.cpio.gz as a separate file if the qemu loader can handle it
      * Else, make an sdcard image or an mtd image that qemu can handle
   - Need to be able to rebuild kernel image and inject it into docker
      * Should be pretty easy, config and tag and gcc version are visible in running image
      * use -v option in docker command line to get files from host into container
      * in qemu start up, look for Image from host and use it if present
   - Need to be able to rebuild R5 images
      * need info on how to rebuild
      * inject & use as with kernel image above
   - Need test scripts
      * Look for test scripts from host, use some defaults if not
      * SOC rootfs should run test scripts at startup
   - Should publish the dockerfile that builds this docker image

Nice to have items
------------------

   - The SOC rootfs runs dropbear but use of user mode networking at QEMU level leaves it inaccessible
      * This makes it hard to get files into or out of the system
      * Use bridge networking in QEMU
      * Inside Docker, forward SOC port 22 to host port 2222 and expose
   - A corporate firewall makes it harder to use
      * Can we push or inherit proxy info from host -> container and container -> SOC rootfs
   - Can we use 2nd serial port direct from R5?
      * screen or tmux could show both serial ports at the same time
      * could be an option if we don't want it by default
   - Can we run both R5s?
      * would be good to run MCU to MCU use cases
   - Document how to rebuild other items
      * PMU firmware, AT-F bl1, linux-loader, sw dtbs
      * QEMU
         + install path should be /opt/xilinx right??


