.. _resource-table:

==============
Resource Table
==============

Overview
********

The resource table is a key part of resource assignment of remoteproc life cycle management.

The table consists of a header detailing a version, number of resource entries and an array pointing
at the offset location of each entry. Directly following the header are the resource entries
themselves, each of which has a 32 bit type. These in remote context will likely be memory carveouts
for locations of parts of the remote system and virtio device definitions.


+--------------+--------------------------------------------------------------------------------+
|     Item     |                                  Description                                   |
+==============+================================================================================+
| ver          | RemoteProc version number                                                      |
+--------------+--------------------------------------------------------------------------------+
| num          | Number of resource entries following the header                                |
+--------------+--------------------------------------------------------------------------------+
| reserved     | Unused but should be set to zero until used                                    |
+--------------+--------------------------------------------------------------------------------+
| offset       | Array of values pointing to the offset location of each resource entry         |
+--------------+--------------------------------------------------------------------------------+
| resources    | Structures which define each of the resource entries (up to num count), at     |
|              | given offset, with each starting with a type (fw_resource_type) so the parser  |
|              | can correctly extract the information.                                         |
+--------------+--------------------------------------------------------------------------------+

The resource table is effectively a list of resource definitions, with each entry detailed by the
corresponding :ref:`resource structure<resource-structure>`, and the Remoteproc framework
is responsible for configuring the resources need by the remote processor (shared memory, trace
buffers, vendor specific resources).

The possible resource types are defined in the
`Remoteproc Header <https://github.com/OpenAMP/open-amp/blob/main/lib/include/openamp/remoteproc.h>`_
and detailed in the :ref:`resource-types` section below.


Compatibility with Linux kernel
-------------------------------

With Linux being a key full stack operating system in the embedded devices space, the resource
table should maintain compatibility with that of
`Linux Remoteproc <https://www.kernel.org/doc/html/latest/staging/remoteproc.html>`_.

::

   Evolution should be done in cooperation with Linux remoteproc community.

Related documentation can be found under the Linux kernel's remoteproc documentation:
`Binary Firmware Structure <https://www.kernel.org/doc/html/latest/staging/remoteproc.html#binary-firmware-structure>`_.


.. _resource-types:

Resource Types
**************

Each of the resources in the :ref:`resource-table` is defined by a type (fw_resource_type) and
its corresponding :ref:`structure<resource-structure>`.

.. doxygenenum:: fw_resource_type
   :project: openamp_doc_embed


.. _resource-structure:

Resource Structure Definitions
------------------------------

The following structures correspond to each of the :ref:`resource-types` (fw_resource_type).

.. doxygenstruct:: fw_rsc_carveout
   :project: openamp_doc_embed

.. doxygenstruct:: fw_rsc_devmem
   :project: openamp_doc_embed

.. doxygenstruct:: fw_rsc_trace
   :project: openamp_doc_embed

.. doxygenstruct:: fw_rsc_vdev
   :project: openamp_doc_embed


In addition to the predefined :ref:`resource-types` vendors can define their
own with types between RSC_VENDOR_START and RSC_VENDOR_END.

.. doxygenstruct:: fw_rsc_vendor
   :project: openamp_doc_embed
