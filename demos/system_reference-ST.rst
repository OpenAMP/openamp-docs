.. _demos-ST-work-label:

=============================================================
System Reference Samples and Demos on STM32MP157C/F-DK2 board
=============================================================

Based on a fork of the yocto [meta-st-stm32mp-oss](https://github.com/STMicroelectronics/meta-st-stm32mp-oss) environment, designed to update and test upstream code on STM32MP boards,

Prerequisite
------------

Some specifics package could be needed to build the ST images. For details refer to  

`STMPU wiki PC prerequisite <https://wiki.st.com/stm32mpu/wiki/PC_prerequisites>`_

Installation
------------

Create the structure of the project

.. code-block:: console

   mkdir stm32mp15-demo
   cd stm32mp15-demo
   mkdir stm32mp1_distrib_oss
   mkdir zephy_rpmsg_multi_services

At this step you should see following folder hierarchy:

.. code-block:: console

   stm32mp15-demo
       |___ stm32mp1_distrib_oss
       |___ zephy_rpmsg_multi_services

Generate the stm32mp15 image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install stm32mp1_distrib_oss kirkstone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From the stm32mp15-demo directory

.. code-block:: console

   cd stm32mp1_distrib_oss

   mkdir -p layers/meta-st
   git clone https://github.com/openembedded/openembedded-core.git layers/openembedded-core
   cd layers/openembedded-core
   git checkout -b WORKING origin/kirkstone
   cd -

   git clone https://github.com/openembedded/bitbake.git layers/openembedded-core/bitbake
   cd layers/openembedded-core/bitbake
   git checkout -b WORKING  origin/2.0
   cd -

   git clone https://github.com/openembedded/meta-openembedded.git layers/meta-openembedded
   cd layers/meta-openembedded
   git checkout -b WORKING origin/kirkstone
   cd -

   git clone https://github.com/arnopo/meta-st-stm32mp-oss.git layers/meta-st/meta-st-stm32mp-oss
   cd layers/meta-st/meta-st-stm32mp-oss
   git checkout -b WORKING origin/kirkstone
   cd -

Initialize the Open Embedded build environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The OpenEmbedded environment setup script must be run once in each new working terminal in which you use the BitBake or devtool tools (see later) from stm32mp15-demo/stm32mp1_distrib_oss directory

.. code-block:: console

   source ./layers/openembedded-core/oe-init-build-env build-stm32mp15-disco-oss

   bitbake-layers add-layer ../layers/meta-openembedded/meta-oe
   bitbake-layers add-layer ../layers/meta-openembedded/meta-perl
   bitbake-layers add-layer ../layers/meta-openembedded/meta-python
   bitbake-layers add-layer ../layers/meta-st/meta-st-stm32mp-oss

   echo "MACHINE = \"stm32mp15-disco-oss\"" >> conf/local.conf
   echo "DISTRO = \"nodistro\"" >> conf/local.conf
   echo "PACKAGE_CLASSES = \"package_deb\" " >> conf/local.conf

Build stm32mp1_distrib_oss image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From stm32mp15-demo/stm32mp1_distrib_oss/build-stm32mp15-disco-oss/ directory

::

   bitbake core-image-base

Note that

   - to build around 30 GB is needed
   - building the distribution can take more than 2 hours depending on performance of the PC.

Install stm32mp1_distrib_oss
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From 'stm32mp15-demo/stm32mp1_distrib_oss/build-stm32mp15-disco-oss/' directory,populate your microSD card inserted on your HOST PC using command

.. code-block:: console

   cd tmp-glibc/deploy/images/stm32mp15-disco-oss/
   # flash wic image on your sdcar. replace <device> by mmcblk<X> (X = 0,1..) or sd<Y> ( Y = b,c,d,..) depending on the connection 
   dd if=core-image-base-stm32mp15-disco-oss.wic of=/dev/<device> bs=8M conv=fdatasync


Generate the Zephyr rpmsg multi service example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prerequisite
^^^^^^^^^^^^

Please refer to the `Getting Started Guide
<https://docs.zephyrproject.org/latest/develop/getting_started/index.html>`_
zephyr documentation

Initialize the Zephyr environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   cd zephy_rpmsg_multi_services
   git clone https://github.com/OpenAMP/openamp-system-reference.git
   west init
   west update

Build the Zephyr image
^^^^^^^^^^^^^^^^^^^^^^

From the zephy_rpmsg_multi_services directory

.. code-block:: console

   west build -b stm32mp157c_dk2 openamp-system-reference/examples/zephyr/rpmsg_multi_services


Install the Zephyr binary on the sdcard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Zephyr sample binary is available in the sub-folder of build directory stm32mp15-demo/zephy_rpmsg_multi_services/build/zephyr/rpmsg_multi_services.elf. It needs to be installed on the "rootfs" partition of the sdcard

.. code-block:: console

   sudo cp build/zephyr/rpmsg_multi_services.elf <mountpoint>/rootfs/lib/firmware/

Don't forget to properly unmoumt the sdcard partitions.


Demos
-----

Start the demo environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

- power on the `stm32mp157C/F-dk2 board <https://wiki.st.com/stm32mpu/nsfr_img_auth.php/thumb/8/82/STM32MP157C-DK2_with_power_stlink_flasher_ethernet.png/600px-STM32MP157C-DK2_with_power_stlink_flasher_ethernet.png>`_, and wait login prompt on your serial terminal

.. code-block:: console

      stm32mp15-disco-oss login: root


There are 2 ways to start the coprocessor:

* During the runtime, by the Linux remoteproc framework

.. code-block:: console

   root@stm32mp15-disco-oss:~# cat /sys/class/remoteproc/remoteproc0/state
   offline
   root@stm32mp15-disco-oss:~# echo rpmsg_multi_services.elf > /sys/class/remoteproc/remoteproc0/firmware
   root@stm32mp15-disco-oss:~# echo start >/sys/class/remoteproc/remoteproc0/state
   root@stm32mp15-disco-oss:~# cat /sys/class/remoteproc/remoteproc0/state
   running

* In the boot stages, by the U-Boot remoteproc framework

    - Prerequisite
      Copy the firmware in the bootfs partition

    .. code-block:: console

      root@stm32mp15-disco-oss:~# cp /lib/firmware/rpmsg_multi_services.elf /boot/
      root@stm32mp15-disco-oss:~# sync

    - Boot the board and go in U-Boot console

    .. code-block:: console

      root@stm32mp15-disco-oss:~# reboot

    Enter in the U-boot console by interrupting the boot with  any  keyboard key.

    .. code-block:: console

      STM32MP>

    - Load and start the Coprocessor firmware:

    .. code-block:: console

      STM32MP> load mmc 0#bootfs ${kernel_addr_r} rpmsg_multi_services.elf
      816776 bytes read in 148 ms (5.3 MiB/s)
      STM32MP> rproc init
      STM32MP> rproc load 0 ${kernel_addr_r} ${filesize}
      Load Remote Processor 0 with data@addr=0xc2000000 816776 bytes: Success!
      STM32MP> rproc start 0
      STM32MP> run bootcmd

    To automatically load the firmware by U-Boot, refer to the
    `STMicorelectronics wiki <https://wiki.st.com/stm32mpu/wiki/How_to_start_the_coprocessor_from_the_bootloader>`_


    - Check that the remoteproc state is "detached"

    .. code-block:: console

      root@stm32mp15-disco-oss:~# cat /sys/class/remoteproc/remoteproc0/state
      detached

    - Attach the Linux remoteproc framework to the Zephyr

    .. code-block:: console

     root@stm32mp15-disco-oss:~# echo start >/sys/class/remoteproc/remoteproc0/state
     root@stm32mp15-disco-oss:~# cat /sys/class/remoteproc/remoteproc0/state
     attached

The communication with the Coprocessor is not initilaized, following traces on console
are observed:

.. code-block:: console

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

This informs that following rpmsg channels devices have been created:

   - a rpmsg-client-sample device
   - a rpmsg-tty device
   - a rpmsg-raw device


Run the multi RPMsg services demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 2

   ../openamp-system-reference/examples/zephyr/rpmsg_multi_services/README.rst
