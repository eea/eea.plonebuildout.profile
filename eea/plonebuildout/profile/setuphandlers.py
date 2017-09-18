""" Various setup
"""
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
try:
    from plone.app import ldap
except ImportError:
    ldap = None


def setupLDAP():
    """ Various setup for LDAP
    """
    site = getSite()
    stool = getToolByName(site, "portal_properties").site_properties
    stool.manage_changeProperties(many_groups=True, many_users=True)

    st = getToolByName(site, "portal_setup")
    st.runAllImportStepsFromProfile("profile-eea.plonebuildout.profile:ldap")


def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eeaplonebuildout.txt') is None:
        return

    # LDAP support is available
    if ldap is not None:
        setupLDAP()
