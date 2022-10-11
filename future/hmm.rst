=====================================
HMM (Heterogeneous Memory Management)
=====================================

Use Cases
---------

   - pcie/ccix endpoint side memory pools
   - embedded soc e.g. dedicated media buffer alloc pool

zone device and memory hotplug (on arm64)
-----------------------------------------

   - arch pte devmap bit options (mair bits, pte_none?, pte_special?)
   - device pluggable private and public memory

hmm address space mirroring w/ rproc
------------------------------------

   - tie into vfio-map shmem model w/ remoteproc instances?
   - could we somehow do better than dma migration w/ pgtable remapping?
   - (opt.) tie into vfio-bind shmem model needs intg. iommu fault handling
