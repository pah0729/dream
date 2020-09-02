import os
import json

SECRET = {}
SECRET_FILE = os.path.dirname(os.path.realpath(__file__)) + "/secret.json"

if os.path.exists(SECRET_FILE):
    SECRET = json.loads(open(SECRET_FILE, 'r').read())


def safe_get(key: str, default: any = None):
    return SECRET.get(key, default)
