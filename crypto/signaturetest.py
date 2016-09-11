from os import urandom
import hashlib

from utilities import integer_to_bytes, bytes_to_integer

def hash(data, algorithm="sha256"):
    hasher = getattr(hashlib, algorithm.lower())()
    hasher.update(data)
    return hasher.digest()
    
def choice(a, b, c):
    return c ^ (a & (b ^ c))
                    
def create_keypair():
    key1, key2 = bytearray(urandom(32)), bytearray(urandom(32))
    public_key = hash(key1), hash(key2)
    return (bytes_to_integer(key1), bytes_to_integer(key2)), public_key
    
def sign(message, private_key):
    message_hash = bytes_to_integer(bytearray(hash(message)))
    key1, key2 = private_key
    signature_a = choice(message_hash, key1, key2)
    signature_b = choice(message_hash, key2, key1)
    return signature_a, signature_b
    
def verify(message, signature, public_key):
    message_hash = bytes_to_integer(bytearray(hash(message)))
    signature_a, signature_b = signature    
    key1 = choice(message_hash, signature_a, signature_b)
    key2 = choice(message_hash, signature_b, signature_a)
    if (hash(integer_to_bytes(key1, 32)), hash(integer_to_bytes(key2, 32))) == public_key:
        return True
    else:
        return False
        
def test_create_sign_verify():
    private_key, public_key = create_keypair()
    message = "An excellent test message"
    
    signature = sign(message, private_key)
    _message = message[:-2]
    for ending2 in str(bytearray(range(256))):
        for ending in str(bytearray(range(256))):
            message = _message + ending2 + ending
        
            if verify(message, signature, public_key):
                print "Signature valid", message[-2], message[-1], ending2, ending
           # else:
           #     print "Signature invalid"
    
if __name__ == "__main__":
    test_create_sign_verify()
    