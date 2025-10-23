from django.urls import re_path
from . import consumers

ws_urlpatterns=[
    re_path('ws/quotes/translate/', consumers.QuoteTranslateConsumer.as_asgi()),
]