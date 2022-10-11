============================
System Device Tree Sub-Group
============================

Introduction
------------

Todays heterogeneous SoCs are very hard to configure. Issues like which cores, memory and devices belongs to which operating systems, hypervisors and firmware is done in an ad-hoc, error prone way. System Device Trees will change all that by extending todays device trees, used by Linux, Xen, uboot, etc. to describe the full system and also include configuration information on what belongs where.

Communications
--------------
Mailing list
~~~~~~~~~~~~

We have a Mailman list for system-dt discussions. You can find info about it, reach the link to the archives, and subscribe/unsubscribe `here <https://lists.openampproject.org/mailman3/lists/system-dt.lists.openampproject.org/>`_

Meetings
~~~~~~~~

Check out the meeting notes for the System Device Tree meetings on the :ref:`OpenAMP Meeting Notes page<meeting-notes-work-label>`.

Documentation
-------------
System DT intro presentation given at Linaro Connect SAN19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    - `Video <https://www.youtube.com/watch?v=n6NYRYdOIJU>`_
    - `Slides <https://connect.linaro.org/resources/san19/san19-115/>`_

Placeholder for Stefano to populate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Placeholder for other documentation here

Lopper
~~~~~~

Lopper is a device tree manipulation tool that has been created to provide data driven manipulation and transformation of System Device Trees into any number of output formats, with an emphasis on conversion to standard device trees.

The source code and information can be found at: https://github.com/devicetree-org/lopper/

Future work
-----------

Check out the future work list for the System Device Tree sub-group in the :ref:`future-device-tree-work-label` section