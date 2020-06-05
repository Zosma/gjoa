from Classes.DBObjects.DBObject import DBObject


class Hash(DBObject):
    def __init__(self, hash_type, index, pub_id, hash_val=None):
        super().__init__(table='hashes', key='hid')
        # Required hash attributes
        self.hash = hash_val
        self.type = hash_type
        self.index = index
        self.pub_id = pub_id
        # ##### UNOPTOMIZED FOR MULTICORE
        # # Check database for the hash
        # self.key_id = self.check_hash()
        # # If the hash doesn't exist, create it and get the key_id
        # if self.key_id is None and self.hash is not None:
        #     self.push_hash()
        #     self.key_id = self.check_hash()
        # elif self.key is not None:
        #     self.pull_hash()

    # Method to check if this hash already exists in the database.
    def check_hash(self):
        match_columns = ['type', 'index', 'pub_id']
        matches = [self.type, self.index, self.pub_id]
        return self.check(match_columns=match_columns, matches=matches)

    # Method to add or update a hash to the database.
    def push_hash(self):
        value_columns = ['hash', 'type', 'index', 'pub_id']
        values = [self.hash, self.type, self.index, self.pub_id]
        return self.push(value_columns=value_columns, values=values)

    # Method to load a hash from the database.
    def pull_hash(self):
        data = self.pull()
        if data is not None:
            self.hash = data[1]

    # Method to delete an address from the database.
    def destroy_hash(self):
        self.destroy()
