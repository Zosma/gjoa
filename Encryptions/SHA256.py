import hashlib
import binascii


# Function to hash a key using the SHA256 technique
def sha256(key):
    key = binascii.unhexlify(key)
    return hashlib.sha256(key).hexdigest().upper()


# TODO
# Function to hash/dehash a key using a custom SHA256 technique
def sha256_two_way(key, encrypt=True):
    return 0
