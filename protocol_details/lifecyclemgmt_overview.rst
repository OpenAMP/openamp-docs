============
LCM Overview
============

The remoteproc APIs provide life cycle management of remote processors by performing five essential
functions.

    - Allow the host software applications to load the code and data sections of the remote firmware
      image to appropriate locations in memory for in-place execution
    - Release the remote processor from reset to start execution of the remote firmware
    - Establish RPMsg communication channels for runtime communications with the remote context
    - Shut down the remote software context and processor when its services are not needed
    - Provide an API for use in the remote application context that allows the remote applications
      to seamlessly initialize the remoteproc system and establish communication channels with the
      host context

The remoteproc component currently supports Executable and Linkable Format (ELF) for the remote
firmware; however, the framework can be easily extended to support other image formats. The remote
firmware image publishes the system resources it requires to remoteproc on the host using a
statically linked resource table data structure. The resource table data structure contains entries
that define the system resources required by the remote firmware (for example, contiguous memory
carve-outs required by remote firmware’s code and data sections), and features/functionality
supported by the remote firmware (like virtio devices and their configuration information required
for RPMsg-based IPC).

The remoteproc APIs on the host processor use the information published through the firmware
resource table to allocate appropriate system resources and to create virtio devices for IPC with
the remote software context. The following figure illustrates the resource table usage.

.. image:: ../images/lcm.jpg

When the application on the host calls to the remoteproc_init API, it performs the following:

    - Causes remoteproc to fetch the firmware ELF image and decode it
    - Obtains the resource table and parses it to handle entries
    - Carves out memory for remote firmware before creating virtio devices for communications with
      remote context

The host application then performs the following actions:

    1. Calls the remoteproc_boot API to boot the remote context
    2. Locates the code and data sections of the remote firmware image
    3. Releases the remote processor to start execution of the remote firmware.

After the remote application is running on the remote processor, the remote application calls the
remoteproc_resource_init API to create the virtio/RPMsg devices required for IPC with the host
context. Invocation of this API causes remoteproc on the remote context to use the rpmsg name
service announcement feature to advertise the rpmsg channels served by the remote application.

The host receives the advertisement messages and performs the following tasks:

    1. Invokes the channel created callback registered by the host application
    2. Responds to remote context with a name service acknowledgement message

After the acknowledgement is received from host, remoteproc on the remote side invokes the RPMsg
channel-created callback registered by the remote application. The RPMsg channel is established at
this point. All RPMsg APIs can be used subsequently on both sides for runtime communications between
the host and remote software contexts.

To shut down the remote processor/firmware, the remoteproc_shutdown API is to be used from the host
context. Invoking this API with the desired remoteproc instance handle asynchronously shuts down the
remote processor. Using this API directly does not allow for graceful shutdown of remote context.

Gracefully bringing down the remote context is not part of the remoteproc LCM, but can be
implemented by the applications using the following steps:

    1. The host application sends an application-specific shutdown message to the remote context
    2. The remote application cleans up application resources, sends a shutdown acknowledge to host,
       and invokes remoteproc_resource_deinit API to deinitialize remoteproc on the remote side.
    3. On receiving the shutdown acknowledge message, the host application invokes the
       remoteproc_shutdown API to shut down the remote processor and de-initialize remoteproc using
       remoteproc_deinit on its side.

The OpenAMP samples and demos exemplify the use of an application specific message to perform
graceful shutdown before the hard remoteproc_shutdown is performed. For an example, see the Shutdown
Packet in the `Echo Test Messaging Flow diagram<echo-test-control-flow>` which is implemented as the
SHUTDOWN_MSG in the source
`open-amp Repository <https://github.com/OpenAMP/openamp-system-reference/blob/main/examples/legacy_apps/examples/echo/rpmsg-echo.c>`_.
