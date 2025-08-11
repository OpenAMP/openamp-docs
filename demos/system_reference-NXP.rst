

.. _reference_board_NXP:

====================
NXP Reference Boards
====================

A number of the `OpenAMP project examples
<https://github.com/OpenAMP/openamp-system-reference/tree/main/examples>`_
can be executed on NXP Reference boards.

Board setup
------------

The `i.MX 8M Plus Evaluation Kit Quick Start Guide (IMX8MPLUSQSG)
<https://www.nxp.com/docs/en/quick-reference-guide/8MPLUSEVKQSG.pdf>`_
contains basic information on the board and how to
set it up.
In `AN13970 Running Zephyr RTOS on Cadence Tensilica HiFi 4 DSP
<https://www.nxp.com/docs/en/application-note/AN13970.pdf>`_
application note provides instructions on how to launch the samples on
the HiFi4 DSP.

Generate the Zephyr rpmsg multi service example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialize the Zephyr environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Refer to :ref:`zephyr example readme<openamp-system-reference/examples/zephyr/README:initialization>` article.


Build the Zephyr image
^^^^^^^^^^^^^^^^^^^^^^

From the openamp-system-reference directory

.. code-block:: console

   west build -p -b imx8mp_evk//adsp -s examples/zephyr/rpmsg_multi_services/

For details refer to
:ref:`rpmsg_multi_services readme <openAMP_rsc_table_sample>` article.

Install the Zephyr binary on the sdcard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Zephyr sample binary is available in the sub-folder of build directory
openamp-system-reference/build/zephyr/rpmsg_multi_services.elf.
It needs to be installed on the "rootfs" partition of the sdcard

.. code-block:: console

   sudo cp build/zephyr/rpmsg_multi_services.elf <mountpoint>/rootfs/lib/firmware/

Don't forget to properly unmount the sdcard partitions.

.. code-block:: console

   sudo eject /dev/<device>

Demos
-----

Start the demo environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

Power on the i.MX8M Plus EVK, and wait login prompt on your serial terminal

.. code-block:: console

      imx8mpevk login: root
      root@imx8mpevk:~#


Start the coprocessor using Linux remoteproc framework

   .. code-block:: console

      root@imx8mpevk:~# cat /sys/class/remoteproc/remoteproc0/state
      offline
      root@imx8mpevk:~# echo rpmsg_multi_services.elf > /sys/class/remoteproc/remoteproc0/firmware
      root@imx8mpevk:~# echo start >/sys/class/remoteproc/remoteproc0/state
      root@imx8mpevk:~# cat /sys/class/remoteproc/remoteproc0/state
      running

The communication with the coprocessor is not initialized, following traces on console
are observed:

.. code-block:: console

   root@imx8mpevk:~#
   [  199.756694] virtio_rpmsg_bus virtio0: rpmsg host is online
   [  199.756756] rproc-virtio rproc-virtio.2.auto: registered virtio0 (type 7)
   [  199.756764] remoteproc remoteproc0: remote processor imx-dsp-rproc is now up
   [  199.757099] virtio_rpmsg_bus virtio0: creating channel rpmsg-client-sample addr 0x400
   [  199.757259] virtio_rpmsg_bus virtio0: creating channel rpmsg-tty addr 0x401
   [  199.757425] virtio_rpmsg_bus virtio0: creating channel rpmsg-raw addr 0x402
   [  199.817974] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: new channel: 0x402 -> 0x400!
   [  199.818049] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 1 (src: 0x400)
   [  199.818089] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 2 (src: 0x400)
   [  199.818290] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 3 (src: 0x400)
   [  199.818325] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 4 (src: 0x400)
   [  199.818354] rpmsg_client_sample virtio0.rpmsg-client-sample.-1.1024: incoming msg 5 (src: 0x400)
   ...

This informs that following rpmsg channels devices have been created:

   - a rpmsg-client-sample device
   - a rpmsg-tty device
   - a rpmsg-raw device


Run the multi RPMsg services demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Refer to
:ref:`rpmsg_multi_services <openAMP_rsc_table_sample>` article.
