from Classes.FileHandling import FileOperationRequest
from Misc.Multithreading import multi_printer, multi_file_operations
from DB.DBManager import DBManager


# Function to check a private key to see if its in the database
def db_check(pk, lock):
    winner = False
    winners = ""
    # if this is a list of arrays, check for all possible addresses
    if isinstance(pk, list):
        addresses = []
        match_column = []
        # Hack to get queries correct.
        # TODO: REMOVE THIS HACK WHEN ENSURE_QUOTED IS FIXED.
        for i in range(0, len(pk)):
            addresses.append(pk[i].public_key.uncompressed_address.address if i == 0 else "'" + pk[i].public_key.uncompressed_address.address + "'")
            addresses.append("'" + pk[i].public_key.compressed_address.address + "'")
            match_column.append('address')
            match_column.append('address')
        # Check all addresses in one sweep.
        db = DBManager(debug=False)
        result = db.query_builder(sql_type="select",
                                  table="addresses",
                                  selects="aid",
                                  match_columns=match_column,
                                  matches=addresses,
                                  match_type="OR")
        # If we have a winner... print all private keys into winner file
        if result is not None and len(result) > 0:
            for key in pk:
                winners = winners + key.private_key + "\n"
            winner = True
    else:
        if pk.public_key.uncompressed_address.check_address() is not None:
            winner = True
            winners = pk.private_key
        if pk.public_key.compressed_address.check_address() is not None:
            winner = True
            winners = pk.private_key
    # If there is a winner... pop champagne and shiet.
    if winner:
        # multi_printer(msg=winners, lock=lock)
        multi_file_operations(FileOperationRequest(filename="winners", msg=winners), lock=lock)
        # pk.public_key.push_public_key()
        # pk.pub_id = pk.public_key.check_public_key()
        # pk.push_private_key()
        return True
    return False
