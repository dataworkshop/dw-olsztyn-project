import mysql.connector
from src.helpers.color_log import setup_logger


class DBManager:

    def __init__(self, db_config):
        self._logger = setup_logger("DBManager")
        self.cnx = mysql.connector.connect(**db_config)
        self.cursor = self.cnx.cursor()

        self._logger.info("Connected to database")

    def execute(self, query):
        
        self.cursor.execute(query)

    def query(self, query):

        self.execute(query)

        return self.cursor.fetchall()

    def setup_table(self, table_name="most_popular"):
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} 
        (
            timestamp DATETIME NOT NULL, 
            name VARCHAR(30) NOT NULL,
            source VARCHAR(10) NOT NULL
        )
        """)

        self._logger.info(f"Table {table_name} is up and ready")
    
    def insert_data(self, timestamp, name, source, table_name="most_popular"):

        sql = f"""
        INSERT INTO {table_name} 
        (timestamp, name, source) 
        VALUES ('{timestamp}', '{name}', '{source}')
        """

        self.execute(sql)
