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

The fw_resource_type's are listed in the
`remoteproc header <https://github.com/OpenAMP/open-amp/blob/main/lib/include/openamp/remoteproc.h>`_.

Compatibility with Linux kernel
-------------------------------

The resource table should maintain compatibility with that of
`remoteproc <https://www.kernel.org/doc/html/latest/staging/remoteproc.html>`_.

::

   Evolution should be done in cooperation with Linux remoteproc community.

Related documentation can be found under the Linux kernel's remoteproc documentation:
`Binary Firmware Structure <https://www.kernel.org/doc/html/latest/staging/remoteproc.html#binary-firmware-structure>`_.
