"""Viewlets for eea.plonebuildout.profile
"""
import os.path
from time import time
import logging
import requests

from App.config import getConfiguration
from distutils import version as vt
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram


logger = logging.getLogger('eea.plonebuildout.profile')


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
