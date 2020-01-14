import base64
import re

def base64_fix_padding(data, altchars=b'+/'):
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def encode_string(string):
    return base64.b64encode(string.encode()).decode("utf-8")

def decode_string(string):
    return base64_fix_padding(string.encode()).decode("utf-8")
