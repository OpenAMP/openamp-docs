================
Project Overview
================

*************
OpenAMP Intro
*************

`Asymmetric Multiprocessing (AMP) <https://en.wikipedia.org/wiki/Asymmetric_multiprocessing>`_ involves the management, control and communication of multiple computer systems, where processors have independent tasks and are often in a `heteregenous <https://en.wikipedia.org/wiki/Heterogeneous_computing>`_ embedded environment where there are different types of processors. This is in contrast to `Symmetric Multiprocessing (SMP) <https://en.wikipedia.org/wiki/Symmetric_multiprocessing>`_ which involves central control and load sharing using identical processor cores and is common place in servers and desktop computers.

The **OpenAMP** project is a community effort that is standardizing and implementing how these multiple embedded systems interact with each other in an AMP environment. It provides conventions and standards as well as an open source implementation to facilitate AMP development for embedded systems.

The vision is that regardless of the operating environment/operating system, it should be possible to use identical interfaces to interact with other operating environments in the same system.

Furthermore, these operating environments can interoperate over a standardized protocol, making it possible to mix and match any two or more operating systems in the same device.

Read more about Asymmetric Multiprocessing :ref:`here<asymmetric-multiprocessing-work-label>`.

********************
OpenAMP Fundamentals
********************

There are some AMP fundamentals which influence the OpenAMP Architecture choices.

* **Topology**: Different runtime systems need to coexist and collaborate as `Asymmetric Multiprocessing <https://en.wikipedia.org/wiki/Asymmetric_multiprocessing>`_ sets no restrictions on how systems can or should be utilized.
* **Resource Assignment**: Resources need to be assigned and shared into **run time domains**
* **Runtime Control**: Remote application/firmware loading, starting and stopping is required to manage the system.
* **IPC**: `Inter Processor Communications <https://en.wikipedia.org/wiki/Inter-process_communication>`_ needs to be established to enable communication and control.
* **Resource Isolation**: AMP systems can be supervised (using a hypervisor) or unsupervised.

Topology
========

The OpenAMP framework assumes a master-slave system architecture, but otherwise the **topology** of the different runtime systems may be star, chain or a combination.

.. image:: ../images/topo_types.jpg

A master will control one or more slaves each on a remote processor (star), and any remote processor could also act as a master to control another slave on a different remote processor (chain).

To exemplify the following sections use diagrams detailing a star topology with a single Linux master and dual slaves, with one remote running an RTOS and the other a bare metal image.

.. raw:: html
    :file: ../images/fundamentals/master-2-slave.svg


Resource Assignment
===================

This diagram details the Resource Assignment using a different color for each **runtime domain**.

.. raw:: html
    :file: ../images/fundamentals/resource-assignment.svg

The yellow colored boxes are the Linux **runtime domain** as the master running on a single processor, utilizing the two cores in a `Symmetric Multiprocessing <https://en.wikipedia.org/wiki/Symmetric_multiprocessing>`_ setup, and the green and blue colored boxes details the RTOS and Bare Metal slave applications each running on a single core of a remote processor as their own **runtime domain**. The Linux system shares memory with both slaves, but the slave applications do not share memory. Each domain owns independent peripherals in the system. Although the Linux domain is `SMP <https://en.wikipedia.org/wiki/Symmetric_multiprocessing>`_, all three **runtime domains** together make up an `AMP <https://en.wikipedia.org/wiki/Asymmetric_multiprocessing>`_ system.

Runtime Control
===============

.. raw:: html
    :file: ../images/fundamentals/runtime-control.svg

With the domains defined, **runtime control** of the asymmetric slave applications can be started. The master will load the images as required. In this example the RTOS image could be loaded at power on to perform say environmental instrument monitoring and the bare metal image on demand to perform some specific high intensity calculations, but stopped on completion for power savings.

Inter Processor Communications
==============================

.. raw:: html
    :file: ../images/fundamentals/ipc.svg

`Inter Processor Communications <https://en.wikipedia.org/wiki/Inter-process_communication>`_ is performed through shared memory and is between master and slave. In this star topology example the slaves can not communicate with each other. If that were required a chain topology would allow one remote to contain a slave and a master in which case they could communicate.

Resource Isolation
==================

Resources are shared, so the ability to utilise a supervisor, such as a hypervisor, to enforce isolatation is an important requirement for the :ref:`OpenAMP Architecture<openamp-architecture>`, along with the previously mentioned fundamentals.

.. _openamp-architecture:

********************
OpenAMP Architecture
********************

`Asymmetric Multiprocessing (AMP) <https://en.wikipedia.org/wiki/Asymmetric_multiprocessing>`_ does not specify that




Read more about OpenAMP System Considerations :ref:`here<porting-guide-work-label>`.



************
Project Aims
************

To accomplish the above, OpenAMP is divided into the following efforts:

    * A standardization group under Linaro Community Projects
        - Standardizing the low-level protocol that allows systems to interact (:ref:`more info here<rpmsg-protocol-work-label>`)
            + Built on top of `virtio <https://github.com/OpenAMP/open-amp/wiki/OpenAMP-RPMsg-Virtio-Implementation>`_ BROKEN LINK
        - Standardizing on the user level APIs that allow applications to be portable
            + `RPMSG <https://github.com/OpenAMP/open-amp/wiki/RPMsg-API-Usage>`_ BROKEN LINK
            + :ref:`remoteproc<lcm-work-label>`
        - Standardizing on the low-level :ref:`OS/HW abstraction layer<porting-guide-work-label>` that abstracts the open source implementation from the underlying OS and hardware, simplifying the porting to new environments

    * An open source project that implements a clean-room implementation of OpenAMP
        - Runs in multiple environments, see below
        - BSD License
        - Please join the :ref:`OpenAMP open source project<openamp-maintenance-work-label>`!
        - See https://github.com/OpenAMP/open-amp

**********************
Operating Environments
**********************

OpenAMP is supported in various operating environments through an a) OpenAMP open source project (OAOS), b) a Linux kernel project (OALK), and c) multiple proprietary implementations (OAPI). The Linux kernel support (OALK) comes through the regular remoteproc/RPMsg/Virtio efforts in the kernel.

The operating environments that OpenAMP supports include:

    - Linux user space - OAOS
    - Linux kernel - OALK
    - Multiple RTOS's - OAOS/OAPI including Nucleus, FreeRTOS, uC/OS, VxWorks and more
    - Bare Metal (No OS) - OAOS
    - In OS's on top of hypervisors - OAOS/OAPI
    - Within hypervisors - OAPI

********************
OpenAMP Capabilities
********************

OpenAMP currently supports the following interactions between operating environments:

    - Lifecycle operations - Such as starting and stopping another environment
    - Messaging - Sending and receiving messages
    - Proxy operations - Remote access to systems services such as file system

Read more about the OpenAMP System Components :ref:`here<openamp-components-work-label>`.

In the future OpenAMP is envisioned to also encompass other areas important in a heterogeneous environment, such as power management and managing the lifecycle of non-CPU devices.

******************
OpenAMP Guidelines
******************

There are a few guiding principles that governs OpenAMP:

    - Provide a clean-room implementation of OpenAMP with business friendly APIs and licensing
        * Allow for compatible proprietary implementations and products
    - Base as much as possible on existing technologies/open source projects/standards
        * In particular remoteproc, RPMsg and virtio
    - Never standardize on anything unless there is an open source implementation that can prove it
    - Always be backwards compatible (unless there is a really, really good reason to change)
        * In particular make sure to be compatible with the Linux kernel implementation of remoteproc/RPMsg/virtio
