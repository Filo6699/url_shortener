import os
import psycopg2


class DB:
    _connection = None
    _cursor = None

    @classmethod
    def connect(cls):
        if cls._connection:
            cls._cursor.close()
            cls._connection.close()
        db_params = {
            'dbname': os.getenv("db_name"),
            'user': os.getenv("db_user"),
            'password': os.getenv("db_password"),
            'host': os.getenv("db_host"),
            'port': os.getenv("db_port") if os.getenv("db_port") != None else '5432',
        }
        cls._connection = psycopg2.connect(**db_params)
        cls._cursor = cls._connection.cursor()

    @classmethod
    def execute(cls, query, params=None):
        if cls._connection == None:
            print(f"No connection to database. Failed to execute a query: {query}")
            return
        cls._cursor.execute(query, params)
        try:
            records = cls._cursor.fetchall()
        except psycopg2.ProgrammingError: # raised when there is no results to fetch
            records = None
        cls._connection.commit()

        if records:
            if len(records) == 1:
                records = records[0]
            return records
    
    @classmethod
    def fetch_table_names(cls):
        return cls.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    
    @classmethod
    def insert_url(cls, short_url, original_url):
        return cls.execute("INSERT INTO url_data (short_url, original_url) VALUES (%s, %s);", (short_url, original_url, ))
    
    @classmethod
    def view_urls(cls):
        return cls.execute("SELECT * FROM url_data")
    
    @classmethod
    def find_url(cls, short_url):
        return cls.execute("SELECT original_url FROM url_data WHERE short_url = %s LIMIT 1;", (short_url, ))
    
    @classmethod
    def close(cls):
        if cls._connection:
            cls._cursor.close()
            cls._connection.close()
