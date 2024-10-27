import sqlite3

class DBbase:
    _conn = None
    _cursor = None

    def __init__(self, db_name):
        """Initialize with the database name and establish a connection."""
        self._db_name = db_name
        self.connect()

    def connect(self):
        """Establish a connection to the SQLite database."""
        try:
            self._conn = sqlite3.connect(self._db_name)
            self._cursor = self._conn.cursor()
            print(f"Connected to database: {self._db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def execute_script(self, sql_string):
        """Execute a SQL script (multiple statements)."""
        try:
            self._cursor.executescript(sql_string)
        except sqlite3.Error as e:
            print(f"Error executing script: {e}")

    def execute_query(self, query, params=[]):
        """Execute a single SQL query with parameters."""
        try:
            self._cursor.execute(query, params)
            self._conn.commit()
            return self._cursor
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    @property
    def get_cursor(self):
        """Provide access to the database cursor."""
        return self._cursor

    @property
    def get_connection(self):
        """Provide access to the database connection."""
        return self._conn

    def reset_database(self):
        """Abstract method for resetting the database. To be implemented in derived classes."""
        raise NotImplementedError("Must implement from the derived class")

    def close_db(self):
        """Close the database connection."""
        try:
            if self._conn:
                self._conn.close()
                print("Database connection closed.")
        except sqlite3.Error as e:
            print(f"Error closing database: {e}")

    def __enter__(self):
        """Enter the runtime context related to this object."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context, closing the database connection."""
        self.close_db()
