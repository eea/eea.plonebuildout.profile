""" Configuration and utilities for PWA
"""
import os
from contextlib import contextmanager
from eea.rabbitmq.client.rabbitmq import RabbitMQConnector
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from z3c.form import form
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import Interface
from zope.schema import TextLine, Int
import logging
import transaction


class IManifestJsonSettings(Interface):
    """ Settings for ManifestJson
    """

    short_name = TextLine(title=u"Short name", required=True, default=u"")
    name = TextLine(title=u"Name", required=True, default=u"")
    start_url = TextLine(title=u"Start url", required=True, default=u"")
    background_color = TextLine(title=u"Background color", required=True, default=u"")
    display = TextLine(title=u"display", required=True, default=u"")
    scope = TextLine(title=u"scope", required=True, default=u"")
    theme_color = TextLine(title=u"Theme color", required=True, default=u"")


class ManifestJsonControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IManifestJsonSettings


ManifestJsonControlPanelView = layout.wrap_form(
    ManifestJsonControlPanelForm, ControlPanelFormWrapper)
ManifestJsonControlPanelView.label = u"ManifestJson settings"


def get_manifest_json_settings():
    """ Return the settings as set in site/@@manifest-json-controlpanel

        Usage: s.short_name
    """
    registry = getUtility(IRegistry, context=api.portal.get())
    s = registry.forInterface(IManifestJsonSettings)
    return s
