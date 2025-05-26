.. _rpmsg-protocol-work-label:

=========================================================
Inter Process Communications (IPC) through RPMsg Protocol
=========================================================

In asymmetric multiprocessor systems, the most common way for different cores to cooperate is to
use a shared memory-based communication. There are many custom implementations, which means that
the considered systems cannot be directly interconnected. Therefore, OpenAMP's aim is to offer a
standardization of this communication based on existing components (RPMsg, VirtIO).

OpenAMP's implementation of RPMsg is through shared memory utlizing a ring buffer, with optional
inter-core interrupts, using Virtio devices as the system level abstraction layer.


.. toctree::
   :maxdepth: 2

   rpmsg_protocol
   rpmsg_comms
