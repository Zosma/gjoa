from Classes.DBObjects.DBObject import DBObject
import decimal


# Class to handle address
class Address(DBObject):
    def __init__(self, address=None, pub_id=None, address_type=None, status=None, amount=None):
        super().__init__(table='addresses', key='aid')
        # Assign attributes, if present.
        self.address = address
        self.pub_id = pub_id
        self.address_type = address_type
        self.balance = amount
        self.status = status

    # Method to check if this address already exists in the database
    def check_address(self):
        if self.address is not None:
            return self.check(match_columns='address', matches=self.address)
        return self.check(match_columns=['pub_id', 'address_type'], matches=[self.pub_id, self.address_type])

    # Method to add or update this address to the database.
    def push_address(self):
        value_columns = ['address', 'balance', 'status', 'address_type', 'pub_id']
        values = [self.address, self.balance, self.status, self.address_type, self.pub_id]
        return self.push(value_columns=value_columns, values=values)

    # Method to load an address from the database.
    def pull_address(self):
        data = self.pull()
        if data is not None:
            self.address = data[1]
            self.address_type = data[2]
            self.balance = data[4]
            self.status = data[5]
            # Only override public_key id if it was previously not known (for linking)
            self.pub_id = data[6] if self.pub_id is None else self.pub_id

    # Method to delete this address from the database.
    def destroy_address(self):
        self.destroy()

    # TODO
    # Method to figure out if this address is in the database already
    def check_status(self):
        result = 0
        # If the private key is known, disqualify
        result += 1 if self.status & 0b1 == 0b1 else 0  # Is this a generated pair?
        result += 4 if self.status & 0b0100 == 0b0100 else 0  # Is the private key known?
        if result != 0:
            return result + 2 if self.pub_id is not None else result  # Is the public key known
        # If the public key is known, add 2.
        result += 2 if self.pub_id is not None else 0
        # If private key is not known, return active if the balance is above 0
        result += 1 if self.balance > 0.0 else 0
        return result