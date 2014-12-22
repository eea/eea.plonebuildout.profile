from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict

KEY = "eea.plonebuildout.profile"


def get_storage(context):
    """ Return the annotation storage for our analytics viewlet
    """
    zope_root = context.getPhysicalRoot()
    annotations = IAnnotations(zope_root)
    storage = annotations.get(KEY, None)

    if storage is None:
        storage = annotations[KEY] = PersistentDict()

    return storage
