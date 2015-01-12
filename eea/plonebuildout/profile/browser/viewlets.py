"""Viewlets for eea.plonebuildout.profile
"""
from time import time
import logging
import os.path
import requests

from App.config import getConfiguration
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from copy import deepcopy
from distutils import version as vt
from eea.plonebuildout.profile.browser.utils import get_storage
from eea.plonebuildout.profile.browser.utils import REQUIRED_PKGS
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram

logger = logging.getLogger('eea.plonebuildout.profile')
EEA_ANALYTICS_URL = 'http://www.eea.europa.eu/@@eea.controlpaneleeacpbstatusagent.html'
READ_TIMEOUT = 3.0
CONNECT_TIMEOUT = 3.0


class NewReleaseViewlet(ViewletBase):
    """A viewlet which informs managers of new EEA KGS releases
    """

    #we cache the result for 24 hours
    @ram.cache(lambda *args:time() // (60*60*24))
    def last_kgs_update(self):
        """Return a version number if running old KGS version, otherwise None
        """

        conf = getConfiguration()
        env = getattr(conf, 'environment', {})

        kgsver = str(env.get("EEA_KGS_VERSION", None))
        if kgsver is None:
            logger.info("EEA_KGS_VERSION is not defined as environment "
                        "variable. Please use proper buildout configuration")
            return 
            
        url = "https://api.github.com/repos/eea/eea.plonebuildout.core/"\
              "contents/buildout-configs/kgs"
        c = requests.get(url)
        j = c.json()
        dirs = []

        # Treat case where github does not return proper json response
        if isinstance(j, list):
            for r in j:
                if r.get('type') == 'dir':
                    name = r['name']
                    if name[0].isdigit():
                        dirs.append(r.get('name'))
        else:
            logger.info("Invalid response from github: " + c.text)

        if not dirs:
            logger.info("Could not determine proper EEA KGS releases")
            return 

        versions = [vt.StrictVersion(v) for v in dirs]
        versions.sort()
        last = str(versions[-1]) #always assume at least one release

        if last != kgsver:
            return last

        return None

    @ram.cache(lambda *args:time() // (60*60*24))
    def last_buildout_update(self):
        """
        Return the revision of the current buildout cfgs
        and the latest revision on Github if different, None otherwise
        Keys: `current` and `latest`

        """
        current_rev = None
        pin_file = os.path.join(INSTANCE_HOME, "..", "..", ".current_revision")
        if os.path.exists(pin_file):
            current_rev = open(pin_file).read().strip()

        url = "https://api.github.com/repos/eea/eea.plonebuildout.core/"\
              "commits/HEAD"
        c = requests.get(url)
        j = c.json()
        latest_rev = j.get('sha')

        if latest_rev and latest_rev != current_rev:
            return {'current': current_rev, 'latest': latest_rev}

        return None


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

        hostname = self.get_hostname()

        if hostname:
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
        if "HTTP_X_FORWARDED_HOST" in request.environ:
            # Virtual host
            host = request.environ["HTTP_X_FORWARDED_HOST"]
        elif "HTTP_HOST" in request.environ:
            # Direct client request
            host = request.environ["HTTP_HOST"]
        else:
            return None

        # separate to domain name and port sections
        host = host.split(":")[0].lower()

        return host

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
        missing = []
        qi = getToolByName(self.context, 'portal_quickinstaller')
        prods = qi.listInstallableProducts(skipInstalled=False)
        installed_pkgs = [prod.get('id') for prod in prods
                          if prod.get('status') == 'installed']

        import pdb; pdb.set_trace( )
        for pkg in REQUIRED_PKGS:
            if pkg not in installed_pkgs:
                missing.append(pkg)

        return missing
