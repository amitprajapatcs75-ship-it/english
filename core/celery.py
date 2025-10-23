import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app= Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")
if os.name == "nt":
    from multiprocessing import set_start_method
    set_start_method("spawn", force=True)
app.autodiscover_tasks()