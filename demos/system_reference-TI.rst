.. _reference_board_TI:

==================================
Texas Instruments Reference Boards
==================================

A number of the `OpenAMP project examples <https://github.com/OpenAMP/openamp-system-reference/tree/main/examples>`_ can be executed on TI Reference boards.

The `Zephyr <https://www.zephyrproject.org/>`_ demo `OpenAMP using resource table <https://docs.zephyrproject.org/latest/samples/subsys/ipc/openamp_rsc_table/README.html>`_ can be built for the following boards:

.. csv-table::
   :header: "Board", "Zephyr Identifier", "Deploy Firmware Name"
   :widths: 50, 50, 50

    `TI SK-AM64B <https://www.ti.com/tool/SK-AM64B>`_, ``sk_am64/am6442/m4``, ``am64-mcu-m4f0_0-fw``
    `BeagleBoard PocketBeagle 2 <https://www.beagleboard.org/boards/pocketbeagle-2>`_, ``pocketbeagle_2/am6232/m4``, ``am62-mcu-m4f0_0-fw``

Use the Zephyr `Getting Started Guide <https://docs.zephyrproject.org/latest/develop/getting_started/index.html>`_ to setup the build environment. Then build the OpenAMP example firmware with:

.. code-block:: console

   west build -p -b <Zephyr Identifier> samples/subsys/ipc/openamp_rsc_table

This will produce a firmware named ``zephyr_openamp_rsc_table.elf`` which can be deployed to the board. Then copy or symlink it to the expected name in the firmware directory:

.. code-block:: console

   ln -s zephyr_openamp_rsc_table.elf /lib/firmware/<Deploy Firmware Name>

Either restart the board so the kernel can load it on boot, or restart the remote processor manually:

.. code-block:: console

   # check remote processor state
   cat /sys/class/remoteproc/remoteproc0/state

   # Stop remote processor if running
   echo stop > /sys/class/remoteproc/remoteproc0/state

   # Load and start target firmware onto remote processor
   echo start > /sys/class/remoteproc/remoteproc0/state

.. note::

   The remote processor number (remoteproc0) may be different depending on driver probe order. To check which remote processor the number belongs to print out the default firmware name (:code:`cat /sys/class/remoteproc/remoteproc0/firmware`) and match that to the ``Deploy Firmware Name`` above.
