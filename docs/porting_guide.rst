.. _porting-guide-work-label:

=================
Porting GuideLine
=================

The `OpenAMP Framework <https://github.com/OpenAMP/open-amp>`_ uses
`libmetal <https://github.com/OpenAMP/libmetal>`_ to provide abstractions that allows for porting
of the OpenAMP Framework to various software environments (operating systems and bare metal
environments) and machines (processors/platforms). To port OpenAMP for your platform, you will
need to:

    - add your system environment support to :ref:`libmetal<port-libmetal>`,
    - implement your platform specific :ref:`remoteproc driver<port-remoteproc>`.
    - define your shared memory layout and specify it in a resource table.

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

Any OpenAMP port will need to implement a platform specific remoteproc driver to use remoteproc
life cycle management (LCM) APIs. The remoteproc driver platform specific functions are defined
in `lib/include/openamp/remoteproc.h <https://github.com/OpenAMP/open-amp/blob/main/lib/include/openamp/remoteproc.h>`_ and provided through the :openamp_doc_link:`remoteproc_ops data structure <remoteproc_ops>`.

The remoteproc LCM APIs use these platform specific implementation of init, remove, mmap,
handle_rsc, config, start, stop, shutdown and notify. These functions are passed to remoteproc
via the remoteproc_ops structure which contains function pointers to each.

.. doxygenstruct:: remoteproc_ops
   :members:

The remoteproc_init API receives this structure, and its function pointers, which are then used
by the other APIs.

.. _port-remoteproc:

**********************************************************************
Platform Specific Porting to Use Remoteproc to Manage Remote Processor
**********************************************************************

With the platform specific remoteproc driver functions implemented by the port, the user can
use remoteproc APIs to run application on a remote processor.

.. doxygenfunction:: remoteproc_init
   :project: openamp_doc_embed

.. doxygenfunction:: remoteproc_remove

.. doxygenfunction:: remoteproc_mmap

.. doxygenfunction:: remoteproc_config

.. doxygenfunction:: remoteproc_start

.. doxygenfunction:: remoteproc_stop

.. doxygenfunction:: remoteproc_shutdown


The following code snippet is an example execution.


.. code-block:: c

  #include <openamp/remoteproc.h>

  /* User defined remoteproc operations */
  extern struct remoteproc_ops rproc_ops;

  /* User defined image store operations, such as open the image file, read
   * image from storage, and close the image file.
   */

  extern struct image_store_ops img_store_ops;
  /* Pointer to keep the image store information. It will be passed to user
   * defined image store operations by the remoteproc loading application
   * function. Its structure is defined by user.
   */
  void *img_store_info;

  struct remoteproc rproc;

  void main(void)
  {
  	/* Instantiate the remoteproc instance */
  	remoteproc_init(&rproc, &rproc_ops, &private_data);

  	/* Optional, required, if user needs to configure the remote before
  	 * loading applications.
  	 */
  	remoteproc_config(&rproc, &platform_config);

  	/* Load Application. It only supports ELF for now. */
  	remoteproc_load(&rproc, img_path, img_store_info, &img_store_ops, NULL);

  	/* Start the processor to run the application. */
  	remoteproc_start(&rproc);

  	/* ... */

  	/* Optional. Stop the processor, but the processor is not powered
  	 * down.
  	 */
  	remoteproc_stop(&rproc);

  	/* Shutdown the processor. The processor is supposed to be powered
  	 * down.
  	 */
  	remoteproc_shutdown(&rproc);

  	/* Destroy the remoteproc instance */
  	remoteproc_remove(&rproc);
  }

.. _port-rpmsg:

**************************************
Platform Specific Porting to Use RPMsg
**************************************

RPMsg in OpenAMP implementation uses VirtIO to manage the shared buffers. OpenAMP library provides
remoteproc VirtIO backend implementation. You don't have to use remoteproc backend. You can
implement your VirtIO backend with the VirtIO and RPMsg implementation in OpenAMP. If you want to
implement your own VirtIO backend, you can refer to the
`remoteproc VirtIO backend implementation <https://github.com/OpenAMP/open-amp/blob/master/lib/remoteproc/remoteproc_virtio.c>`_

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
  	 * VirtIO device master will initiate the VirtIO rings, and assign
  	 * shared buffers. If you running the application as VirtIO slave, you
  	 * set the role as VIRTIO_DEV_SLAVE.
  	 * If you don't use remoteproc, you will need to define your own VirtIO
  	 * device.
  	 */
  	vdev = remoteproc_create_virtio(&rproc, 0, VIRTIO_DEV_MASTER, NULL);

  	/* This step is only required if you are VirtIO device master.
  	 * Initialize the shared buffers pool.
  	 */
  	shbuf = metal_io_phys_to_virt(shm_io, SHARED_BUF_PA);
  	rpmsg_virtio_init_shm_pool(&shpool, shbuf, SHARED_BUFF_SIZE);

  	/* Initialize RPMsg VirtIO device with the VirtIO device */
  	/* If it is VirtIO device slave, it will not return until the master
  	 * side set the VirtIO device DRIVER OK status bit.
  	 */
  	rpmsg_init_vdev(&rpmsg_vdev, vdev, ns_bind_cb, io, shm_io, &shpool);

  	/* Get RPMsg device from RPMsg VirtIO device */
  	rpmsg_dev = rpmsg_virtio_get_rpmsg_device(&rpmsg_vdev);

  	/* Create RPMsg endpoint. */
  	rpmsg_create_ept(&ept, rdev, RPMSG_SERVICE_NAME, RPMSG_ADDR_ANY,
  			 rpmsg_ept_cb, ns_unbind_cb);

  	/* If it is VirtIO device master, it sends the first message */
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