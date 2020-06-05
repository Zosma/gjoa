from Classes.DBObjects.DBObject import DBObject
from Classes.DBObjects.Hash import Hash
from Classes.DBObjects.PublicKey import PublicKey
from Encryptions.SHA256 import sha256
from Encryptions.ECDSA import ecdsa


class PrivateKey(DBObject):
    def __init__(self, private_key=None, pub_id=None):
        super().__init__(table='private_keys', key='pri_id')
        # Assign attributes, if present
        self.private_key = private_key
        self.pub_id = pub_id
        #### CODE THAT IS UNOPTOMIZED FOR MULTIPROCESSING
        # # Check database for the private key
        # self.key_id = self.check_private_key()
        # # If the private key doesn't exist, create it and get its key_id
        # if self.key_id is None and self.private_key is not None:
        #     self.private_key_wif = None
        #     self.private_key_wif_comp = None
        #     self.push_private_key()
        #     self.key_id = self.check_private_key()
        # elif self.key is not None or self.pub_id is not None:
        #     self.pull_private_key()
        # if private_key is not None and pub_id is not None:
        #     self.push_private_key()
        # Initialize sub-objects
        self.private_key_wif = None
        self.private_key_wif_comp = None
        # Uncompressed wif hashes
        self.hash_a1 = None
        self.hash_a2 = None
        # Compressed wif hashes
        self.hash_b1 = None
        self.hash_b2 = None
        # Public key
        self.public_key = None

    # ================== LOCAL ACTIONS ======================

    # Method to check if this private key already exists in the database.
    def check_private_key(self):
        if self.private_key is not None:
            return self.check(match_columns='private_key', matches=self.private_key)
        return self.check(match_columns='pub_id', matches=self.pub_id)

    # Method to add or update this private key to the database.
    def push_private_key(self):
        value_columns = ['private_key', 'private_key_wif', 'private_key_wif_comp', 'pub_id']
        values = [self.private_key, self.private_key_wif, self.private_key_wif_comp, self.pub_id]
        return self.push(value_columns=value_columns, values=values)

    # Method to load an private key from the database.
    def pull_private_key(self):
        data = self.pull()
        if data is not None:
            self.private_key = data[1]
            self.private_key_wif = data[2]
            self.private_key_wif_comp = data[3]

    # Method to delete this private key from the database.
    def destroy_private_key(self):
        self.destroy()

    # ================== SUB-OBJECT ACTIONS ======================

    # Method to check the database for entries based on the sub-objects
    def populate_sub_objects(self):
        # UNCOMPRESSED WIF HASHES
        self.hash_a1 = Hash(hash_type='a', index=1, pub_id=self.pub_id)
        self.hash_a2 = Hash(hash_type='a', index=2, pub_id=self.pub_id)
        # COMPRESSED WIF HASHES
        self.hash_b1 = Hash(hash_type='b', index=1, pub_id=self.pub_id)
        self.hash_b2 = Hash(hash_type='b', index=2, pub_id=self.pub_id)
        # PUBLIC KEY
        self.public_key = PublicKey(pub_id=self.pub_id)

    # Method to create a public key and copy its pub_id to the private key
    def generate_public_key(self):
        public_key = ecdsa(self.private_key)
        self.public_key = PublicKey(public_key=public_key)
        self.pub_id = self.public_key.key_id

    # Method to create the private_key_wifs
    def generate_wifs(self):
        # ONLY RUN THIS GENERATOR AFTER CREATING A PUBLIC KEY
        if self.pub_id is None:
            return 0
        # UNCOMPRESSED
        # Prepend "80" to Private_Key
        private_key_version = int("0x80" + self.private_key, 16)
        # Perform the first hash using SHA256 and save the results
        hash_val = hex(sha256(private_key_version))[2:]
        # self.hash_a1 = Hash(hash_type='a', index=1, pub_id=self.pub_id, hash_val=hash_val)
        # Perform the second hash using SHA256 and save the results
        hash_val = hex(sha256(int("0x" + hash_val, 16)))[2:]
        # self.hash_a2 = Hash(hash_type='a', index=2, pub_id=self.pub_id, hash_val=hash_val)
        # Checksum A is the first 8 hex characters in Hash A2
        checksum_a = hash_val[0:8]
        # Append checksum a to the private key version and you get the private key wif
        self.private_key_wif = hex(private_key_version)[2:] + checksum_a
        # COMPRESSED
        # Prepend "80" to Private Key and append "01"
        private_key_version_comp = int("0x80" + self.private_key + "01", 16)
        # Perform the first hash using SHA256 and save the results
        hash_val = hex(sha256(private_key_version_comp))[2:]
        # self.hash_b1 = Hash(hash_type='b', index=1, pub_id=self.pub_id, hash_val=hash_val)
        # Perform the second hash using SHA256 and save the results
        hash_val = hex(sha256(int("0x" + hash_val, 16)))[2:]
        # self.hash_b2 = Hash(hash_type='b', index=2, pub_id=self.pub_id, hash_val=hash_val)
        # Checksum B is the first 8 hex characters in Hash B2
        checksum_b = hash_val[0:8]
        # Append checksum B to the private key version (compressed) and you get the private key wif compressed
        self.private_key_wif_comp = hex(private_key_version_comp)[2:] + checksum_b
        # Push resultant WIF keys to the database
        self.push_private_key()
