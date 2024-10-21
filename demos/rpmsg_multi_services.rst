
=================================
OpenAMP RPMsg Multi Services Demo
=================================

.. _rpmsg-multi-services-intro:

**************************
RPMsg Multi Services Intro
**************************

The RPMsg Multi Services reference sample, as the name suggests, demonstrates OpenAMP :ref:`Interprocessor Communications (IPC)<ipc-work-label>` components by providing multiple services on a single remote.

Three channel types are demonstrated.

* Direct RPMsg Channel
* Raw `character device <https://linux-kernel-labs.github.io/refs/heads/master/labs/device_drivers.html>`_ channel
* `tty Device <https://www.kernel.org/doc/html/latest/driver-api/tty/index.html>`_ channels

The host side is implemented in Linux as client drivers being to the remote services.

The direct RPMsg client is a `dedicated Linux sample driver <https://github.com/torvalds/linux/blob/master/samples/rpmsg/rpmsg_client_sample.c>`_ specifically for this demonstration.

The raw character 'client' is the `RPMsg character driver <https://github.com/torvalds/linux/blob/master/drivers/rpmsg/rpmsg_char.c>`_ provided in the Linux source, and becomes available once the driver module is loaded at /dev/rpmsg? device file. To exercise the demonstration, characters can be sent to the device file using the `rpmsg-utils/rpmsg_ping <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/linux/rpmsg-utils/rpmsg_ping.c>`_ command. The RPMsg device id name is "rpmsg-raw".

The tty 'client' is the `PRMsg tty driver <https://github.com/torvalds/linux/blob/master/drivers/tty/rpmsg_tty.c>`_ provided in the Linux source, and becomes available once the driver module is loaded at /dev/ttyRPMSG?. To exercise the demonstration, characters can be sent to the device file using echo or cat Linux command.

..  image::  ../images/demos/rpmsg-multi-services-intro.svg

.. _rpmsg-multi-services-components:

The linux rpmsg_client_sample driver begins sending 'hello world!' messages on a rpmsg_driver probe, and repeats a predefined time for each response from the remote. The response from the remote application is to return the same packet they received at the :ref:`RPmsg endpoint <rpmsg-endpoint>` from the host controller.

Build and run instructions for reference board.
https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/zephyr/rpmsg_multi_services

TODO: more on how resource table is used