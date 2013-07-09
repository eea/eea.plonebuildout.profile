Introduction
============

This product is a simple Plone profile that depends on all EEA core 
packages. Its purpose is to enable simple instalation of those packages,
to verify that they work and install properly in a simple Plone site.

Also, it provides a viewlet, visible only to managers, placed just above the
content title in regular pages, that informs if a new EEA KGS version is
available. This viewlet uses github to retrieve the latest available KGS and
caches this information for one hour. To get rid of of this information you'll
have to either disable the viewlet or upgrade to the latest EEA KGS.
