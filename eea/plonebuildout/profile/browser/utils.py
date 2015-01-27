from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict

KEY = "eea.plonebuildout.profile"
REQUIRED_PKGS = [
    {'pkg_id': 'eea.rdfmarshaller', 'url': ''},
    {'pkg_id': 'eea.tags',
     'url': 'http://eea.github.io/docs/eea.tags/index.html'},
    {'pkg_id': 'eea.translations', 'url': ''},
    {'pkg_id': 'eea.tinymce',
     'url': 'http://eea.github.io/docs/eea.tinymce/index.html'},
    {'pkg_id': 'eea.uberlisting',
     'url': 'http://eea.github.io/docs/eea.uberlisting/index.html'},
    {'pkg_id': 'eea.relations',
     'url': 'http://eea.github.io/docs/eea.relations/index.html'},
    {'pkg_id': 'eea.plonebuildout.profile', 'url': ''},
    {'pkg_id': 'eea.facetednavigation',
     'url': 'http://eea.github.io/docs/eea.facetednavigation/index.html'},
    {'pkg_id': 'eea.faceted.vocabularies',
     'url': 'http://eea.github.io/docs/eea.faceted.vocabularies/index.html'},
    {'pkg_id': 'eea.faceted.inheritance',
     'url': 'http://eea.github.io/docs/eea.faceted.inheritance/index.html'}
]


def get_storage(context):
    """ Return the annotation storage for our analytics viewlet
    """
    zope_root = context.getPhysicalRoot()
    annotations = IAnnotations(zope_root)
    storage = annotations.get(KEY, None)

    if storage is None:
        storage = annotations[KEY] = PersistentDict()

    return storage
