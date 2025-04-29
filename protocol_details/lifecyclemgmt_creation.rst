=====================================================
Creation and Boot of Remote Firmware Using remoteproc
=====================================================

You can create and boot remote firmware for Linux, RTOS, and bare metal-based remote applications
using remoteproc. The following procedure provides general steps for creating and executing remote
firmware on a supported platform.

The following figure illustrates the remote firmware creation process.

.. image:: ../images/lcm_boot.jpg

Defining the Resource Table and Creating the Remote ELF Image
-------------------------------------------------------------

Creating a remote image through remoteproc begins by defining the resource table and creating the
remote ELF image.

Procedure
~~~~~~~~~

  1. Define the :ref:`resource table<resource-table>` structure in the application. The resource
     table must minimally contain carve-out and VirtIO device information for IPC.

  As an example, please refer to the resource table defined in the bare metal remote echo test
  application at
  `rsc_table.c <https://github.com/OpenAMP/open-amp/blob/main/apps/machine/zynqmp_r5/rsc_table.c>`_.
  The resource table contains entries for memory carve-out and virtio device resources. The memory
  carve-out entry contains info like firmware ELF image start address and size. The virtio device
  resource contains virtio device features, vring addresses, size, and alignment information. The
  resource table data structure is placed in the resource table section of remote firmware ELF
  image using compiler directives.

  2. After defining the resource table and creating the OpenAMP Framework library, link the
     remote application with the RTOS or bare metal library and the OpenAMP Framework library to
     create a remote firmware ELF image capable of in-place execution from its pre-determined memory
     region. (The pre-determined memory region is determined according to guidelines provided by
     section.)

  3. For remote Linux, step 1 describes modifications to be made to the resource table. The
     previous flow figures shows the high level steps involved in creation of the remote Linux
     firmware image. The flow shows to create a Linux Flat Image Tree (FIT) image that encapsulates
     the Linux kernel image, Device Tree Blob (DTB), and initramfs.

  The user applications and kernel drivers required on the remote Linux context could be built
  into the initramfs or moved to the remote root file system as needed after boot. The FIT image
  is linked along with a boot strap package provided within the OpenAMP Framework. The bootstrap
  implements the functionality required to decode the FIT image (using libfdt), uncompress the
  Linux kernel image (using zlib) and locate the kernel image, initramfs, and DTB in RAM. It can
  also set up the ARM general purpose registers with arguments to boot Linux, and transfer control
  to the Linux entry point.

Making Remote Firmware Accessible to the Host
-----------------------------------------------

After creating the remote firmware’s ELF image, you need to make it accessible to remoteproc in the
host context.

Procedure
~~~~~~~~~

  1. If the RTOS- or bare metal-based host software context has a file system, place this firmware
     ELF image in the file system.
  2. Implement the remoteproc APIs to load the remote firmware.
  3. For AMP use cases with Linux as host, place the firmware application in the root file system
     for use by Linux remoteproc platform drivers.

In the OpenAMP Framework reference port to Zynq ZC702EVK, the bare metal library used by the host
software applications does not include a file system. Therefore, the remote image is packaged along
with the host ELF image. The remote ELF image is converted to an object file using “objcopy”
available in the “GCC bin-utils”. This object file is further linked with the host ELF image.

The remoteproc component on the host uses the start and end symbols from the remote object files to
get the remote ELF image base and size.

You can now use the remoteproc APIs.
