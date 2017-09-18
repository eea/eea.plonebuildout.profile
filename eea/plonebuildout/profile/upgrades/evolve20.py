""" Upgrade scripts to version 2.0
"""
import logging
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from eea.plonebuildout.profile.setuphandlers import ldap
from eea.plonebuildout.profile.setuphandlers import setupLDAP
logger = logging.getLogger('eea.plonebuildout.profile')

def migrate2plone_app_ldap(context):
    """ Fix comments without id and creation date
    """
    if ldap is None:
        logger.warn("plone.app.ldap not present. Nothing to migrate.")
        return "plone.app.ldap not present. Nothing to migrate."

    site = getSite()
    acl_users = getToolByName(site, 'acl_users')
    old = [oid for oid in acl_users.objectIds('LDAP Multi Plugin')
                       if oid.startswith('EIONET')]
    if old:
        logger.warn("Removing old LDAP Multi Plugins: %s", ", ".join(old))
        acl_users.manage_delObjects(old)

    logger.info("Installing plone.app.ldap and configure EIONET LDAP")
    setupLDAP()
    return (
        "Installed plone.app.ldap and configured it with the default "
        "EIONET LDAP settings."
    )
