.. _asymmetric-multiprocessing-work-label:

================================
Asymmetric Multiprocessing Intro
================================

An embedded AMP system is characterized by multiple homogeneous and/or heterogeneous processing cores integrated into one System-on-a-Chip (SoC). Examples include:

    - The Xilinx MPSoC that has four ARM Cortex-A53, two ARM Cortex-R5, and potentially a number of MicroBlaze cores.
    - The NXP i.MX6SoloX/i.MX7d SoCs that utilizes ARM Cortex-A9 and ARM Cortex-M4F cores
    - The Texas Instruments TI AM57x SoCs that have dual ARM Cortex A15, dual ARM Cortex M4, and C66x DSP cores.

These cores typically run independent instances of homogeneous and/or heterogeneous software environments, such as Linux, RTOS, and Bare Metal that work together to achieve the design goals of the end application. While Symmetric Multiprocessing (SMP) operating systems allow load balancing of application workload across homogeneous processors present in such AMP SoCs, asymmetric multiprocessing design paradigms are required to leverage parallelism from the heterogeneous cores present in the system.

Increasingly, today’s multicore applications require heterogeneous processing power. Heterogeneous multicore SoCs often have one or more general purpose CPUs (for example, dual ARM Cortex A9 cores on Xilinx Zynq) with DSPs and/or smaller CPUs and/or soft IP (on SoCs such as Xilinx Zynq MPSOC). These specialized CPUs, as compared to the general purpose CPUs, are typically dedicated for demand-driven offload of specialized application functionality to achieve maximum system performance. Systems developed using these types of SoCs, characterized by heterogeneity in both hardware and software, are generally termed as AMP systems.

Other reasons to run heterogeneous software environments (e.g. multi-OS) include:

    - Needs for multiple environments with different characteristics
        * Real-time (RTOS) and general purpose (i.e. Linux)
        * Safe/Secure environment and regular environment
        * GPL and non-GPL environments
    - Integration of code written for multiple environments
        * Legacy OS and new OS

In AMP systems, it is typical for software running on a master to bring up software/firmware contexts on a remote on a demand-driven basis and communicate with them using IPC mechanisms to offload work during run time. The participating master and remote processors may be homogeneous or heterogeneous in nature.

A master is defined as the CPU/software that is booted first and is responsible for managing other CPUs and their software contexts present in an AMP system. A remote is defined as the CPU/software context managed by the master software context present.