"""Viewlets for eea.plonebuildout.profile
"""
import os
import logging
import requests
import contextlib
from time import time

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from copy import deepcopy
from distutils.version import StrictVersion
from eea.plonebuildout.profile.browser.utils import get_storage
from eea.plonebuildout.profile.browser.utils import REQUIRED_PKGS
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram

logger = logging.getLogger('eea.plonebuildout.profile')
EEA_ANALYTICS_URL = 'http://www.eea.europa.eu/@@eea.controlpaneleeacpbstatusagent.html'
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


class AnalyticsViewlet(ViewletBase):
    """A viewlet which stores the current requests hostname in a storage
    """
    def hostname_checkin(self):
        """ Store the current hostname and timestamp in the storage
        """
        storage = get_storage(self.context)
        hostnames = storage.get('hostnames', None)

        if hostnames is None:
            hostnames = storage['hostnames'] = {}

        hostname_list = self.get_hostname()
        if hostname_list is not None:
            for hostname in hostname_list:
                if not hostnames.get(hostname):
                    hostnames[hostname] = {'created': DateTime()}

                hosts = deepcopy(hostnames)
                last_ping = storage.get('last_ping')
                if last_ping:
                    last_ping_date = last_ping.get('date')
                    hostnames_checked = last_ping.get('hostnames')
                    success = last_ping.get('success')
                    new_hostname = hostname not in hostnames_checked.keys()
                    if success:
                        is_old = DateTime().greaterThan(last_ping_date+7)
                        if new_hostname or is_old:
                            self.do_ping(hosts, storage)
                    else:
                        is_old = DateTime().greaterThan(last_ping_date+1)
                        if is_old:
                            self.do_ping(hosts, storage)
                else:
                    self.do_ping(hosts, storage)

        return None

    def get_hostname(self):
        """ Extract hostname in virtual-host-safe manner
        """

        request = self.request
        result = []
        if "HTTP_X_FORWARDED_HOST" in request.environ:
            # Virtual host
            host = request.environ["HTTP_X_FORWARDED_HOST"]
        elif "HTTP_HOST" in request.environ:
            # Direct client request
            host = request.environ["HTTP_HOST"]
        else:
            return None

        # separate to domain name and port sections
        host_list = []
        host = host.split(":")[0].lower()
        host_list.append(host)

        # filter bad/irrelevant domain names
        for h in host_list:
            if h.endswith('europa.eu'):
                result.append(h)
            elif h == 'localhost':
                result.append(h)
            elif h == 'land.copernicus.eu':
                result.append(h)
            elif len(h.split('.')) == 4:
                result.append(h)

        return result

    def do_ping(self, hostnames, storage):
        """ Ping the eea central site
        """

        # Prepare the data
        data = {
            'hostnames': hostnames.keys()
        }
        timeout = (CONNECT_TIMEOUT, READ_TIMEOUT)

        try:
            req = requests.post(EEA_ANALYTICS_URL, data=data, timeout=timeout)
            success = False
            if req.status_code == 200:
                success = True

            storage['last_ping'] = {
                'hostnames': hostnames,
                'date': DateTime(),
                'success': success
            }
        except Exception as e:
            storage['last_ping'] = {
                'hostnames': hostnames,
                'date': DateTime(),
                'success': False
            }
            logger.info(e)


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
