=============================================
Inclusive Language and Biased Terms Sub-Group
=============================================

This proposal from Bill Mills was approved at the 10/22/21 OpenAMP TSC:

replace master with main
------------------------

github has special case logic to make this easier: https://github.com/github/renaming

remoteproc context
------------------

    - "slave" should be "remote processor"
    - "master" should be "remoteproc host"

virto context
-------------

virtio spec uses "device" and "driver". suggest we use "virtio device" and "virtio driver"

Examples of devices:

    - vitioblk device
    - virtio network interface

For today's remoteproc rpmsg, Linux is always the driver side.

Some virtio "devices" are not very device like and instead are more like services. Alternative for such cases

    - "application service" and "application client"

Examples:

    - vsock: service is the one that calls accept on the socket
    - p9fs: service is the side that has the filesystem

Note that a remote processor can host a service and be a client at the same time. The terminology is per service.