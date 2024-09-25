import os
from time import sleep

# from . import base

environment = os.environ.get('ENVIRONMENT', 'development')

if environment == 'production':
    from .prod import *
elif environment == 'testing':
    from .testing import *
else:
    print("Environment Settings loading...")
    from .dev import *

