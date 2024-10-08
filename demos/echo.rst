==================================
OpenAMP Echo Test Reference Sample
==================================

.. _echo-test-intro:

***************
Echo Test Intro
***************

The echo test reference sample, as the name suggests, demonstrates OpenAMP :ref:`Interprocessor Communications (IPC)<ipc-work-label>` components by providing an echo application on a remote which simply returns (echoes) packets as they are received at an :ref:`RPmsg endpoint <rpmsg-endpoint>` from the host controller. The host controller then verifies the returned packet for integrity.

..  image::  ../images/demos/echo-test-intro.svg

.. _echo-test-components:

********************
Echo Test Components
********************

There are two applications involved in this demonstration. The :ref:`remote application<echo-test-remote-app>` runs as an echo service, which returns packets it receives on an :ref:`RPmsg endpoint <rpmsg-endpoint>`. The :ref:`host application<echo-test-host-app>` is the test application sending packets to the echo service and expecting them back.

The underlying OpenAMP architectural components used by these applications are

* :ref:`Remoteproc<overview-remoteproc-work-label>`
* :ref:`Resource Table<overview-remoteproc-work-label>`
* :ref:`RPMsg<overview-rpmsg-work-label>`
* :ref:`Virtio<overview-rpmsg-work-label>`
* :ref:`Libmetal<overview-proxy-libmetal-label>`

This diagram shows the components involved in the demonstration.

..  image::  ../images/demos/echo-test-components.svg

.. _echo-test-remote-app:

RPmsg Echo Remote Application
=============================

The remote application, rpmsg-echo, is the core of the demonstration. It is a simple application serving a :ref:`RPmsg endpoint <rpmsg-endpoint>` running as the main task on the remote processor, once loaded and started using :ref:`Remoteproc<overview-remoteproc-work-label>`.


.. _echo-test-host-app:

Echo Test Host Application
==========================

The echo_test application forms the host controller side of the OpenAMP RPmsg **reference echo sample**. It repeatedly writes an increasing length payload of 0xA5's up to the maximum data size (packet size minus header) to the RPmsg endpoint. It then reads from the same endpoint and verifies the returned packet for correctness, reporting any corruption.

Echo Test Host Script
=====================

The host is also responsible for loading the firmware containing the :ref:`RPmsg Echo Remote Application <echo-test-remote-app>`_ and starting the remote processor using :ref:`Remoteproc<overview-remoteproc-work-label>`.

For host controllers, like Linux, a script can be used to pipe the firmware to the exposed remoteproc system, followed by the execution of the user space echo_test application.



*************************
Echo Test Implementations
*************************

.. _echo-test-linux-app:

RPmsg Echo Baremetal Implementation
===================================

The RPmsg Echo service application is available as a baremetal solution in the `open-amp Repository <https://github.com/OpenAMP/open-amp/blob/main/apps/examples/echo/rpmsg-echo.c>`_

It is a CMake application so can be built for any remote as long as the relevant :ref:`OS/HW abstraction layer<porting-guide-work-label>` components like libmetal are ported for that platform.

Echo Test Linux Implementation
==============================

The echo test Linux application is executed on the Linux host controller as a user space application.
The application is available in the `OpenAMP System Reference repository <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/linux/rpmsg-echo-test/echo_test.c>`_.

It is a Makefile application and can be built using the `Yocto rpmsg-echo-test recipe <https://github.com/OpenAMP/meta-openamp/blob/master/recipes-openamp/rpmsg-examples/rpmsg-echo-test_1.0.bb>`_

