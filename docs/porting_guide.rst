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
    - the :ref:`VirtIO Rings<docs/data_structures_content:Shared virtqueue structure>`
    - the :ref:`Resource Table<resource-table>`
      (optional if the RPMsg host is not the Linux kernel)

- Optional, but recommended, mailboxes acting as a doorbell interrupt on processors to
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
is set. It should be enabled if your shared memory region is cacheable and the core you are
building for is not cache coherent with the remote side.

Memory requirements are generally modest because :doc:`RPMsg <../docs/rpmsg_design>` is a
control‑oriented protocol rather than a high‑bandwidth streaming channel.
For example, with Linux’s 512-byte RPMsg buffer size (496 bytes of payload after the 16-byte
header), an 8 kB buffer region provides 16 buffers - 8 per direction, since the pool is split
between TX and RX. This is in addition to the vring memory described below.
The size and message count should be tuned based on system needs.

In addition to the messages, the VirtIO ring structures need memory allocated. For Linux
this equates to 2*4k, to align with kernel page size, but likely less for other implementations.

If the :ref:`Resource Table<resource-table>` is not embedded in the remote firmware image,
additional shared memory may be required for a dynamic table.

:ref:`Remoteproc<overview-remoteproc-work-label>` can also use shared memory for optional
trace buffers.


Memory Protection
-----------------

Because this is shared memory, appropriate hardware memory protection should be configured
on both processors, to enforce correct access permissions.

Depending on the memory type, this may involve configuring the Memory Management Unit (MMU),
Memory Protection Unit (MPU), Input-Output Memory Management Unit (IOMMU), or some other
memory protection mechanism.


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

For the the RPmsg and VirtIO transport, there is a concept of a driver and device role which
affect the layers.

- The :openamp_doc_link:`VIRTIO_DEV_DEVICE <VIRTIO_DEV_DEVICE>` role and its alias
  :openamp_doc_link:`RPMSG_REMOTE <RPMSG_REMOTE>` refer to the VirtIO instance of the remote processor.
- The :openamp_doc_link:`VIRTIO_DEV_DRIVER <VIRTIO_DEV_DRIVER>` role and its alias
  :openamp_doc_link:`RPMSG_HOST <RPMSG_HOST>` refer to the VirtIO instance of the main processor.

The support for either of these roles can be enabled or disabled through the main CMake options,
as defined in OpenAMP's
`cmake/options.cmake <https://github.com/OpenAMP/open-amp/blob/main/cmake/options.cmake>`_

- set the **VIRTIO_DRIVER_SUPPORT** cmake configuration to define **WITH_VIRTIO_DRIVER**
- set the **VIRTIO_DEVICE_SUPPORT** cmake configuration to define **WITH_VIRTIO_DIVICE**


.. literalinclude:: ../open-amp/cmake/options.cmake
   :language: cmake
   :lines: 40-41

These definitions affect what is compiled into the main/driver or remote/device image and can be used
to limit code size if required. By default both are enabled.

One can think of the implementation options as four features, three of which are part of Remoteproc.

- Full Remoteproc as life cycle management, implemented in driver role on main processor
- The resource table, implemented as part of the full Remoteproc for main processor or
  independently in device role on remote processor
- Remoteproc VirtIO transport layer for VirtIO protocol
- RPMsg, implementing IPC and VirtIO transport layer if not implemented by Remoteproc

The resulting porting implementation approaches include:

- On the main processor

  - :openamp_doc_link:`Remoteproc <remoteproc>` as driver role to manage remote processor, with optional
    associated :openamp_doc_link:`resource table management <resource_table>`
  - :openamp_doc_link:`Remoteproc VirtIO <remoteproc_virtio>` to implement the VirtIO driver transport layer
  - :openamp_doc_link:`RPMsg <rpmsg_device>`

- On the remote processor

  - Optional :openamp_doc_link:`Remoteproc <remoteproc>` as device role for the
    :openamp_doc_link:`resource table management <resource_table>`
  - :openamp_doc_link:`Remoteproc VirtIO <remoteproc_virtio>` device role to implement the
    VirtIO device transport layer
  - :openamp_doc_link:`RPMsg <rpmsg_device>`

Additional details and examples are provided in the subsequent sections.

Remoteproc Framework
====================

The Remoteproc framework as the name suggests is responsible for remote processor management.
For both roles this includes resource table management and/or setup of the VirtIO transport
and as the driver role also the remote processor lifecycle management.

Remoteproc Driver Role
----------------------

In the driver role, Remoteproc includes  management of the remote processor lifecycle and
resource table management. For instance, if no address is specified for the VirtIO vrings
and buffers, the main processor allocates the memory regions and updates the resource table
accordingly.

Most :ref:`OpenAMP Samples and Demos<demos-reference-samples>` provide examples of lifecycle management for Remoteproc
in the driver role.

The
`load_fw <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/legacy_apps/examples/load_fw>`_
is an example dedicated to demonstrating Remoteproc lifecycle management.

Remoteproc Device Role
----------------------

Use of Remoteproc framework for the remote or device role is optional and when used is for
resource discovery, parsing the resource table to determine the resources allocated.
The resources may be statically defined in the table, or dynamically assigned by the main or
driver processor and updated in the table.

Dynamic examples are:

- `ZynqMP R5 <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/legacy_apps/machine/xlnx/zynqmp_r5/platform_info.c>`_
  machine implementation example.

Management using a static resource examples are:

- `Multi Services Remote Example <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/zephyr/rpmsg_multi_services/src/main_remote.c>`_.

Remoteproc VirtIO Framework
===========================

When using Remoteproc, the
`VirtIO transport layer <https://github.com/OpenAMP/open-amp/blob/main/lib/remoteproc/remoteproc_virtio.c>`_
is created through it (as compared to through
`RPMsg's VirtIO <https://github.com/OpenAMP/open-amp/blob/main/lib/rpmsg/rpmsg_virtio.c>`_).

Remoteproc VirtIO Driver Role
-----------------------------

For the main processor driver role, Remoteproc is used

- to obtain and configure resource table information.
- create the main processor or driver side VirtIO device

The intent of OpenAMP Remoteproc is to remain compatible with Linux's Remoteproc.

The
`Multi Services Example <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/zephyr/rpmsg_multi_services>`_
example uses Linux Remoteproc for the driver role implementation.
For details refer to :ref:`RPMsg Multi Services<rpmsg-multi-services-intro>` Demo.

Remoteproc VirtIO Device Role
-----------------------------

For the remote processor device role, Remoteproc is used

- to get resource table information populated by the VirtIO driver
- create remote or device side VirtIO device

The
`Multi Services <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/zephyr/rpmsg_multi_services/src/main_remote.c>`_
Example Remote shows Remoteproc VirtIO device creation using
:openamp_doc_link:`rproc_virtio_create_vdev <rproc_virtio_create_vdev>`
and obtaining the resource table using Zephyr's
`rsc_table_get <https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/ipc/open-amp/resource_table.c>`_
function.


RPMsg Framework
===============

The RPMsg Framework provides the IPC which is based on VirtIO.

When using Remoteproc, the VirtIO used for RPMsg is setup by it for the main processor as the
driver role and device role for the remote.

When the implementation does not require Remoteproc, OpenAMP provides VirtIO through the
`RPMsg  Virtio Framework  <https://github.com/OpenAMP/open-amp/blob/main/lib/rpmsg/rpmsg_virtio.c>`_.

The `Zephyr OpenAMP IPC Sample <https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/subsys/ipc/openamp>`_
is one demonstrating the use of VirtIO through RPMsg framework using static vrings as the transport layer.

The main processor VirtIO device is setup as driver role, using
:openamp_doc_link:`RPMSG_HOST <RPMSG_HOST>` passed to
:openamp_doc_link:`rpmsg_init_vdev <rpmsg_init_vdev>`.

Refer
`Zephyr OpenAMP IPC Sample Main <https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/subsys/ipc/openamp/src/main.c>`_
for an example driver role implementation.

The remote processor VirtIO device is setup as device role, using
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
    - optionally implement a platform specific :ref:`Remoteproc driver<port-remoteproc>`.
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

The Remoteproc LCM APIs use these platform specific implementation of init, remove, mmap,
handle_rsc, config, start, stop, shutdown and notify. These functions are passed to Remoteproc
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

With the :ref:`Remoteproc driver functions<port-remoteproc-driver>` required
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
   :start-at: int load_exectuable_block
   :end-before: int load_exectuable_noblock




.. _port-rpmsg:

**************************************
Platform Specific Porting to Use RPMsg
**************************************

RPMsg in OpenAMP implementation uses `VirtIO <https://docs.oasis-open.org/virtio/virtio/>`_
to manage the shared buffers. OpenAMP library provides
`remoteproc VirtIO backend implementation <https://github.com/OpenAMP/open-amp/blob/main/lib/remoteproc/remoteproc_virtio.c>`_.
You don't have to use remoteproc backend. You can implement your VirtIO backend with the VirtIO
and RPMsg implementation in OpenAMP. If you want to implement your own VirtIO backend, you can
refer to the
`remoteproc VirtIO backend implementation < https://github.com/OpenAMP/open-amp/blob/main/lib/remoteproc/remoteproc_virtio.c>`_.

Here are the steps to use OpenAMP for RPMsg communication:


.. code-block:: c

  #include <openamp/remoteproc.h>
  #include <openamp/rpmsg.h>
  #include <openamp/rpmsg_virtio.h>

  /* User defined remoteproc operations for communication */
  sturct remoteproc rproc_ops = {
  	.init = local_rproc_init;
  	.mmap = local_rproc_mmap;
  	.notify = local_rproc_notify;
  	.remove = local_rproc_remove;
  };

  /* Remoteproc instance. If you don't use Remoteproc VirtIO backend,
   * you don't need to define the remoteproc instance.
   */
  struct remoteproc rproc;

  /* RPMsg VirtIO device instance. */
  struct rpmsg_virtio_device rpmsg_vdev;

  /* RPMsg device */
  struct rpmsg_device *rpmsg_dev;

  /* Resource Table. Resource table is used by remoteproc to describe
   * the shared resources such as vdev(VirtIO device) and other shared memory.
   * Resource table resources definition is in the remoteproc.h.
   * Examples of the resource table can be found in the OpenAMP repo:
   *  - apps/machine/zynqmp/rsc_table.c
   *  - apps/machine/zynqmp_r5/rsc_table.c
   *  - apps/machine/zynq7/rsc_table.c
   */
  void *rsc_table = &resource_table;

  /* Size of the resource table */
  int rsc_size = sizeof(resource_table);

  /* Shared memory metal I/O region. It will be used by OpenAMP library
   * to access the memory. You can have more than one shared memory regions
   * in your application.
   */
  struct metal_io_region *shm_io;

  /* VirtIO device */
  struct virtio_device *vdev;

  /* RPMsg shared buffers pool */
  struct rpmsg_virtio_shm_pool shpool;

  /* Shared buffers */
  void *shbuf;

  /* RPMsg endpoint */
  struct rpmsg_endpoint ept;

  /* User defined RPMsg name service callback. This callback is called
   * when there is no registered RPMsg endpoint is found for this name
   * service. User can create RPMsg endpoint in this callback. */
  void ns_bind_cb(struct rpmsg_device *rdev, const char *name, uint32_t dest);

  /* User defined RPMsg endpoint received message callback */
  void rpmsg_ept_cb(struct rpmsg_endpoint *ept, void *data, size_t len,
  		uint32_t src, void *priv);

  /* User defined RPMsg name service unbind request callback */
  void ns_unbind_cb(struct rpmsg_device *rdev, const char *name, uint32_t dest);

  void main(void)
  {
  	/* Instantiate remoteproc instance */
  	remoteproc_init(&rproc, &rproc_ops);

  	/* Mmap shared memories so that they can be used */
  	remoteproc_mmap(&rproc, &physical_address, NULL, size,
  			<memory_attributes>, &shm_io);

  	/* Parse resource table to remoteproc */
  	remoteproc_set_rsc_table(&rproc, rsc_table, rsc_size);

  	/* Create VirtIO device from remoteproc.
  	 * VirtIO device main controller will initiate the VirtIO rings, and assign
  	 * shared buffers. If you running the application as VirtIO device, you
  	 * set the role as VIRTIO_DEV_DEVICE.
  	 * If you don't use remoteproc, you will need to define your own VirtIO
  	 * device.
  	 */
  	vdev = remoteproc_create_virtio(&rproc, 0, VIRTIO_DEV_DRIVER, NULL);

  	/* This step is only required if you are VirtIO device main controller.
  	 * Initialize the shared buffers pool.
  	 */
  	shbuf = metal_io_phys_to_virt(shm_io, SHARED_BUF_PA);
  	rpmsg_virtio_init_shm_pool(&shpool, shbuf, SHARED_BUFF_SIZE);

  	/* Initialize RPMsg VirtIO device with the VirtIO device */
  	/* If it is VirtIO device, it will not return until the main
  	 * controller side sets the VirtIO device DRIVER OK status bit.
  	 */
  	rpmsg_init_vdev(&rpmsg_vdev, vdev, ns_bind_cb, io, shm_io, &shpool);

  	/* Get RPMsg device from RPMsg VirtIO device */
  	rpmsg_dev = rpmsg_virtio_get_rpmsg_device(&rpmsg_vdev);

  	/* Create RPMsg endpoint. */
  	rpmsg_create_ept(&ept, rdev, RPMSG_SERVICE_NAME, RPMSG_ADDR_ANY,
  			 rpmsg_ept_cb, ns_unbind_cb);

  	/* If it is VirtIO device main controller, it sends the first message */
  	while (!is_rpmsg_ept_read(&ept)) {
  		/* check if the endpoint has binded.
  		 * If not, wait for notification. If local endpoint hasn't
  		 * been bound with the remote endpoint, it will fail to
  		 * send the message to the remote.
  		 */
  		/* If you prefer to use interrupt, you can wait for
  		 * interrupt here, and call the VirtIO notified function
  		 * in the interrupt handling task.
  		 */
  		rproc_virtio_notified(vdev, RSC_NOTIFY_ID_ANY);
  	}
  	/* Send RPMsg */
  	rpmsg_send(&ept, data, size);

  	do {
  		/* If you prefer to use interrupt, you can wait for
  		 * interrupt here, and call the VirtIO notified function
  		 * in the interrupt handling task.
  		 * If vdev is notified, the endpoint callback will be
  		 * called.
  		 */
  		rproc_virtio_notified(vdev, RSC_NOTIFY_ID_ANY);
  	} while(!ns_unbind_cb_is_called && !user_decided_to_end_communication);

  	/* End of communication, destroy the endpoint */
  	rpmsg_destroy_ept(&ept);

  	rpmsg_deinit_vdev(&rpmsg_vdev);

  	remoteproc_remove_virtio(&rproc, vdev);

  	remoteproc_remove(&rproc);
  }

.