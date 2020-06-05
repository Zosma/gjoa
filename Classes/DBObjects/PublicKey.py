from Classes.DBObjects.DBObject import DBObject
from Classes.DBObjects.Hash import Hash
from Classes.DBObjects.Address import Address
from Encryptions.SHA256 import sha256
from Encryptions.RIPEMD160 import ripemd160
from Misc.Base58 import b58encode_int


class PublicKey(DBObject):
    def __init__(self, public_key=None, pub_id=None):
        super().__init__(table='public_keys', key='pub_id')
        # Initialize Public Key attributes
        self.public_key = public_key
        # Check database for public key if it is not given
        if pub_id is not None:
            self.key_id = pub_id
        # #### UNOPTIMIZED FOR MULTIPROCESSING
        # else:
        #     self.key_id = self.check_public_key()
        # # If the public key doesn't exist, create it
        # if self.key_id is None and self.public_key is not None:
        #     self.push_public_key()
        #     self.key_id = self.check_public_key()
        # elif self.key_id is not None:
        #     self.pull_public_key()
        # Initialize sub-objects
        # Uncompressed address and hashes
        self.hash_c1 = None
        self.hash_c2 = None
        self.hash_c3 = None
        self.hash_c4 = None
        self.uncompressed_address = None
        # Compressed address and hashes
        self.hash_d1 = None
        self.hash_d2 = None
        self.hash_d3 = None
        self.hash_d4 = None
        self.compressed_address = None

    # ================== LOCAL ACTIONS ======================

    # Method to check if this public key already exists in the database.
    def check_public_key(self):
        if self.public_key is None:
            return None
        return self.check(match_columns=['public_key'], matches=[self.public_key])

    # Method to add or update this public key to the database.
    def push_public_key(self):
        self.push(value_columns='public_key', values=self.public_key)

    # Method to load an public key from the database.
    def pull_public_key(self):
        data = self.pull()
        if data is not None:
            self.public_key = data[1]

    # Method to delete this public key from the database.
    def destroy_public_key(self):
        self.destroy()

    # ================== SUB-OBJECT ACTIONS ======================

    # Method to check the database for entries based on the sub-objects
    def populate_sub_objects(self):
        # UNCOMPRESSED HASHES AND ADDRESS
        self.hash_c1 = Hash(hash_type='c', index=1, pub_id=self.key_id)
        self.hash_c2 = Hash(hash_type='c', index=2, pub_id=self.key_id)
        self.hash_c3 = Hash(hash_type='c', index=3, pub_id=self.key_id)
        self.hash_c4 = Hash(hash_type='c', index=4, pub_id=self.key_id)
        self.uncompressed_address = Address(pub_id=self.key_id, address_type=0)
        # COMPRESSED HASHES AND ADDRESS
        self.hash_d1 = Hash(hash_type='d', index=1, pub_id=self.key_id)
        self.hash_d2 = Hash(hash_type='d', index=2, pub_id=self.key_id)
        self.hash_d3 = Hash(hash_type='d', index=3, pub_id=self.key_id)
        self.hash_d4 = Hash(hash_type='d', index=4, pub_id=self.key_id)
        self.compressed_address = Address(pub_id=self.key_id, address_type=1)

    # Method to Create public addresses based on the public key
    def generate_addresses(self):
        # UNCOMPRESSED
        # Prepend '04' to the public key for uncompressed versions
        public_key_version = "04" + self.public_key
        # Perform first hash using SHA256 and save results
        hash_val = sha256(public_key_version)
        # self.hash_c1 = Hash(hash_type='c', index=1, pub_id=self.key_id, hash_val=hash_val)
        # Perform second hash using RIPEMD160 and save results
        hash_val = ripemd160(hash_val)
        # self.hash_c2 = Hash(hash_type='c', index=2, pub_id=self.key_id, hash_val=hash_val)
        # Prepend '00' to Hash C2
        public_key_version_hash_c = "00" + hash_val
        # Perform third hash using SHA256 and save results
        hash_val = sha256(public_key_version_hash_c)
        # self.hash_c3 = Hash(hash_type='c', index=3, pub_id=self.key_id, hash_val=hash_val)
        # Perform fourth hash using SHA256 and save results
        hash_val = sha256(hash_val)
        # self.hash_c4 = Hash(hash_type='c', index=4, pub_id=self.key_id, hash_val=hash_val)
        # Checksum C is the first 8 hex characters of hash C4
        checksum_c = hash_val[0:8]
        # Public Key Checksum C is the checksum appended to the version C of the public key.
        public_key_checksum_c = public_key_version_hash_c + checksum_c
        public_address_uncompressed = "1" + b58encode_int(int(public_key_checksum_c, 16))
        # ASSUME STATUS OF ADDRESS IS PRIVATE_KEY AND PUBLIC_KEY KNOWN
        self.uncompressed_address = Address(address=public_address_uncompressed, pub_id=self.key_id, address_type=0, status=0b110)
        # COMPRESSED
        y = self.public_key[64:128]
        # Append '02' to x if y is even, else append '03' to x.
        public_key_version_comp = "02" + self.public_key[0:64] if int(y, 16) % 2 == 0 else "03" + self.public_key[0:64]
        # Perform first hash using SHA256 and save results
        hash_val = sha256(public_key_version_comp)
        # self.hash_d1 = Hash(hash_type='d', index=1, pub_id=self.key_id, hash_val=hash_val)
        # Perform the second hash using RIPEMD160 and save results
        hash_val = ripemd160(hash_val)
        # self.hash_d2 = Hash(hash_type='d', index=2, pub_id=self.key_id, hash_val=hash_val)
        # Prepend '00' to Hash D2
        public_key_version_hash_d = "00" + hash_val
        # Perform the third hash using SHA256 and save results
        hash_val = sha256(public_key_version_hash_d)
        # self.hash_d3 = Hash(hash_type='d', index=3, pub_id=self.key_id, hash_val=hash_val)
        # Perform the fourth hash using SHA256 and save results
        hash_val = sha256(hash_val)
        # self.hash_d4 = Hash(hash_type='d', index=4, pub_id=self.key_id, hash_val=hash_val)
        # Checksum D is the first 8 hex characters of hash D4
        checksum_d = hash_val[0:8]
        # Public Key Checksum D is the checksum appended to the Public key Version Hash D
        public_key_checksum_d = public_key_version_hash_d + checksum_d
        public_address_compressed = "1" + b58encode_int(int(public_key_checksum_d, 16))
        # ASSUME STATUS OF ADDRESS IS PRIVATE_KEY AND PUBLIC_KEY KNOWN
        self.compressed_address = Address(address=public_address_compressed, pub_id=self.key_id, address_type=1, status=0b110)
