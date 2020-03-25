"""Viewlets for eea.plonebuildout.profile
"""
import os
import logging
import requests
import contextlib
from time import time

from Products.CMFCore.utils import getToolByName
from distutils.version import StrictVersion
from eea.plonebuildout.profile.browser.utils import REQUIRED_PKGS
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram

from zope.component import getUtility
from eea.plonebuildout.profile.controlpanel.manifest_json import IManifestJsonSettings
from plone import api
from plone.registry.interfaces import IRegistry

logger = logging.getLogger('eea.plonebuildout.profile')
EEA_KGS_URL = "https://api.github.com/repos/eea/eea.docker.kgs/tags"
READ_TIMEOUT = 3.0
CONNECT_TIMEOUT = 3.0


class NewReleaseViewlet(ViewletBase):
    """A viewlet which informs managers of new EEA KGS releases
    """

    def current_kgs_version(self):
        """ Get current KGS version running on
        """
        return os.environ.get("EEA_KGS_VERSION", '')

    #we cache the result for 24 hours
    @ram.cache(lambda *args:time() // (60*60*24))
    def last_kgs_update(self):
        """Return a version number if running old KGS version, otherwise None
        """

        kgsver = self.current_kgs_version()
        if not kgsver:
            logger.warn("EEA_KGS_VERSION is not defined as environment "
                        "variable. Please use proper buildout configuration")
            return ''

        with contextlib.closing(requests.get(EEA_KGS_URL)) as conn:
            tags = conn.json()
            if not (tags and isinstance(tags, list)):
                logger.warn("Could not retrive KGS version at %s", EEA_KGS_URL)
                return ''

            last = tags[0].get('name', None)
            try:
                if StrictVersion(last) > StrictVersion(kgsver):
                    return last
            except (ValueError, AttributeError):
                if last != kgsver:
                    return last
        return ''


class RequiredPkgsViewlet(ViewletBase):
    """ A viewlet which displays a warning about missing required packages
    """

    def get_missing_packages(self):
        """ Return a list of missing required packages
        """
        missing = {}
        available_pkgs = []
        installed_pkgs = []
        qi = getToolByName(self.context, 'portal_quickinstaller')
        prods = qi.listInstallableProducts(skipInstalled=False)

        for prod in prods:
            pkg_id = prod.get('id')
            if prod.get('status') == 'installed':
                installed_pkgs.append(pkg_id)
            else:
                available_pkgs.append(pkg_id)

        for pkg in REQUIRED_PKGS:
            pkg_id = pkg.get('pkg_id')
            if pkg_id not in installed_pkgs:
                if pkg_id not in available_pkgs:
                    try:
                        __import__(pkg_id)
                    except ImportError:
                        missing_pkg = pkg.copy()
                        missing_pkg['available'] = False
                        missing[pkg_id] = missing_pkg
                else:
                        missing_pkg = pkg.copy()
                        missing_pkg['available'] = True
                        missing[pkg_id] = missing_pkg

        return missing

class ManifestJsonViewlet(ViewletBase):
    def get_manifest_json_settings(self):
        """ Return the settings as set in site/@@pwa-controlpanel

            Usage: s.name
        """
        registry = getUtility(IRegistry, context=api.portal.get())
        s = registry.forInterface(IManifestJsonSettings)
        return s

    def get_theme_color(self):
        settings = self.get_manifest_json_settings()
        return settings.theme_color
