import os
import psycopg2


class DB:
    _connection = None
    _cursor = None
    _visits = None

    @classmethod
    def connect(cls):
        """
        Establishes a connection to the PostgreSQL database.

        Closes the existing connection if one is already open.
        """
        if cls._connection:
            cls._cursor.close()
            cls._connection.close()
        db_params = {
            'dbname': os.getenv("db_name"),
            'user': os.getenv("db_user"),
            'password': os.getenv("db_password"),
            'host': os.getenv("db_host"),
            'port': os.getenv("db_port") if os.getenv("db_port") is not None else '5432',
        }
        cls._connection = psycopg2.connect(**db_params)
        cls._cursor = cls._connection.cursor()

    @classmethod
    def execute(cls, query, params=None):
        """
        Executes a SQL query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            params (tuple): Optional parameters for the query.

        Returns:
            records (list): The result records of the query.
        """
        if cls._connection is None:
            print(f"No connection to the database. Failed to execute a query: {query}")
            return
        cls._cursor.execute(query, params)
        try:
            records = cls._cursor.fetchall()
        except psycopg2.ProgrammingError:  # raised when there is no results to fetch
            records = None
        cls._connection.commit()

        if records:
            if len(records) == 1:
                records = records[0]
            return records

    @classmethod
    def insert_url(cls, short_url, original_url):
        """
        Inserts a new URL into the 'url_data' table.

        Args:
            short_url (str): The shortened URL.
            original_url (str): The original URL.

        Returns:
            records (list): The result records of the query.
        """
        return cls.execute("INSERT INTO url_data (short_url, original_url) VALUES (%s, %s);", (short_url, original_url,))

    @classmethod
    def save_visits(cls):
        """
        Saves the number of visits to the 'visit_counts' table.
        """
        if cls._visits:
            cls.execute("UPDATE visit_counts SET visit_count = %s;", (cls._visits,))

    @classmethod
    def visits(cls):
        """
        Retrieves and increments the visit count from the 'visit_counts' table.

        Returns:
            int: The number of visits.
        """
        if cls._visits:
            cls._visits += 1
            if cls._visits % 50 == 0:
                cls.execute("UPDATE visit_counts SET visit_count = %s;", (cls._visits,))
            return cls._visits
        cls._visits = int(cls.execute("SELECT visit_counts FROM visit_counts;")[0][3:-1])
        return cls._visits

    @classmethod
    def view_urls(cls):
        """
        Retrieves all records from the 'url_data' table.

        Returns:
            records (list): The result records of the query.
        """
        return cls.execute("SELECT * FROM url_data")

    @classmethod
    def find_url(cls, short_url):
        """
        Retrieves the original URL from the 'url_data' table based on the short URL.

        Args:
            short_url (str): The short URL to find.

        Returns:
            records (list): The result records of the query.
        """
        return cls.execute("SELECT original_url FROM url_data WHERE short_url = %s LIMIT 1;", (short_url,))

    @classmethod
    def close(cls):
        """
        Closes the database connection and cursor.
        """
        if cls._connection:
            cls._cursor.close()
            cls._connection.close()
