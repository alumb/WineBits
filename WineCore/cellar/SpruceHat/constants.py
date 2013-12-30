import os

try:
    DEBUG = bool(os.environ["DEBUG"])
except KeyError:
    DEBUG = True

def variable( key, cast_to, debug_default, production_default ):
    if key in os.environ:
        return cast_to(os.environ[key])
    elif DEBUG:
        return debug_default
    else:
        return production_default

MAX_RESULTS = variable( "MAX_RESULTS", int, 100, 5000 )

