#!/usr/bin/env python

import secrets

secret = secrets.token_urlsafe(16)
print(f"SECRET_KEY = '{secret}'")
