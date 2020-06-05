import hashlib
import binascii


# Function to hash a value using the RIPEMD-160 technique
def ripemd160(key):
    key = binascii.unhexlify(key)
    return hashlib.new('ripemd160', key).hexdigest().upper()


# TODO
# Function to hash/dehash a value using a custom RIPEMD-160 technique
def ripemd160_two_way(key, hash=True):
    return 0
