.. _inter-process-reference-label:

===================================
Running Demos as Processes on Linux
===================================

The `OpenAMP project examples <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples>`_
are intended to execute on the remote of a reference board but can also be demonstrated by
implementing as a process on the main controller, effectively emulating a remote.

This can be useful for demonstration purposes, but can also be leveraged for component testing, even
as part of a continuous integration setup.

Effectively the `OpenAMP Library <https://github.com/OpenAMP/open-amp/tree/main/lib>`_ and
`reference examples <https://github.com/OpenAMP/open-amp/tree/main/apps/examples>`_ are built for
the main controller system along with the
`main controller examples <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples/linux>`_.

To build and execute on a Linux system, refer to the
`example to compile OpenAMP for communication between Linux processes <https://github.com/OpenAMP/open-amp/blob/main/README.md#example-to-compile-openamp-for-communication-between-linux-processes>`_.
