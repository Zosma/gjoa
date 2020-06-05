from ecdsa import SECP256k1, SigningKey


# Function to encrypt a private key into a public key
def ecdsa(key):
    # return int("0x" + create_random_hex(128), 16)
    sk = SigningKey.from_string(bytearray.fromhex(key), curve=SECP256k1)
    vk = sk.get_verifying_key()
    return vk.to_string().hex().upper()


# TODO
# Function to encrypt OR decrypt between private<->public keys
def ecdsa_two_way(key, encrypt=True):
    return 0
