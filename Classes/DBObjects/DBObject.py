import DB.DBManager
from Classes.Singleton import Singleton


# Class parent for wallets and derivable objects in the database
class DBObject:
    def __init__(self, table, key):
        super().__init__()
        self.db = DB.DBManager.DBManager(debug=False)
        self.table = table
        self.key = key
        self.key_id = None

    # Method to check if given objects already exists in the database
    def check(self, match_columns=None, matches=None):
        result = self.db.query_builder(sql_type="select",
                                       table=self.table,
                                       selects=self.key,
                                       match_columns=match_columns,
                                       matches=matches,
                                       limit='1')
        return None if len(result) < 1 else result[0][0]  # result[0][0] := key_id

    # Method to push the object to the database.
    def push(self, value_columns=None, values=None):
        # If there is no primary key id, add this entry to the database
        if self.key_id is None:
            return self.db.query_builder(sql_type='insert',
                                         table=self.table,
                                         value_columns=value_columns,
                                         values=values)
        # If primary key id exists, just update.
        return self.db.query_builder(sql_type='update',
                                     table=self.table,
                                     match_columns=self.key,
                                     matches=self.key_id,
                                     value_columns=value_columns,
                                     values=values)

    # Method to load an object from the database
    def pull(self, match_columns=None, matches=None):
        if self.key_id is not None:
            result = self.db.query_builder(sql_type="select",
                                           table=self.table,
                                           match_columns=self.key,
                                           matches=self.key_id,
                                           limit=1)
            return None if len(result) < 1 else result[0]
        # If there is no primary key logged, match whatever information requested.
        result = self.db.query_builder(sql_type="select",
                                       table=self.table,
                                       match_columns=match_columns,
                                       matches=matches,
                                       limit=1)
        return None if len(result) < 1 else result[0]

    # Method to delete the current object from the database
    def destroy(self):
        return 0 if self.key_id is None else self.db.query_builder(sql_type='delete',
                                                                   table=self.table,
                                                                   match_columns=self.key,
                                                                   matches=self.key_id)
