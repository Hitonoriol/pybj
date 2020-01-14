import base64_utils

def xor(data, key, decode = False):
    
    if (decode):
        data = base64_utils.decode_string(data)
        
    length = len(data);
    
    for i in range(length): 
        data = (data[:i] + chr(ord(data[i]) ^ (key)) + data[i + 1:])
        
    if (not decode):
        data = base64_utils.encode_string(data)
        
    return data

def encode(data, key):
    return xor(data, key)

def decode(data, key):
    return xor(data, key, True)
