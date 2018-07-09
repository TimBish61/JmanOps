
# -*- coding: UTF-8 -*-
from os import path
from django.conf import settings

XERO_PRIVATE_KEY = getattr(settings, 'privatekey', path.join(settings.STATIC_ROOT, 'xero/privatekey.pem').replace("\\","/"))

#JmanDev
XERO_CONSUMER_KEY="KTRJWQUF3W2CXDSMZC61JNIQ2PNXTA"
XERO_CONSUMER_SECRET="Z47Y16EZO78RQCRDYXYFQXLMDBMBGJ"
