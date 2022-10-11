====================
Hardware Description
====================

Problems
--------

   - Need to communicate HW details (addresses, topologies, …) to SW subsystems during build
      * Both at system level (complete HW including all CPUs) and subsystem level
      * Tool to create subsystems with assigned devices out of system level info
   - Need to communicate HW details during runtime
      * Device trees used by Linux, Xen, etc.
      * How to communicate to coprocessors (remoteproc) what devices it has?
   - Need tools to create static config data (#defines, .h, .c files) from HW description
      * Zephyr working on this. Need general solution.
   - Need compact format for runtime use cases
      * DTB is not very compact. Using strings instead of labels, no compression

Potential solutions
-------------------

   - Come up with standard, humanly readable, HW description format for usage during build
      * Possible candidates include extended Device Trees, IPExact, …
      * A “System Level Device Tree” would add another level with multiple CPUs and mappings
   - Come up with standard compressed HW description
      * Potential candidate is CBOR

Others interested in this problem?
----------------------------------