#!/usr/bin/env python

from pathlib import Path

import yaml
from werkzeug.security import generate_password_hash

user_file = Path("users.yaml")

username = input("Enter username: ")
password = input("Enter password: ")
hash = generate_password_hash(password, "sha256")

if user_file.exists():
    users = yaml.safe_load(open(user_file))
else:
    users = {}

users[username] = hash
yaml.dump(users, open(user_file, "w"))
