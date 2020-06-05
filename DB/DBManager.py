import mysql.connector
from mysql.connector import errorcode
import Misc.Decorations


# Class to manage all database transactions
# class DBManager(Classes.Singleton.Singleton):
class DBManager:
    # Database parameters
    database = ''    # ADD DATABASE NAME HERE
    username = ''    # ADD DB USERNAME HERE
    password = ''    # ADD DB PASSWORD HERE
    ip = ''          # ADD DB IP HERE

    # Constructor to connect to database.
    def __init__(self, debug=False):
        super().__init__()
        # Declare the connection variable
        self.db_conn = None
        self.cursor = None
        self.debug = debug

    # Method to connect to the database
    def connect(self):
        # print("Opening connection to database...")
        if self.debug:
            return 0
        try:
            # Create a database connection
            self.db_conn = mysql.connector.connect(
                user=self.username,
                password=self.password,
                host=self.ip,
                database=self.database)
            # Create a cursor for queries
            self.cursor = self.db_conn.cursor(buffered=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Could not connect to the database. Check the parameters.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.")
            else:
                print(err)

    # Method to Execute sql statements
    def execute(self, sql, select=False, data=None):
        # print(sql)
        if self.debug:
            return []
        try:
            # Open Connection
            self.connect()
            if data is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, data)
            # Close connection
            if select is True:
                data = self.cursor.fetchall()
                self.close()
                return data
            # Commit if not a select
            self.db_conn.commit()
            self.close()
        except mysql.connector.Error as e:
            print("Couldn't execute the sql: " + sql + ". " + str(e))
        # print("Operation complete")
        return 1

    # Method to close the database connection
    def close(self):
        # print("Closing database connection")
        if self.debug:
            return 0
        try:
            # Close the cursor, then the connection
            self.cursor.close()
            self.db_conn.close()
        except mysql.connector.Error as e:
            print("Couldn't close the database. " + str(e))

    # Method to send a simple query to the database (handles 'SELECT', 'INSERT', 'UPDATE', and 'DELETE')
    @Misc.Decorations.ensure_list
    @Misc.Decorations.ensure_list_lengths
    def query_builder(self, sql_type=None, table=None, selects=None, match_columns=None, matches=None, match_type="AND", value_columns=None, values=None, limit=None):
        select = False if sql_type[0] != "select" else True
        opener = {'insert': "INSERT INTO ", 'delete': "DELETE FROM ", 'select': "SELECT ", 'update': "UPDATE "}
        # OPENINGS FOR ALL QUERIES
        sql = opener[sql_type[0]]
        sql += table[0] if sql_type[0] != "select" else ""
        sql += " (" if sql_type[0] == "insert" else ""
        # SELECTIONS FOR SELECTS
        sql += "* FROM " + table[0] if sql_type[0] == "select" and selects is None else ""
        if sql_type[0] == "select" and selects is not None:
            for i in range(0, len(selects)):
                sql += selects[i] + ", " if i != len(selects) - 1 else selects[i] + " FROM " + table[0]
        # SETS FOR UPDATES
        if sql_type[0] == "update":
            sql += " SET "
            for i in range(0, len(value_columns)):
                sql += value_columns[i] + "=" + values[i] + ", " if i != len(value_columns) - 1 else value_columns[i] + "=" + values[i]
        # CONDITIONALS FOR SELECTS, UPDATES, AND DELETES
        if sql_type[0] != "insert" and match_columns is not None:
            sql += " WHERE "
            for i in range(0, len(match_columns)):
                sql += match_columns[i] + "=" + matches[i] + " " + match_type[0] + " " if i != len(match_columns) - 1 else match_columns[i] + "=" + matches[i]
        # COLUMNS AND VALUES FOR INSERTS
        elif value_columns is not None:
            for i in range(0, len(value_columns)):
                sql += value_columns[i] + ", " if i != len(value_columns) - 1 else value_columns[i] + ") VALUES ("
            for i in range(0, len(values)):
                sql += values[i] + ", " if i != len(value_columns) - 1 else values[i] + ")"
        # LIMIT FOR SELECTS
        sql += " LIMIT " + limit[0] if sql_type[0] == "select" and limit is not None else ""
        # RETURN EXECUTION OF STATEMENT
        return self.execute(sql, select=select)

