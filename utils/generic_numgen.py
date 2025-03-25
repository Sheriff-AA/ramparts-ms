from django.utils.http import int_to_base36
import uuid
from base64 import b32encode
from hashlib import sha1
from random import random

ID_LENGTH = 12
UNIQUE_ID_LENGTH = 7

def password_gen():
    pk = int_to_base36(uuid.uuid4().int)[:ID_LENGTH]
    return f"{pk}"

def unique_gen():
    pk = int_to_base36(uuid.uuid4().int)[:UNIQUE_ID_LENGTH]
    return f"{pk}"
