"""Viewlets for eea.plonebuildout.profile
"""

from App.config import getConfiguration
from distutils import version as vt
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from time import time
import json
import logging
import urllib

logger = logging.getLogger('eea.plonebuildout.profile')


class NewReleaseViewlet(ViewletBase):
    """A viewlet which informs managers of new EEA KGS releases
    """

    #we cache the result for an hour
    @ram.cache(lambda *args:time() // (60*60))
    def last_update(self):
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
        c = urllib.urlopen(url).read()
        j = json.loads(c)
        dirs = []

        # Treat case where github does not return proper json response
        if isinstance(j, list):
            for r in j:
                if r.get('type') == 'dir':
                    name = r['name']
                    if name[0].isdigit():
                        dirs.append(r.get('name'))
        else:
            logger.info("Invalid response from github: " + c)

        if not dirs:
            logger.info("Could not determine proper EEA KGS releases")
            return 

        versions = [vt.StrictVersion(v) for v in dirs]
        versions.sort()
        last = str(versions[-1]) #always assume at least one release

        if last != kgsver:
            return last

        return None
        
