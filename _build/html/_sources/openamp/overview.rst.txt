================
Project Overview
================

*************
OpenAMP Intro
*************

OpenAMP is a community effort that is standardizing and implementing how multiple embedded environments interact with each other using AMP. It provides conventions and standards as well as an open source implementation to facilitate AMP development for embedded systems. Read more about Asymmentric Multiprocessing :ref:`here<asymmetric-multiprocessing-work-label>`. 

The vision is that regardless of the operating environment/operating system, it should be possible to use identical interfaces to interact with other operating environments in the same system.

Furthermore, these operating environments can interoperate over a standardized protocol, making it possible to mix and match any two or more operating systems in the same device.

Read more about OpenAMP System Considerations :ref:`here<porting-guide-work-label>`.

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
