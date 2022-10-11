.. _demos-work-label:

==================================
System Reference Samples and Demos
==================================

Echo Test
---------

ST Echo Test Example
~~~~~~~~~~~~~~~~~~~~

Instruction to install the yocto environment, build and load an image, run the echo example is available here: https://github.com/arnopo/oe-manifest/blob/OpenAMP/README.md

For more information and help on the stm32mp15 platform and environment, please refer to `stm32mpu wiki <https://wiki.st.com/stm32mpu/wiki/Main_Page>`_.

Xilinx Echo Test Example
~~~~~~~~~~~~~~~~~~~~~~~~

`WIP document <https://drive.google.com/drive/u/0/folders/1CqerKYLfwtQu0cnDFa00wqwznCpBK5WO>`_ (Note Google doc access is currently restricted to working group members. To publish once it is sufficiently ready)

Multi RPMSG services demo
-------------------------
STM32MP157C/F-DK2 board
~~~~~~~~~~~~~~~~~~~~~~~

Based on

    - a fork of the yocto [meta-st-stm32mp-oss](https://github.com/STMicroelectronics/meta-st-stm32mp-oss) environment, designed to update and test upstream code on STM32MP boards,
    - a fork of the yocto [meta-zephyr](https://git.yoctoproject.org/meta-zephyr/).

Prerequisite
^^^^^^^^^^^^

TBC

Installation
^^^^^^^^^^^^

Create the structure of the project

::

   mkdir stm32mp15-demo
   cd stm32mp15-demo
   mkdir zephy_distrib
   mkdir stm32mp1_distrib_oss

At this step you should see following folder hierarchy:

::

   stm32mp15-demo
       |___ stm32mp1_distrib_oss
       |___ zephy_distrib

Generate the stm32mp15 image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install stm32mp1_distrib_oss dunfell
____________________________________

From the stm32mp15-demo directory

::

   cd stm32mp1_distrib_oss

   mkdir -p layers/meta-st
   git clone https://github.com/openembedded/openembedded-core.git layers/openembedded-core
   cd layers/openembedded-core
   git checkout -b WORKING origin/dunfell
   cd -

   git clone https://github.com/openembedded/bitbake.git layers/openembedded-core/bitbake
   cd layers/openembedded-core/bitbake
   git checkout -b WORKING  origin/1.46
   cd -

   git clone git://github.com/openembedded/meta-openembedded.git layers/meta-openembedded
   cd layers/meta-openembedded
   git checkout -b WORKING origin/dunfell
   cd -

   git clone https://github.com/arnopo/meta-st-stm32mp-oss.git layers/meta-st/meta-st-stm32mp-oss
   cd layers/meta-st/meta-st-stm32mp-oss
   git checkout -b WORKING origin/dunfell
   cd -

Initialize the Open Embedded build environment
______________________________________________

The OpenEmbedded environment setup script must be run once in each new working terminal in which you use the BitBake or devtool tools (see later) from stm32mp15-demo/stm32mp1_distrib_oss directory

::

   source ./layers/openembedded-core/oe-init-build-env build-stm32mp15-disco-oss

   bitbake-layers add-layer ../layers/meta-openembedded/meta-oe
   bitbake-layers add-layer ../layers/meta-openembedded/meta-perl
   bitbake-layers add-layer ../layers/meta-openembedded/meta-python
   bitbake-layers add-layer ../layers/meta-st/meta-st-stm32mp-oss

   echo "MACHINE = \"stm32mp15-disco-oss\"" >> conf/local.conf
   echo "DISTRO = \"nodistro\"" >> conf/local.conf
   echo "PACKAGE_CLASSES = \"package_deb\" " >> conf/local.conf

Build stm32mp1_distrib_oss image
________________________________

From stm32mp15-demo/stm32mp1_distrib_oss/build-stm32mp15-disco-oss/ directory

::

   bitbake core-image-base

Note that

   - to build around 30 GB is needed
   - building the distribution can take more than 2 hours depending on performance of the PC.

Flash stm32mp1_distrib_oss
__________________________

From 'stm32mp15-demo/stm32mp1_distrib_oss/build-stm32mp15-disco-oss/' directory,populate your microSD card inserted on your HOST PC using command

::

   cd tmp-glibc/deploy/images/stm32mp15-disco-oss/
   # flash wic image on your sdcar. replace <device> by mmcblk<X> (X = 0,1..) or sd<Y> ( Y = b,c,d,..) depending on the connection 
   dd if=core-image-base-stm32mp15-disco-oss.wic of=/dev/<device> bs=8M conv=fdatasync

Generate the Zephyr firmware image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install meta-zephyr Honister version
____________________________________

From stm32mp15-demo directory

::

   cd zephy_distrib

   git clone https://github.com/openembedded/openembedded-core.git layers/openembedded-core
   cd layers/openembedded-core
   git checkout -b WORKING origin/honister
   cd -

   git clone https://github.com/openembedded/bitbake.git layers/openembedded-core/bitbake
   cd layers/openembedded-core/bitbake
   git checkout -b WORKING  origin/1.46
   cd -

   git clone git://github.com/openembedded/meta-openembedded.git layers/meta-openembedded
   cd layers/meta-openembedded
   git checkout -b WORKING origin/honister
   cd -

   git clone https://github.com/arnopo/meta-zephyr.git layers/meta-zephyr
   cd layers/meta-zephyr
   git checkout -b WORKING origin/OpenAMP_demo
   cd -

Initialize the OpenEmbedded build environment
_____________________________________________

The OpenEmbedded environment setup script must be run once in each new working terminal in which you use the BitBake or devtool tools (see later) from the stm32mp15-demo/zephy_distrib directory

::

   MACHINE="stm32mp157c-dk2" DISTRO="zephyr" source layers/openembedded-core/oe-init-build-env    build-zephyr
   bitbake-layers add-layer ../layers/meta-openembedded/meta-oe/
   bitbake-layers add-layer ../layers/meta-openembedded/meta-python/
   bitbake-layers add-layer ../layers/meta-zephyr/

Build the Zephyr image
______________________

For instance to build the zephyr-openamp-rsc-table example which answers to the Linux rpmsg sample client example 

From the stm32mp15-demo/zephy_distrib/build-zephyr directory

::

   MACHINE="stm32mp157c-dk2" DISTRO="zephyr" bitbake zephyr-openamp-rsc-table

Note that

   - to build around 30 GB is needed,
   - building the distribution can take 1 or 2 hours depending on performance of the PC.

Install the Zephyr binary on the sdcard
_______________________________________

The Zephyr sample binary is available in the sub-folder of build directory stm32mp15-demo/zephy_distrib/build-zephyr/tmp-newlib/deploy/images/stm32mp157c-dk2/. It needs to be installed on the "rootfs" partition of the sdcard

::

   sudo cp tmp-newlib/deploy/images/stm32mp157c-dk2/zephyr-openamp-rsc-table.elf <mount    point>/rootfs/lib/firmware/

Don't forget to properly unmoumt the sdcard partitions.

Demos
^^^^^

Start the demo environment
__________________________

- power on the `stm32mp157C/F-dk2 board <https://wiki.st.com/stm32mpu/nsfr_img_auth.php/thumb/8/82/STM32MP157C-DK2_with_power_stlink_flasher_ethernet.png/600px-STM32MP157C-DK2_with_power_stlink_flasher_ethernet.png>`_, and wait login prompt on your serial terminal

::

      stm32mp15-disco-oss login: root

- Start the Cortex-M4 firmware

::

   echo zephyr-openamp-rsc-table.elf > /sys/class/remoteproc/remoteproc0/firmware 
   echo start >/sys/class/remoteproc/remoteproc0/state 

You should observe following traces on console

::

   root@stm32mp15-disco-oss:~#
   [   54.495343] virtio_rpmsg_bus virtio0: rpmsg host is online
   [   54.500044] virtio_rpmsg_bus virtio0: creating channel rpmsg-client-sample addr 0x400
   [   54.507923] virtio_rpmsg_bus virtio0: creating channel rpmsg-tty addr 0x401
   [   54.514795] virtio_rpmsg_bus virtio0: creating channel rpmsg-raw addr 0x402
   [   54.548954] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: new channel: 0x402 -> 0x400!
   [   54.557337] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 1 (src:    0x400)
   [   54.565532] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 2 (src:    0x400)
   [   54.581090] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 3 (src:    0x400)
   [   54.588699] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 4 (src:    0x400)
   [   54.599424] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 5 (src:    0x400)
   ...

This inform that following rpmsg channels devices have been created

   - a rpmsg-client-sample device
   - a rpmsg-tty device
   - a rpmsg-raw device

Demo 1: rpmsg-client-sample device
__________________________________

- Principle

This demo is automatically run when the co-processor firmware is started. It confirms that the rpmsg and virtio protocols are working properly.

   * The Zephyr requests the creation of the rpmsg-client-sample channel to the Linux rpmsg framework using the "name service announcement" rpmsg.
   * On message reception the Linux rpmsg bus creates an associated device and probes the `rpmsg-client-sample driver <https://elixir.bootlin.com/linux/latest/source/samples/rpmsg/rpmsg_client_sample.c>`_
   * The Linux rpmsg-client-sample driver sent 100 messages to the remote processor, which answers to each message
   * After answering to each rpmsgs the Zephyr destroys the channel

- Associated traces

::

   [   54.548954] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: new channel: 0x402 -> 0x400!
   [   54.557337] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 1 (src: 0x400)
   [   54.565532] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 2 (src: 0x400)
   ...
   [   55.436401] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 99 (src: 0x400)
   [   55.445343] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 100 (src: 0x400)
   [   55.454280] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: goodbye!
   [   55.461424] virtio_rpmsg_bus virtio0: destroying channel rpmsg-client-sample addr 0x400
   [   55.469707] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: rpmsg sample client driver is removed

Demo 2: rpmsg-tty device
________________________

- Principle

This channel allows to create a /dev/ttyRPMSGx for terminal based communication with Zephyr. 

- Demo

1- Check presence of the /dev/ttyRPMSG0

By default the Zephyr has created a rpmsg-tty channel 

::

   [   54.507923] virtio_rpmsg_bus virtio0: creating channel rpmsg-tty addr 0x401

::

   root@stm32mp15-disco-oss:~# ls /dev/ttyRPMSG*
   /dev/ttyRPMSG0

2- Send and receive messages on /dev/ttyRPMSG0

The zephyr is programmed to resent received messages with a prefixed "TTY 0: ", 0 is the instance of the tty link

::

   root@stm32mp15-disco-oss:~# cat /dev/ttyRPMSG0 &
   root@stm32mp15-disco-oss:~# echo " hello Zephyr" >/dev/ttyRPMSG0
   TTY 0:  hello Zephyr
   root@stm32mp15-disco-oss:~# echo " goodbye Zephyr" >/dev/ttyRPMSG0
   TTY 0:  goodbye Zephyr

Demo 3: dynamic creation/release of a rpmsg-tty device
______________________________________________________

- Principle

This demo is based on the `rpmsg_char restructuring series <https://lkml.org/lkml/2022/1/24/293>`_ not yet upstreamed. This series de-correlates the /dev/rpmsg_ctrl from the rpmsg_char device and then introduces 2 new rpmsg IOCtrls

   * RPMSG_CREATE_DEV_IOCTL : to create a local rpmsg device and to send a name service creation announcement to the remote processor
   * RPMSG_RELEASE_DEV_IOCTL: release the local rpmsg device and to send a name service destroy announcement to the remote processor

- Demo 

1- Prerequisite

* Due to a limitation in the rpmsg protocol, the zephyr does not know the existence of the /dev/ttyRPMG0 until the Linux sends it a first message. Creating a new channel before this first one is well establish leads to bad endpoints association. To avoid this just send a message on /dev/ttyRPMSG0

::

   root@stm32mp15-disco-oss:~# cat /dev/ttyRPMSG0 &
   root@stm32mp15-disco-oss:~# echo " hello Zephyr" >/dev/ttyRPMSG0
   TTY 0:  hello Zephyr

* Download rpmsgexport tools relying on the /dev/rpmsg_ctrl, and compile it in an arm environment unsing make instruction and install it on target

* optional enable rpmsg bus trace to observe rp messages in kernel trace

::

   echo -n 'file virtio_rpmsg_bus.c +p' > /sys/kernel/debug/dynamic_debug/control


2- create a new TTY channel Create a rpmsg-tty channel with local address set to 257 and undefined remote address -1.

::

   root@stm32mp15-disco-oss:~# ./rpmsgexportdev /dev/rpmsg_ctrl0 rpmsg-tty 257 -1

The /dev/ttyRPMSG1 is created

::

   root@stm32mp15-disco-oss:~# ls /dev/ttyRPMSG*
   /dev/ttyRPMSG0  /dev/ttyRPMSG1

A name service announcement has been sent to Zephyr, which has created a local endpoint (@ 0x400), and sent a "bound" message to the /dev/ttyRPMG1 (@ 257)

::

   root@stm32mp15-disco-oss:~# dmesg
   [  115.757439] rpmsg_tty virtio0.rpmsg-tty.257.-1: TX From 0x101, To 0x35, Len 40, Flags 0, Reserved 0
   [  115.757497] rpmsg_virtio TX: 01 01 00 00 35 00 00 00 00 00 00 00 28 00 00 00  ....5.......(...
   [  115.757514] rpmsg_virtio TX: 72 70 6d 73 67 2d 74 74 79 00 00 00 00 00 00 00  rpmsg-tty.......
   [  115.757528] rpmsg_virtio TX: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
   [  115.757540] rpmsg_virtio TX: 01 01 00 00 00 00 00 00                          ........
   [  115.757568] remoteproc remoteproc0: kicking vq index: 1
   [  115.757590] stm32-ipcc 4c001000.mailbox: stm32_ipcc_send_data: chan:1
   [  115.757850] stm32-ipcc 4c001000.mailbox: stm32_ipcc_tx_irq: chan:1 tx
   [  115.757906] stm32-ipcc 4c001000.mailbox: stm32_ipcc_rx_irq: chan:0 rx
   [  115.757969] remoteproc remoteproc0: vq index 0 is interrupted
   [  115.757994] virtio_rpmsg_bus virtio0: From: 0x400, To: 0x101, Len: 6, Flags: 0, Reserved: 0
   [  115.758022] rpmsg_virtio RX: 00 04 00 00 01 01 00 00 00 00 00 00 06 00 00 00  ................
   [  115.758035] rpmsg_virtio RX: 62 6f 75 6e 64 00                                bound.
   [  115.758077] virtio_rpmsg_bus virtio0: Received 1 messages

2- Play with /dev/ttyRPMSG0 and /dev/ttyRPMSG1

::

   root@stm32mp15-disco-oss:~# cat /dev/ttyRPMSG0 &
   root@stm32mp15-disco-oss:~# cat /dev/ttyRPMSG0 &
   root@stm32mp15-disco-oss:~# echo hello dev0 >/dev/ttyRPMSG0
   TTY 0: hello dev0
   root@stm32mp15-disco-oss:~# echo hello dev1 >/dev/ttyRPMSG1
   TTY 1: hello dev1

3- Destroy RPMSG TTY devices

- Destroy the /dev/ttyRPMSG0

::

   root@stm32mp15-disco-oss:~# ./rpmsgexportdev /dev/rpmsg_ctrl0 -d rpmsg-tty 257 -1

- Destroy the /dev/ttyRPMSG1

Get the source address

::

   root@stm32mp15-disco-oss:~# cat /sys/bus/rpmsg/devices/virtio0.rpmsg-tty.-1.*/src
   0x402

- Destroy the /dev/ttyRPMSG1 specifying the address 1026 (0x402)

::

   root@stm32mp15-disco-oss:~# ./rpmsgexportdev /dev/rpmsg_ctrl0 -d rpmsg-tty 1026 -1

The /dev/ttyRPMGx devices no more exists 

Demo 4: rpmsg-char device
_________________________


- Principle

This channel allows to create a /dev/rpmsgX for character device based communication with Zephyr. 

- Demo

1- Prerequisite

   * Download `rpmsgexport tools <https://github.com/arnopo/rpmsgexport>`_ relying on the /dev/rpmsg_ctrl, an compile it in an arm environment unsing make instruction and install it on target
   * optional enable rpmsg bus trace to observe rp messages in kernel trace:

::

   echo -n 'file virtio_rpmsg_bus.c +p' > /sys/kernel/debug/dynamic_debug/control

2- Check presence of the /dev/rpmsg0

By default the Zephyr has created a rpmsg-raw channel 

::

   [   54.514795] virtio_rpmsg_bus virtio0: creating channel rpmsg-raw addr 0x402

3- Check device exists

::

   root@stm32mp15-disco-oss:~# ls /dev/rpmsg?
   /dev/rpmsg0

4- Send and receive messages on /dev/rpmsg0

The zephyr is programmed to resent received message with a prefixed "from ept 0x0402: ", 0x0402 is the zephyr endpoint address

::

   root@stm32mp15-disco-oss:~# ./rpmsgping /dev/rpmsg0
   message for /dev/rpmsg0: "from ept 0x0402: ping /dev/rpmsg0"

Demo 5: Multi endpoints demo using rpmsg-ctrl device
____________________________________________________

- Principle

Use the rpmsg_ctrl RPMSG_CREATE_EPT_IOCTL IoCtrl to instantiate endpoints on Linux side. Theses endpoints will not be associated to a channel but will communicate with a predefined remote proc endpoint. For each endpoint created, a /dev/rpmsg sysfs interface will be created On Zephyr side, an endpoint with a prefixed address 0x1 has been created. When it receives a message it re-sends a the message to the Linux sender endpoint, prefixed by "from ept 0x0001:" 

- Demo

1- Prerequisite

   * Download `rpmsgexport tools <https://github.com/arnopo/rpmsgexport>`_ relying on the /dev/rpmsg_ctrl, an compile it in an arm environment unsing make instruction and install it on target
   * optional enable rpmsg bus trace to observe rp messages in kernel trace

::

   echo -n 'file virtio_rpmsg_bus.c +p' > /sys/kernel/debug/dynamic_debug/control

2- Check presence of the /dev/rpmsg0

By default the Zephyr has created a rpmsg-raw channel 

::

   [   54.514795] virtio_rpmsg_bus virtio0: creating channel rpmsg-raw addr 0x402

3- Check device exists

::

   root@stm32mp15-disco-oss:~# ls /dev/rpmsg*
   /dev/rpmsg0       /dev/rpmsg_ctrl0

4- Create 3 new endpoints

::

   root@stm32mp15-disco-oss:~# ./rpmsgexport /dev/rpmsg_ctrl0 my_endpoint1 100 1
   root@stm32mp15-disco-oss:~# ./rpmsgexport /dev/rpmsg_ctrl0 my_endpoint2 101 1
   root@stm32mp15-disco-oss:~# ./rpmsgexport /dev/rpmsg_ctrl0 my_endpoint2 103 1
   root@stm32mp15-disco-oss:~# ls /dev/rpmsg?
   /dev/rpmsg0  /dev/rpmsg1  /dev/rpmsg2  /dev/rpmsg3

5- Test them

::

   root@stm32mp15-disco-oss:~# ./rpmsgping  /dev/rpmsg0
   message for /dev/rpmsg0: "from ept 0x0402: ping /dev/rpmsg0"
   root@stm32mp15-disco-oss:~# ./rpmsgping  /dev/rpmsg1
   message for /dev/rpmsg1: "from ept 0x0001: ping /dev/rpmsg1"
   root@stm32mp15-disco-oss:~# ./rpmsgping  /dev/rpmsg2
   message for /dev/rpmsg2: "from ept 0x0001: ping /dev/rpmsg2"
   root@stm32mp15-disco-oss:~# ./rpmsgping  /dev/rpmsg3
   message for /dev/rpmsg3: "from ept 0x0001: ping /dev/rpmsg3"

6- Destroy them

::

   root@stm32mp15-disco-oss:~# ./rpmsgdestroyept /dev/rpmsg1
   root@stm32mp15-disco-oss:~# ./rpmsgdestroyept /dev/rpmsg2
   root@stm32mp15-disco-oss:~# ./rpmsgdestroyept /dev/rpmsg3
   root@stm32mp15-disco-oss:~# ls /dev/rpmsg?
   /dev/rpmsg0
