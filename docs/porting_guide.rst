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
SRAM or DDR region accessible by both cores.
Cache maintenance operations are performed by OpenAMP if the
`WITH_DCACHE <https://github.com/OpenAMP/open-amp/blob/main/cmake/options.cmake>`_ cmake flag
is set. It should be enabled if your shared memory region is caching and the core you are
building for is not cache coherent with the remote side.

Memory requirements are generally modest because :doc:`RPMsg <../docs/rpmsg_design>` is a
control‑oriented protocol rather than a high‑bandwidth streaming channel. For example, using
the Linux RPMsg packet size of 512 bytes, a 8kB shared memory region can hold roughly 16
messages. The size and message count should be tuned based on system needs.

In addition to the messages, the Virtio ring structures need memory allocated. For Linux
this equates to 2*4k, to align with kernel page size, but likely less for other implementations.

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

For both there is a concept of a driver and device role which affect the virtio transport layer,
specified when setting up the virtio structure, via the definitions:

:openamp_doc_link:`VIRTIO_DEV_DEVICE <VIRTIO_DEV_DEVICE>` or
:openamp_doc_link:`VIRTIO_DEV_DRIVER <VIRTIO_DEV_DRIVER>`

When creating the virtio device (not to be confused with the device role), the driver role
indicates the main processor and the device role the remote processor.

In OpenAMP
`RPMsg Virtio <https://github.com/OpenAMP/open-amp/blob/main/lib/include/openamp/rpmsg_virtio.h>`_
these are aliased as
:openamp_doc_link:`RPMSG_HOST <RPMSG_HOST>` and :openamp_doc_link:`RPMSG_REMOTE <RPMSG_REMOTE>`
respectively.

The support for either of these roles can be enabled or disabled through the main CMake options,
as defined in OpenAMP's
`cmake/options.cmake <https://github.com/OpenAMP/open-amp/blob/main/cmake/options.cmake>`_

WITH_VIRTIO_DRIVER, sets the VIRTIO_DRIVER_SUPPORT and
WITH_VIRTIO_DEVICE, sets the VIRTIO_DEVICE_SUPPORT definition.

.. literalinclude:: ../open-amp/cmake/options.cmake
   :language: cmake
   :lines: 40-41

These definitions affect what is compiled into the main/driver or remote/device image and can be used
to limit code size if required. By default both are enabled.

One can think of the implementation options as four features, three of which are part of Remoteproc.

- Full Remoteproc as life cycle management, implemented in driver role on main processor
- Remoteproc Virtio transport layer for Virtio protocol
- The resource table, implemented as part of the full Remoteproc for main processor or
  independently in device role on remote processor
- RPMsg, implementing IPC and Virtio transport layer if not implemented by Remoteproc

The resulting porting implementation approaches include:

- On the main processor

  - :openamp_doc_link:`Remoteproc <remoteproc>` as driver role to manage remote processor
    life cycle
  - :openamp_doc_link:`Remoteproc Virtio <remoteproc_virtio>` to implement the virtio driver transport layer
  - :openamp_doc_link:`RPMsg <rpmsg_device>`

- On the remote processor

  - Optional :openamp_doc_link:`Remoteproc <remoteproc>` as device role for the
    :openamp_doc_link:`resource table management <resource_table>`
  - :openamp_doc_link:`Remoteproc Virtio <remoteproc_virtio>` device role to implement the
    virtio device transport layer
  - :openamp_doc_link:`RPMsg <rpmsg_device>`

Additional details and examples are provided in the subsequent sections.

Remoteproc Framework
====================

The Remoteproc framework as the name suggests is responsible for remote processor management.
For both roles this includes resource table management and/or setup of the virtio transport
and as the driver role also the remote processor lifecycle management.

Remoteproc Driver Role
----------------------

In the driver role, Remoteproc includes  management of the remote processor lifecycle and
resource table discovery.

Most :ref:`OpenAMP Samples and Demos<demos-reference-samples>` provide examples of lifecycle management for Remoteproc
in the driver role.

The
`load_fw <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/legacy_apps/examples/load_fw>`_
is an example dedicated to demonstrating Remoteproc lifecycle management.

Remoteproc Device Role
----------------------

Use of Remoteproc framework for the remote or device role is optional and when used is for
resource table management, parsing the resource table for dynamic resource allocation or
statically assigning the resources required for Remoteproc.

Dynamic examples are:

- `ZynqMP R5 <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/legacy_apps/machine/xlnx/zynqmp_r5/platform_info.c>`_
  machine implementation example.

Management using a static resource examples are:

- `Multi Services Remote Example <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/zephyr/rpmsg_multi_services/src/main_remote.c>`_.

Remoteproc Virtio Framework
===========================

When using Remoteproc, the
`Virtio transport layer <https://github.com/OpenAMP/open-amp/main/lib/remoteproc/remoteproc_virtio.c>`_
is created through it (as compared to through
`RPMsg's Virtio <https://github.com/OpenAMP/open-amp/blob/main/lib/rpmsg/rpmsg_virtio.c>`_).

Remoteproc Virtio Driver Role
-----------------------------

For the main processor driver role, Remoteproc is used

- to obtain and configure resource table information.
- create the main processor or driver side Virtio device

The intent of OpenAMP Remoteproc is to remain compatible with Linux's Remoteproc.

The
`Multi Services Example <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/zephyr/rpmsg_multi_services>`_
example uses Linux Remoteproc for the driver role implementation.
For details refer to :ref:`RPMsg Multi Services<rpmsg-multi-services-intro>` Demo.

Remoteproc Virtio Device Role
-----------------------------

For the remote processor device role, Remoteproc is used

- to get resource table information populated by the Virtio driver
- create remote or device side Virtio device

The
`Multi Services <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/zephyr/rpmsg_multi_services/src/main_remote.c>`_
Example Remote shows Remoteproc Virtio device creation using
:openamp_doc_link:`rproc_virtio_create_vdev <rproc_virtio_create_vdev>`
and obtaining the resource table using Zephyr's
`rsc_table_get <https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/ipc/open-amp/resource_table.c>`_
function.


RPMsg Framework
===============

The RPMsg Framework provides the IPC which is based on Virtio.

When using Remoteproc, the Virtio used for RPMsg is setup by it for the main processor as the
driver role and device role for the remote.

When the implementation does not require Remoteproc, OpenAMP provides Virtio through the
`RPMsg  Virtio Framework  <https://github.com/OpenAMP/open-amp/blob/main/lib/rpmsg/rpmsg_virtio.c>`_.

The `Zephyr OpenAMP IPC Sample <https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/subsys/ipc/openamp>`_
is one demonstrating the use of Virtio through RPMsg framework using static vrings as the transport layer.

The main processor Virtio device is setup as driver role, using
:openamp_doc_link:`RPMSG_HOST <RPMSG_HOST>` passed to
:openamp_doc_link:`rpmsg_init_vdev <rpmsg_init_vdev>`.

Refer
`Zephyr OpenAMP IPC Sample Main <https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/subsys/ipc/openamp/src/main.c>`_
for an example driver role implementation.

The remote processor Virtio device is setup as device role, using
:openamp_doc_link:`RPMSG_REMOTE <RPMSG_REMOTE>` passed to
:openamp_doc_link:`rpmsg_init_vdev <rpmsg_init_vdev>`.

Refer
`Zephyr OpenAMP IPC Sample Remote <https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/subsys/ipc/openamp/remote/src/main.c>`_
for an example device role implementation.


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

For example Cortex-R5 remoteproc_ops are defined in
`zynqmp_r5_a53_rproc.c <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/legacy_apps/machine/xlnx/zynqmp_r5/zynqmp_r5_a53_rproc.c>`_.

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

For an example of setting up Remoteproc Virtio for a remote device refer to
`zynqmp_r5 platform_info.c <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/legacy_apps/machine/xlnx/zynqmp_r5/platform_info.c>`_.
