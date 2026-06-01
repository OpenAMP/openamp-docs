.. _porting-guide-work-label:

=================
Porting GuideLine
=================

********
Hardware
********

The porting of OpenAMP to a new :doc:`multicore system <../openamp/overview>` requires
some hardware for inter-processor communication.

- Shared memory for

    - the :ref:`RPMsg<overview-rpmsg-work-label>` buffer
    - the :ref:`Virtio Rings<docs/data_structures_content:Shared virtqueue structure>`
    - the :ref:`Resource Table<resource-table>`
      (optional if the RPMsg host is not the Linux kernel)

- Optional, but recommended, mailboxes acting as a ring bell interrupt on processors to
  notify of message reception

Memory and interrupt assignments are critical design choices for any port. For a broader overview, refer to
:doc:`../protocol_details/system_considerations`.


Shared Memory
=============

Shared memory forms the :ref:`physical layer<rpmsg-layers-work-label>` for
:doc:`RPMsg <../docs/rpmsg_design>` protocol.
The specific memory type and layout are implementation dependent, but should be a dedicated
SRAM or DDR region accessible by both cores. Caching is enabled in OpenAMP with the
`WITH_DCACHE <https://github.com/OpenAMP/open-amp/blob/main/cmake/options.cmake>`_
cmake configuration.

Memory requirements are generally modest because :doc:`RPMsg <../docs/rpmsg_design>` is a
control‑oriented protocol rather than a high‑bandwidth streaming channel. For example, using
the Linux RPMsg packet size of 512 bytes, a 64kB shared memory region can hold roughly 128
messages — sufficient for most applications. Larger or smaller allocations can be chosen based
on system needs.

In addition to the messages, the Virtio ring structures need memory allocated. For Linux
this equates to 2*4k but likely less for other implementations.

If the :ref:`Resource Table<resource-table>` is not embedded in the remote firmware image,
additional shared memory may be required for a dynamic table.

:ref:`Remoteproc<overview-remoteproc-work-label>` can also use shared memory for optional
trace buffers.


Memory Protection
-----------------

Because this is shared memory, appropriate hardware memory protection should be configured
on both processors.

Depending on the memory type, this may involve configuring the Memory Management Unit (MMU),
Memory Protection Unit (MPU), or Input-Output Memory Management Unit (IOMMU) to enforce
correct access permissions.

On systems running an advanced OS — such as Linux on the main
processor — these protections may be applied through OS mechanisms like the device tree or
via the :ref:`Remoteproc<overview-remoteproc-work-label>` :ref:`Resource Table<resource-table>`.


Notification
------------

:doc:`RPMsg <../docs/rpmsg_design>` uses :ref:`ring buffers<rpmsg-protocol-mac>` in shared
memory, so either processor can poll for incoming messages. However, asynchronous notification
via interrupts is recommended.

Most heterogeneous SoCs include a built‑in inter‑core interrupt mechanism, often called a
mailbox. The sending core raises the mailbox interrupt to notify the other core that a vring has
been updated for message reception, buffer release, or both.
The core can then manage the message in normal context, for example, in a thread, or in
interrupt.


***************
Porting Options
***************

OpenAMP consists of two major components: :ref:`Remoteproc<overview-remoteproc-work-label>`
and :doc:`RPMsg <../docs/rpmsg_design>`. These can be ported
independently or together.

The :doc:`RPMsg <../docs/rpmsg_design>` port on the main processor is usually a virtio driver
level and the remote processor the virtio device role.

`libmetal <https://github.com/OpenAMP/libmetal>`_ provides the
:ref:`hardware abstraction layer<hardware-abstraction>` for both.

The main porting approaches include:

- :ref:`Remoteproc<overview-remoteproc-work-label>` on the remote processor only,
  with the main processor using an existing
  :ref:`Remoteproc<overview-remoteproc-work-label>` implementation (e.g., Linux Remoteproc)
  and no IPC.

- :doc:`RPMsg <../docs/rpmsg_design>` on the remote processor only, with the main processor
  using an existing :doc:`RPMsg <../docs/rpmsg_design>` stack (e.g., Linux RPMsg) and no
  remote firmware management.

- Custom device‑level implementation of :ref:`Remoteproc<overview-remoteproc-work-label>`
  and/or :doc:`RPMsg <../docs/rpmsg_design>` for both processors.


.. _driver-lcm-remoteproc:

Driver Lifecycle Management via Remoteproc
==========================================

Some systems do not require IPC or use an alternative IPC mechanism. In these cases, only
:ref:`Remoteproc<overview-remoteproc-work-label>` may be ported (or reused, as on Linux)
on both the main and remote processors.

The main processor uses driver level :ref:`Remoteproc<overview-remoteproc-work-label>` to
load, start, stop, and manage remote firmware.
This approach is useful when the remote firmware must be externally controlled or when
multiple firmware images may be deployed depending on runtime needs.
This configuration is common in custom or bare‑metal remote environments.

- Pros: Full remote firmware management
- Cons: No IPC. Larger software footprint


.. _driver-lcm-remoteproc-rpmsg:

Driver Lifecycle Management via Remoteproc with IPC
===================================================

This setup is the most complete and includes driver based lifecycle management and IPC.
In these cases, both :ref:`Remoteproc<overview-remoteproc-work-label>` and
:doc:`RPMsg <../docs/rpmsg_design>` need to be ported (or reused, as on Linux) on both
the main and remote processors.

The main processor uses driver level :ref:`Remoteproc<overview-remoteproc-work-label>` and
:doc:`RPMsg <../docs/rpmsg_design>`.

This approach is useful when full IPC and remote firmware control is required.

This configuration is common in custom or bare‑metal remote environments.

- Pros: Full IPC and remote firmware management
- Cons: Largest software footprint


.. _driver-rpmsg:

Driver to Remote IPC via RPMsg
==============================

If the remote firmware is static and starts at boot, or if another framework manages
firmware loading, only :doc:`RPMsg <../docs/rpmsg_design>` needs to be ported.
In this model, the remote processor runs its firmware autonomously, and the main processor
interacts with it solely through the :doc:`RPMsg <../docs/rpmsg_design>` communication channel,
without any involvement in firmware lifecycle control. This approach suits systems where the
remote environment is minimal or bare‑metal, and where the primary requirement is efficient
message‑based IPC rather than external management of the remote core.

- Pros: Lightweight. Provides IPC.
- Cons: No remote firmware management.


.. _device-lcm-remoteproc:

Device Level Custom Remoteproc and RPMsg
========================================

In highly customized or bare‑metal only environments, a port of
:ref:`Remoteproc<overview-remoteproc-work-label>` and :doc:`RPMsg <../docs/rpmsg_design>` may
be required without any driver‑level abstraction.
In this case, the full :ref:`Remoteproc<overview-remoteproc-work-label>` and
:doc:`RPMsg <../docs/rpmsg_design>` mechanism must be implemented
directly on both the main and remote processors, ensuring that each core provides the necessary
firmware lifecycle management, messaging, shared‑memory handling, and notification logic without
relying on OS‑level drivers or frameworks.

- Pros: Lightweight.
- Cons: Highly custom and less portable.


.. _device-rpmsg:

Device Level Custom RPMsg
=========================

In a simpler bare‑metal only environments, a port of only :doc:`RPMsg <../docs/rpmsg_design>` may
be required without any driver‑level abstraction.
In this case, only the :doc:`RPMsg <../docs/rpmsg_design>` mechanism need be implemented
directly on both the main and remote processors, ensuring that each core provides the necessary
IPC and notification logic without relying on OS‑level drivers or frameworks.

- Pros: Very lightweight.
- Cons: Highly custom and less portable.


.. _hardware-abstraction:

********************
Hardware Abstraction
********************

The `OpenAMP Framework <https://github.com/OpenAMP/open-amp>`_ uses
`libmetal <https://github.com/OpenAMP/libmetal>`_ to provide abstractions that allows for porting
of the OpenAMP Framework to various software environments (operating systems and bare metal
environments) and machines (processors/platforms). To port OpenAMP for your platform, you will
need to:

    - add your system environment support to :ref:`libmetal<port-libmetal>`,
    - optionally implement a platform specific :ref:`remoteproc driver<port-remoteproc>`.
    - define your shared memory layout and specify it in a :ref:`resource table<resource-table>`.

.. _port-libmetal:

**************************************
Add System/Machine Support in Libmetal
**************************************

User will need to add system/machine support to
`lib/system/<SYS>/ <https://github.com/OpenAMP/libmetal/tree/main/lib/system>`_ directory in
libmetal repository. OpenAMP requires the following libmetal primitives:

alloc
=====

Memory allocation and memory free as defined in
`alloc.h <https://github.com/OpenAMP/libmetal/blob/main/lib/alloc.h>`_, which call the
functions of equivalent names with double underscore which are the ported functions
(__metal_allocate_memory, __metal_free_memory).

.. doxygenfunction:: metal_allocate_memory
   :project: libmetal_doc_embed

.. doxygenfunction:: metal_free_memory
   :project: libmetal_doc_embed


io
==

Memory mapping as used by `io.h <https://github.com/OpenAMP/libmetal/blob/main/lib/io.h>`_,
in order to access vrings and carved out memory.

:libmetal_doc_link:`metal_sys_io_mem_map <metal_sys_io_mem_map>` and
:libmetal_doc_link:`metal_machine_io_mem_map <metal_machine_io_mem_map>` functions.

mutex
=====

Mutex functions as used by `mutex.h <https://github.com/OpenAMP/libmetal/blob/main/lib/mutex.h>`_
which call the functions of equivalent names with double underscore which are the ported functions
(e.g. __metal_mutex_init).

.. doxygenfunction:: metal_mutex_init
   :project: libmetal_doc_embed

.. doxygenfunction:: metal_mutex_deinit
   :project: libmetal_doc_embed

.. doxygenfunction:: metal_mutex_try_acquire
   :project: libmetal_doc_embed

.. doxygenfunction:: metal_mutex_acquire
   :project: libmetal_doc_embed

.. doxygenfunction:: metal_mutex_release
   :project: libmetal_doc_embed

.. doxygenfunction:: metal_mutex_is_acquired
   :project: libmetal_doc_embed

sleep
=====

At the moment, OpenAMP only requires microseconds sleep as when OpenAMP fails to get a buffer to
send messages, it will call this function to sleep and then try again.

The __metal_sleep_usec to be implemented by the port is wrapped in
`sleep.h <https://github.com/OpenAMP/libmetal/blob/main/lib/sleep.h>`_.

.. doxygenfunction:: metal_sleep_usec
   :project: libmetal_doc_embed

init
====

Init is ported for libmetal initialization for
`sys.h <https://github.com/OpenAMP/libmetal/blob/main/lib/sys.h>`_.


:libmetal_doc_link:`metal_sys_init <metal_sys_init>` and
:libmetal_doc_link:`metal_sys_finish <metal_sys_finish>` functions.


Please refer to
`lib/system/generic/ <https://github.com/OpenAMP/libmetal/tree/main/lib/system/generic>`_
when adding RTOS support to libmetal.

libmetal uses C11/C++11 stdatomics interface for atomic operations, if you use a different
compiler to GNU gcc, you may need to implement the atomic operations defined in
`lib/compiler/gcc/atomic.h <https://github.com/OpenAMP/libmetal/blob/main/lib/compiler/gcc/atomic.h>`_.


.. _port-remoteproc-driver:


***********************************
Platform Specific Remoteproc Driver
***********************************

An OpenAMP port could need a platform specific :ref:`Remoteproc<overview-remoteproc-work-label>`
driver to use :ref:`Remoteproc<overview-remoteproc-work-label>` life cycle management (LCM) APIs.
The :ref:`Remoteproc<overview-remoteproc-work-label>` driver platform specific functions are defined in
`lib/include/openamp/remoteproc.h <https://github.com/OpenAMP/open-amp/blob/main/lib/include/openamp/remoteproc.h>`_
and provided through the :openamp_doc_link:`remoteproc_ops data structure <remoteproc_ops>`.

The remoteproc LCM APIs use these platform specific implementation of init, remove, mmap,
handle_rsc, config, start, stop, shutdown and notify. These functions are passed to remoteproc
via the remoteproc_ops structure which contains function pointers to each.

.. doxygenstruct:: remoteproc_ops
   :members:

The remoteproc_init API receives this structure, and its function pointers, which are then used
by the other APIs.

.. _port-remoteproc:


Use Remoteproc to Manage Remote Processor
=========================================

With the :ref:`remoteproc driver functions<port-remoteproc-driver>` required
by the framework ported, the user can call the :ref:`Remoteproc<overview-remoteproc-work-label>`
APIs to run an application on a remote processor, as described in the
:ref:`Remote User APIs<remoteproc_config>` section of the Remoteproc design.

The following code snippets from the
`Load FW System Reference Example <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/legacy_apps/examples/load_fw>`_
demonstrate the use of the Remote User APIs.

Remoteproc Init
---------------

From `platform_info.c <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/legacy_apps/examples/load_fw/platform_info.c>`_

.. literalinclude::  ../openamp-system-reference/examples/legacy_apps/examples/load_fw/platform_info.c
   :language: c
   :lines: 16-31


Lifecycle APIs
--------------

From `load_fw.c <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/legacy_apps/examples/load_fw/load_fw.c>`_

.. literalinclude::  ../openamp-system-reference/examples/legacy_apps/examples/load_fw/load_fw.c
   :language: c
   :lines: 21-57


.. _port-rpmsg:

***********************
Platform Specific RPMsg
***********************

In OpenAMP, :doc:`RPMsg <../docs/rpmsg_design>` uses
`VirtIO <https://docs.oasis-open.org/virtio/virtio/>`_ to manage shared buffers.
The OpenAMP library provides a
`Remoteproc VirtIO <https://github.com/OpenAMP/open-amp/blob/main/lib/remoteproc/remoteproc_virtio.c>`_
backend implementation, and a
`VirtIO and RPMsg <https://github.com/OpenAMP/open-amp/blob/main/lib/rpmsg/rpmsg_virtio.c>`_
implementation.

You can also implement your own VirtIO backend using the
`OpenAMP VirtIO <https://github.com/OpenAMP/open-amp/tree/main/lib/virtio>`_ and
`RPMsg <https://github.com/OpenAMP/open-amp/tree/main/lib/rpmsg>`_ components provided by OpenAMP.

If you choose to create your own backend, you can use the
`Remoteproc VirtIO <https://github.com/OpenAMP/open-amp/blob/main/lib/remoteproc/remoteproc_virtio.c>`_
backend as a reference.

For an example of setting up Remoteproc and Virtio for a remote device refer to
`zynqmp platform_info.c <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/legacy_apps/machine/xlnx/zynqmp/platform_info.c>`_

*****************
Examples of Ports
*****************


Example of Driver based Remoteproc Virtio
=========================================

Most of the :doc:`../demos/index` are examples of example of :ref:`driver-lcm-remoteproc-rpmsg`,
using Virtio through a :ref:`Resource Table<resource-table>` with the most advanced being the
`Zephyr RPMsg Multi Service Demo <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/zephyr/rpmsg_multi_services>`_
detailed in :doc:`../demos/rpmsg_multi_services`.


Example of Device based RPMsg only with Virtio
==============================================

For an example of :ref:`device-rpmsg` without Remoteproc and a Resource Table, refer to the
`Zephyr IPC OpenAMP Demo <https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/subsys/ipc/openamp>`_
