==============
Resource Table
==============

Overview
********

The resource table is a key part of resource assignment of remoteproc life cycle management.

Needs
*****

Compatibility with Linux kernel
-------------------------------

::

   The evolution should be done in cooperation with Linux remoteproc community.

Review current resource table fields
------------------------------------

Review the current version resource table to confirm fields relevance (e.g name fields). The aim is to keep resource table as small as possible...

64 bit addresses
----------------

Parameter passing
-----------------

In order to pass parameters to the remote application, it could be useful to have a new resource type for that.

Evolutive virtio dev features
-----------------------------

Currently, field for virtio dev features is 32 bits in rsc table. However, some virtio dev now have bits > 32 bit.

Pointer to Device Tree
----------------------

vdev buffer management
----------------------

   - Add possibility to provide DA to fix the vdev buffers memory region and size ( carveout?)
   - Allow to specify the size of the buffers, depending on the direction.

Trace evolution
---------------

Improve the trace mechanism to increase depth.

Enhancement
***********

To confirm a need...

Define resource table ownership
-------------------------------

The resource table has to be managed by only one core, the master. To break the master slave relationship, a field that define the ownership of the resource table, could be added

Include the resource table size
-------------------------------

Add size information in header to avoid to parse the whole resource table to retrieve the length (memory allocation/mapping)

New resource to provide processors states
-----------------------------------------

Add resource that defines a structure to share the processor states. This can be used by some systems to manage low power and crash mechanisms.

Mechanisms
**********

Discussion of how the add the new capabilities to the resource table while providing back and forward compatibility.

Resource table version number
-----------------------------

The existing resource table definition has a version number. This number could be incremented for a new format.

The issue with the method is that it is all or nothing and does not allow new firmware to be used with an old kernel.

clementleger: IMHO, this is not a real "issue", if new firmware requires new capabilities in resource table, then it will use the new format and expect a master that support such features. If the firmware does not need them, then it will stick with old format. Having a backward compatibility seems mandatory however a forward compatibility seems really limitating.

Multiple resource tables of different versions could be included but this is rather bulky and awkward and a new method would need to be defined for marking and locating the various versions.

Per item version number
-----------------------

Resource table item IDs are currently 32 bits. It has been suggested that this is a very large range for this purpose. One idea would be to subdivide the 32 bits into fields and designate some bits to be an item type specific version number.

clementleger: This is a bit clunky. If we are modifying the resource table, it would be better to add a new field to handled such cases. Actually, all resources have reserved fields. IMHO, these fields should be used for versionning if using a new version (they were currently 0) so they are well suited to be used as a versionning field. But this probably be discussed on the mailing list. the vdev_vring resources are tied to rsc_vdev so it will mosty probably be used in conjunction with them and the versionning of vdev_rsc will apply to them.

This would allow multiple versions of the same type to be included in the resourse table and the kernel could look for the greatest version that it understands. The bit fields makes this logic easier than if unrelated 32 bit values were used.

Per item Priority
-----------------

Item ID bit fields could also/instead be used to define what a consumer should do it if does not understand the Item ID. A priority of "optional" means that the consumer can ignore the Item if it does not understand it and a priority of "required" means that the consumer should refuse to load firmware that contains this item ID. Other priorities might be defined but at least these two would make sense.

vdev buffer management
----------------------

Should we add a new resource tied to the vdev one to define a DA and buffer size? Do we need to define independent memory region for both direction (P2P)? Buffer size and number of buffers should depend on the direction.

Traces
------

The existing tracing mechanism is relying on a circular buffer. The depth of the trace is the size of the buffer as no mechanism exists to extract the traces before overflow. Proposal is to implement trace extraction based on a flip flop buffer with notifications (mailbox notifyID). This would allow the main processor to extract the traces in time to fill its own logs buffer/file. The Impact in the resource table would be a new resource structure or the addition of a “trace method” field in existing resource structure.

Firmware publishes multiple versions of Resource table
------------------------------------------------------

TODO