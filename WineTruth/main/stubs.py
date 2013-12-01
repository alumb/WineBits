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
                self.parent = None
                if 'parent' in kwargs:
                    self.parent = kwargs['parent']
                pass
            def put(self, *args, **kwargs):
                self.key = ndb.Key("stub-key")
                if self.parent:
                    ndb.Key.load_parent(self.parent)
                return ndb.Key("stub-key")
            def to_dict(self, *args, **kwargs):
                return vars(self)
            @classmethod
            def query(cls, *args, **kwargs):
                return ndb.QueryResult(args, kwargs)
            pass
        class Key(object):
            thing_to_get = None
            parent_ = None
            def __init__(self, *args):
                self._id = "-".join([str(x) for x in args])
                pass
            def id(self):
                return self._id
            def get(self, *args, **kwargs):
                return ndb.Key.thing_to_get
            def parent(self, *args, **kwargs):
                return self.parent_
            @classmethod
            def load_get(cls, thing):
                cls.thing_to_get = thing
            @classmethod
            def load_parent(cls, parent):
                cls.parent_ = parent

        class QueryResult:
            def __init__(self, *args, **kwargs):
                pass
            def fetch(self, *args, **kwargs):
                return []

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
    class FakeRequest(object):
        def __init__(self, *args, **kwargs):
            self.POST = {}

    class FakeResponse(object):
        def __init__(self, *args, **kwargs):
            self.content_type = None
            self.last_write = None
        def write(self, thing):
            self.last_write = thing

    class webapp2(object):
        def __init__(self, *args, **kwargs):
            pass
        class RequestHandler(object):
            def __init__(self, *args, **kwargs):
                self.request = FakeRequest()
                self.response = FakeResponse()
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
