# Settings package
from .settings import *

if 'FLY_APP_NAME' in os.environ:
    from .fly import *