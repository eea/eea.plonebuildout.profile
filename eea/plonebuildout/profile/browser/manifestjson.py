import json
from Products.Five.browser import BrowserView
from eea.plonebuildout.profile.controlpanel.manifest_json import IManifestJsonSettings
from zope.component import getUtility
from plone import api
from plone.registry.interfaces import IRegistry

class ManifestJsonView(BrowserView):
    """ manifest.json
    """
    def __call__(self):
        if self.haveValidManifest():
            self.request.response.setHeader("Content-type", "application/json")
            return self.json()
        else:
            self.request.response.setStatus(404)
            return None

    def haveValidManifest(self):
        """ check for the manifest
        """
        settings = self.get_manifest_json_settings()
        if len(settings.start_url)>0:
            return 1
        return 0

    def json(self):
        """ JSON dump
        """
        settings = self.get_manifest_json_settings()
        response = {}
        response['short_name'] = settings.short_name
        response['name'] = settings.name
        response['icons'] = []
        icon = {}
        icon['src'] = '/icon-192x192.png'
        icon['type'] = 'image/png'
        icon['sizes'] = '192x192'
        response['icons'].append(icon)
        icon = {}
        icon['src'] = '/icon-512x512.png'
        icon['type'] = 'image/png'
        icon['sizes'] = '512x512'
        response['icons'].append(icon)
        response['start_url'] = settings.start_url
        response['background_color'] = settings.background_color
        response['display'] = settings.display
        return json.dumps(response)

    def get_manifest_json_settings(self):
        """ Return the settings as set in site/@@pwa-controlpanel

            Usage: s.name
        """
        registry = getUtility(IRegistry, context=api.portal.get())
        s = registry.forInterface(IManifestJsonSettings)
        return s
