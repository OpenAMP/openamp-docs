.. _openamp-maintenance-work-label:

===================================
Contributing to the OpenAMP Project
===================================

Release Cycle
-------------
- 6 month release cycle aligned with Ubuntu (xx.04 and xx.10)
- (feature freeze) release branch cut 1 month before release target
- Maintainence releases are left open-ended for now

Roadmap discussion and publication
----------------------------------
- Feature freeze period of a release used for roadmap discussions for next release
- Contributers propose features posted and discussed on mailing list
- Maintainer collects accepted proposals
- Maintainer posts list of development tasks, owners, at open of release cycle

Patch process
-------------
- Patches posted on the mailing list for review
- Pull request on github once review cycles are complete
- Maintainer ensures a minimum of 1 week review window prior to merge

Platform maintainers
--------------------
- Platform code refers to sections of code that apply to specific vendor's hardware or operating system platform
- Platform maintainers represent OS or hardware platform's interests in the community
- Every supported OS or hardware platform must have a platform maintainer (via addition to MAINTAINERS file in code base), or patches may not be merged.
- Support for an OS or hardware platform may be removed from the code base if the platform maintainer is non-responsive for more than 2 release cycles
- Responsible for verification and providing feedback on posted patches
- Responsible to ACK platform support for releases (No ACK => platform not supported in the release)

Push rights
-----------
- Push rights restricted to the Core Team
- Generally exercised by the maintainers for each repository
- Maintainers manage delegation between themselves
