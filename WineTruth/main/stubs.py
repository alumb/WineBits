"""
stubs.py provides access to Google App Engine primitives
when the Google App Engine primitives are available,
and provides featureless stubs otherwise for testing.

currently mocked:

debug
ndb
webapp2
uuid

>>> ndb.Model(variable='awesome', thing='thang')
<stubs.Model object at ...>

"""
import os

try:
    google_is_here = os.environ["GOOGLE"]
    debug = os.environ["DEBUG"]
except KeyError:
    google_is_here = False
    debug = True

if google_is_here:
    from google.appengine.ext import ndb
else:
    class ndb:
        class Model(object):
            def __init__(self, *args, **kwargs):
                pass
            def put(self, *args, **kwargs):
                return "stub-key"
            def to_dict(self, *args, **kwargs):
                return vars(self)
            pass
        class StringProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class TextProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class BooleanProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class IntegerProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class FloatProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class BlobProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class DateTimeProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class TimeProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class DateProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class GeoPtProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class KeyProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class BlobKeyProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class UserProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class StructuredProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class LocalStructuredProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class JsonProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class ComputedProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

        class PickleProperty:
            def __init__(self, *args, **kwargs):
                pass
            pass

if google_is_here:
    import webapp2
else:
    class webapp2(object):
        def __init__(self, *args, **kwargs):
            pass
        class RequestHandler(object):
            def __init__(self, *args, **kwargs):
                pass
        class WSGIApplication(object):
            def __init__(self, *args, **kwargs):
                pass

if not debug:
    import uuid
else:
    class uuid(object):
        def __init__(self, *args, **kwargs):
            pass
        class UUID(object):
            def __init__(self, *args, **kwargs):
                pass
            hex = "stub-uuid"
        @staticmethod
        def uuid4(*args, **kwargs):
            return uuid.UUID()
