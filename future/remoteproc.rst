.. _future-remoteproc-work-label:

================================
Remoteproc Sub-Group Future Work
================================

This list (needs update) covers topics for the "OpenAMP remoteproc" sub-group to discuss and work on. This sub-group covers areas such as remoteproc, rpmessage, virtio, big buffers, etc.

The sections below should include an short abstract and links to prior discussion etc. More detailed information should be added on a new wiki page and a link to that page should be added to the topic here.

HW description (Xilinx, TI, ST, Mentor)
---------------------------------------

   - How to describe HW to System SW – Complete HW vs. OS centric subsystems – DT, IPExact. More info can be found here.
   - Q: 2019/11/7, Is this the same as SystemDT and should be moved to that group, or are there rp specific topics?

System Resource Management – (ST, Xilinx, TI, Cypress)
------------------------------------------------------

   - How to configure and assign resources and peripherals to coprocessors
   - Complications include clock and power domain control, system firewall and/or IOMMU configuration
   - Some of this gets easier if both Linux and the remote processor are using a central system controller for clock. power, and peripheral access control like SCMI or TISCI

OpenAMP project support for Virtio spec (Xilinx, TI, ST, Mentor)
----------------------------------------------------------------

   - Packed vrings, indirect descriptors, …
   - Virtio device handshake improvements
   - Use of existing virtio drivers (ex: virtblk, virtnet, virtcon) from remoteprocs
      * remoteproc could be frontend or backend (ex:could be the block user or block device)
      * Q: 2019/10/7, should this be its own topic and leave this one to be just virtio mechanics?

Remoteproc Virtio driver
------------------------

Remoteproc framework is covering coprocessor management (init, load, start, stop, crash, dump...), but also provides functions for vring support. That complicates the device management, mainly the parent/child relation and the memory region assignment. Idea is to create a virtrproc like virtmem or virtcon and rely on DT definition for driver probing.

   - ST has some patches to share

Big data – (Xilinx, TI, ST)
---------------------------

   - Rpmsg buffer management
   - Zero copy and big buffer
   - Heterogeneous Memory Management. More info can be found here BROKEN LINK
   - libmetal shared memory allocation: https://github.com/OpenAMP/libmetal/issues/70
   - sub topics include allocation, mapping, IOMMU, remoteproc MMU, cache maintenance, address translation
   - DMA-BUF heaps seems to be the obvious choice for allocation API now

Kernel remoteproc CI patches - Loic
-----------------------------------

The rate of remoteproc/rpmsg patch review/acceptance seems slow, what can we do to accelerate it? This page has a lot of stuff (and there is a lot more waiting as 2nd tier of features). (This is not about maintainer bashing; it is about working better together.)

   - more mailing list discussion
      * patch review should be done on kernel rpmsg list not openamp-rp list
      * openamp-rp list can be used for broader arch discussion and Linux/RTOS interaction
   - more reviewed by/acked by/tested by cooperation
   - remoteproc CI loop should help

OpenAMP kernel staging tree - Bill
----------------------------------

   - Create an OpenAMP github repo for linux to collect all carried and WIP patches in one place
   - This is not to create a product, it is to more easily see what problem everyone is working around
   - Suggestion is to have a branch per vendor where they collect all the remoteproc related patches as a rebase branch
   - Extra: Some have suggested trying to merge all the vendor work together ahead of getting to mainline
      * However this step seems controversial, lets not focus on that, at least for now
   - Alternative: just collect a list of links to the vendor trees
      * This is definitely easier but it can be a lot of work to find the relevant patches

Remoteproc/rpmsg CI & regression test – (Xilinx, TI, ST)
--------------------------------------------------------

Create a CI environment that can build both RTOS and Linux side and test existing and new operations.

   - QEMU based AMP SOC highly desired as target
   - Should be usable in cloud CI (travis etc) and on individual developers desktop
   - V0.1: Start with QEMU fork and any publicly reproducible build
   - V1: Add build flow for easy developer mode
   - Expand to board farm as second phase
   - Nice to have: use upstream QEMU

There is a Docker container (work in process), that runs an instance of Xilinx QEMU that supports up to 4 A-53 cores and 2 R5 cores. This boots Linux, loads the firmware into the R5 via remoteproc, and can run the OpenAMP rpmsg echo test. https://hub.docker.com/repository/docker/edmooring/qemu

Secure coprocessor support – Loic
---------------------------------

Add a generic rproc driver to support secure and isolated coprocessor thanks to some trusted services based on OPTEE or other Trusted OS. Standard flow will be to load coprocessor firmware and its associated signature somewhere in secure/non-secure shared memory and then to request secure world to load, authenticate coprocessor image and then start coprocessor Some tasks:

   - Define a standard file format for firmware to authenticate (is ELF still relevant or should we rely on PKCS11 header like to integrate signature ?)
   - Define TA API to control secure coprocessor (load, start, stop...)
   - How to manage resource table in that case? Should we rely on some secure services or should we consider it as input for communication link (aka rpmsg) configuration between coprocessor and Linux kernel (and in that case could stay non-secure)
   - Q: Can we make this generic enough to be used when coproessor is to be owned/trusted by a hypervisor instead of the secure world

Linux RPMSG only mode - Bill (TI,)
----------------------------------

RPMSG should be usable in the Linux kernel when Linux will never be the life-cycle manager for that coprocessor.

In many modern systems the Linux kernel is not the most trusted entity in the system. Sometimes a given coprocessor is loaded and managed by another entity that is more secure (ex: secure world), more safe (ex: dual lock-set R5), or more trusted (hypervisor). In these system Linux may never be the one that loads/starts/restarts/crash dumps the coprocessor but Linux still needs to use a rpmsg channel and perhaps other virtio based communication channels.

   - Need to tell remoteproc that it is not the controller
   - Need to find the resource table in use
   - remoteproc still needs to do: IOMMU mapping, PA to DA, etc
   - Q: Can we make a generic remoteproc that is usable for this case that can handle some (but not all) SOCs?
   - This model brings up many cases for robustness

RPMSG robustness - Bill (TI,ST)
-------------------------------

   - If coprocessor goes down and comes backup, Linux needs to recognize that and re-establish rpmsg communication
   - If Linux goes down (crash/shutdown) and restarts while the coprocessor stays running, coprocessor needs to recognize that and re-establisg rpmsg communication
   - The restart should be advertised to the applications not hidden from them. Applications should take recovery actions themselves.
      * On Linux this would probably mean an error code from the existing handle and a need to open a new one (or a issue a reset ioctl)

Early coprocessor boot – late attach, detach - Loic (ST,TI)
-----------------------------------------------------------

Late attach is different from rpmsg only mode in that once Linux comes up, it becomes the life cycle controller for the coprocessor.

   - Linux should have the option to stay with the firmware already loaded on the coprocessor.
   - Linux could later stop or reload the coprocessor with different firmware
   - Linux may take ownership of crashdump and debug logs
   - Late attach could require that matching firmware file exists in the filesystem, this would make finding the resource table easier
   - Or late attach could require to know where firmware resource table has previously been loaded as would be required in RPMSG only mode

Detach means that Linux stops becoming the life cycle owner. This could happen while Linux is running or as part of Linux crash/shutdown.

Early booted processor patch sent on ML: https://lore.kernel.org/patchwork/patch/1147726/

Lifecycle management and Trusted & Embedded Base Boot Requirement (T/E-BBR) – Etsam
-----------------------------------------------------------------------------------

Lifecycle management with Linux remote – Etsam
----------------------------------------------

The life cycle management of Linux is required in scenarios where it provides the rich execution environment and certified software environment (e.g on low end CPUs such as cortex M or R) is the system master and responsible to start/stop/recover Linux. The intent here is to cover the driver architecture (e.g. remoteproc replacement ) and device tree bindings for remote Linux. No plan to cover the Linux bootstrapping and RPMSG remote mode operation. They can be treated as separate topics. Linux will still assumed to be the RPMsg master.

Rpmsg protocol documentation for remote – Etsam
-----------------------------------------------

The RPMSG framework master side protocol is well manifested in Linux upstream and new masters (e.g. OpenAMP) can be written using it as a reference. However, there is no standard Doc/Implementation for remote which often leads to problematic protocol scenarios. For instance, consider the two cases below:

   - At what point VDEV Resource is initialized by the Master, specially when the vrings are dynamically allocated?
      * Conversely, at what point remote should access that vdev resource? Consider the case where vdev resource is accessed by the remote right after boot up, assumption here is that it is initialized by the master before starting the remote. This worked for kernel v3.18 , however, it is broken for v4.9 (may be for others as well) where the vring addresses are populated after remote is booted. For latter, this leads to race condition and sometimes remote ends up accessing uninitialized vdev resource. Apparently, the correct point to access vdev resource is after vdev status field (DRIVER_OK) is updated by the master. 
   - When to send the Name service announcement?
      * In response to first kick from the master: This works if remote is up and running. What if kick is sent and remote is not yet operational? It will miss the kick and consequently NS will not be sent.
      * In response to VDEV status update (DRIVER_OK). Will work if remote comes up after the first kick. The status will still be in the shared memory and can be used to send the NS.

The foolproof approach would be to use both kick and VDEV status to send the NS. This point was found after trial and error.

It is required to document all such scenarios i.e. all master actions and expected response from the remote, to enable seamless operation with different remotes.

MCU – MCU issues, rpsmg only - Mark
-----------------------------------

   - libopenamp example of rpmsg only
      * Does it exist, are there any remaining issues?
      * target for CI loop
      * how big is it? Measure as regression test
   - MCU boot first - late-attach
      * Crash recovery
   - Are there MISRA issues with libopenamp?
      * Is malloc required? Can this be easily mapped to something more static
   - "Big" Data in context of MCU to MCU (same SOC)
      * zero-copy?
   - OpenAMP improvement
      * Libmetal rework to be continued
      * Integrates last feedbacks coming from Nordic benchmark
      * Reduce memory footprint
      * Stack usage
   - rpmsg-lite: anything missing from libopenamp?

64 bits support - Clément
-------------------------

   - 64 bits support in elf file, see https://patchwork.kernel.org/patch/11175161/
      * Elf 64 files are needed for 64 bits processors
   - 64 bits addresses in resources table
      * Currently, addresses are only on 32bits, this is really limitating for 64bits 
   - 64 bits features in vdev declaration
      * Virtio Features are now using 64 bits. Without this support, we are tied to legacy 32bits features.
      * Need to switch to at least 64 bits and provisioned more bits for future evolution

Misc I/O over VirtIO/RPMSG - Loic, Bill
---------------------------------------

   - Put the "IO" in VirtIO
   - Virtual UART
      * ST has patches
      * should this be full UART control (baud rate, HW flow control, RI/DCE/DTE/CTS/RTS) or just a communication channel
      * Is Linux the device or the user?
      * example: MCU wants to send console messages to Linux for logging
      * example: MCU owns a physical UART but wants Linux to use it.
   - Virtual I2C
      * ST has some patches
      * exmaple: MCU owns phy I2C with multiple devices, presents virtual I2C for to Linux so it can use some but not all of the devices
   - Virtual SPI
      * ST has some patches
   - Virtual GPIO
   - Virtual register bank
      * via: regmap
      * Can be used on its own or as the base level of some of the above (GPIO seems obvious)
   - Should these be over RPMSG, direct over virtio, or both?

Reference: ST Presentation at ELC-E 2019, https://elinux.org/images/6/63/ELC_EU19_rpmsg.pdf

Improve Coprocessor debug capabilities - Loic
---------------------------------------------

Today rproc framework offers access to a virtual trace file (circular buffer filed by coprocessor) which limit coprocessor debug capabilities. Tracks to explore:

   - How to store coprocessor traces in a log file (syslog like) to improve trace depth?
   - How to get same timestamp between Linux and coprocessors to correlate trace
   - How to control coprocessor debug infrastructure (coresight?)
   - Is it possible to debug coprocessor firmware thanks to GDB/GDB server over rpmsg or mailbox?
   - How to avoid clashing with external JTAG debugger (RPMSG only mode may help here)

Past presentations and TODO lists
=================================

   - TI presentation on TODO list from 2017
      * https://github.com/OpenAMP/openamp.github.io/blob/master/docs/linaro-2017/OpenAMP-TI-Roadmap.pdf
   - ST presentation from 2018 on short term TODO list
      * https://github.com/OpenAMP/openamp.github.io/blob/master/docs/linaro-2018hkg/OpenAMP-short-term-topcis-st.pdf
   - Xilinx presentation from 2017 on Intro
      * https://github.com/OpenAMP/openamp.github.io/blob/master/docs/linaro-2017/OpenAMP-Intro-Feb-2017.pdf
   - TI presentation from 2018 on Big Data and robustness, IPC only and life cycle
      * https://github.com/OpenAMP/openamp.github.io/blob/master/docs/linaro-2018hkg/OpenAMP-Buffer-Exchange.pdf
   - TI presentation from 2017 on coprocessor memory types and howto handle
      * https://github.com/OpenAMP/openamp.github.io/blob/master/docs/linaro-2017/OpenAMP-memory-types.pdf
