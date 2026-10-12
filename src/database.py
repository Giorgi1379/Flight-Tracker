import psycopg2
from src.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from src.logger import logger

class DatabaseManager:
    def __init__(self):
        self.db_name = DB_NAME
        self.db_user = DB_USER
        self.db_password = DB_PASSWORD
        self.db_host = DB_HOST
        self.db_port = DB_PORT

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
            )
            return conn
        except Exception as e:
            logger.error("database connection error: " + str(e))
            return None

    def insert_flight_data(self, flight_data):
        if not flight_data:
            logger.warning("no flight data")
            return

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            insert_query = """INSERT INTO flights (aircraft_id, callsign, time, longitude, latitude, altitude, speed, \
                                                   heading, on_ground)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (aircraft_id, time) DO NOTHING; \
                           """

            cursor.executemany(insert_query, flight_data)
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("inserted flight data")

        except Exception as e:
            logger.error("database insert error: " + str(e))
            conn.rollback()  #if mistake decline transaction
            conn.close()



