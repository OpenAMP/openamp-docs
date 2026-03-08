.. OpenAMP documentation master file, created by
   sphinx-quickstart on Wed Oct  5 10:21:26 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the OpenAMP Project Documentation
============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   openamp/index
   demos/index
   demos/reference_boards
   tools/index
   protocol_details/index
   docs/porting_guide
   openamp/glossary


..
  TOC entries used to suppress warnings we accept for files not included in a table of contents.
  WARNING: document isn't included in any toctree [toc.not_included]
  Note that each library's (e.g. open-amp) readme file is included via the REFERENCE section links
  in the navigation bar on the left.

.. toctree::
   :hidden:

   README
   openamp-system-reference/README
   openamp-system-reference/LICENSE
   openamp-docs/README
   open-amp/.github/actions/build_ci/README
   open-amp/README
   open-amp/LICENSE
   libmetal/.github/actions/build_ci/README
   libmetal/README
   libmetal/LICENSE

..
  TOC entries for examples which do not have readthedocs descriptions so suppressing to avoid the
  warning:
  WARNING: document isn't included in any toctree [toc.not_included]
  If readthedocs description is added, these should be integrated into that description.

.. toctree::
   :hidden:

   openamp-system-reference/examples/legacy_apps/examples/nocopy_echo/README
   openamp-system-reference/examples/legacy_apps/examples/rpmsg_sample_echo/README
   openamp-system-reference/examples/libmetal/README
   openamp-system-reference/examples/libmetal/demos/irq_shmem_demo/README
   openamp-system-reference/examples/libmetal/demos/irq_shmem_demo/host/README
   openamp-system-reference/examples/libmetal/demos/irq_shmem_demo/remote/README
   openamp-system-reference/examples/zephyr/dual_qemu_ivshmem/README
