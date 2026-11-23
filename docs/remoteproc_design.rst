Remoteproc Design Document
===========================

Remoteproc provides abstraction to manage the life cycle of a remote
application. For now, it only provides APIs on bringing up and
tearing down the remote application, and parsing resource table.
It will extend to crash detection, suspend and resume.

Remoteproc LCM States
---------------------

.. csv-table::
   :header: "State", "State Description"
   :widths: 50, 200

    Offline, "Initial state of a remoteproc instance. The remote presented by the remoteproc instance and its resource has been powered off."
    Configured, "The remote presented by the remoteproc instance has been configured. And ready to load application."
    Ready, "The remote presented by the remoteproc instance has application loaded, and ready to run."
    Stopped, "The remote presented by the remoteproc instance has stopped from running. But the remote is still powered on. And the remote's resource hasn't been released."

..  image:: ../images/design/img/rproc-lcm-state-machine.png


State Transition
----------------

.. csv-table::
   :header: "State Transition", "Transition Trigger"
   :widths: 50, 200

    Offline -> Configured, "Configure the remote to make it able to load application :ref:`remoteproc_config<remoteproc_config>`"
    Configured -> Ready, "load firmware :ref:`remoteproc_load<remoteproc_load>`"
    Ready -> Running, "start the processor :ref:`remoteproc_start<remoteproc_start>`"
    Ready -> Stopped, "stop the processor :ref:`remoteproc_stop<remoteproc_stop>`, :ref:`remoteproc_shutdown<remoteproc_shutdown>` (Stopped is the intermediate state of shutdown operation)"
    Running -> Stopped, "stop the processor :ref:`remoteproc_stop<remoteproc_stop>`, :ref:`remoteproc_shutdown<remoteproc_shutdown>`"
    Stopped -> Offline, "shutdown the processor :ref:`remoteproc_shutdown<remoteproc_shutdown>`"

Remote User APIs
----------------
.. _remoteproc_config:

Initialize Remoteproc Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_init
   :project: openamp_doc_embed

Release Remoteproc Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_remove
   :project: openamp_doc_embed

Add Memory to Remoteproc
^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_add_mem
   :project: openamp_doc_embed

Get Memory Libmetal I/O Region From Remoteproc Specifying Memory Name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_get_io_with_name
   :project: openamp_doc_embed

Get Memory Libmetal I/O Region From Remoteproc Specifying Physical Address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_get_io_with_pa
   :project: openamp_doc_embed

Get Memory Libmetal I/O Region From Remoteproc Specifying Virtual Address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_get_io_with_va
   :project: openamp_doc_embed

Map Memory and Add the Memory to the Remoteproc Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_mmap
   :project: openamp_doc_embed

Set Resource Table to Remoteproc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_set_rsc_table
   :project: openamp_doc_embed

Configure the Remote Presented by the Remoteproc Instance to Make It Able to Load Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_config
   :project: openamp_doc_embed

Load Application to the Remote Presented by the Remoteproc Instance to Make It Ready to Run
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _remoteproc_load:
.. doxygenfunction:: remoteproc_load
   :project: openamp_doc_embed

Run Application on the Remote Presented by the Remoteproc Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _remoteproc_start:
.. doxygenfunction:: remoteproc_start
   :project: openamp_doc_embed

Stop Application on Remote Presented by the Remoteproc Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _remoteproc_stop:
.. doxygenfunction:: remoteproc_stop
   :project: openamp_doc_embed

Shutdown the Remote Presented by the Remoteproc Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _remoteproc_shutdown:
.. doxygenfunction:: remoteproc_shutdown
   :project: openamp_doc_embed

Create Virtio Device From the Resource Table Vdev Resource, and Add It to the Remoteproc Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_create_virtio
   :project: openamp_doc_embed

Remove Virtio Device From the Remoteproc Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doxygenfunction:: remoteproc_remove_virtio
   :project: openamp_doc_embed
