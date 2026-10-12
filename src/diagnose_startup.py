
import os
import faulthandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
faulthandler.dump_traceback_later(5, repeat=True)

import django
from django.conf import settings
from django.apps import apps

print("Loading settings...", flush=True)
print("Apps to load:", settings.INSTALLED_APPS, flush=True)

print("Initializing Django...", flush=True)
django.setup()

print("Django setup complete!", flush=True)
