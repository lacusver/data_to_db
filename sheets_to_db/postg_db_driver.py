import psycopg2
import psycopg2.extras
import sheets_to_db.exchange_rate as exchange_rate
import config as cfg

class Database():
    connection = None
    cursor = None
    user = cfg.DATABASE_CONFIG["user"]
    password = cfg.DATABASE_CONFIG["password"]
    host = cfg.DATABASE_CONFIG["host"]
    port = cfg.DATABASE_CONFIG["port"]
    DB_NAME = cfg.DATABASE_CONFIG["db_name"]
    TABLE_NAME = cfg.TABLE_CONFIG["table_name"]
    TABLE_COLS = cfg.TABLE_CONFIG["table_cols"]

    @classmethod
    def check_if_db_exists(cls, cursor):
        sql = f"SELECT datname FROM pg_database;"
        cursor.execute(sql)
        list_database = cursor.fetchall()
        return (cls.DB_NAME,) in list_database

    @classmethod
    def create_database(cls):
        if cls.connection is None:
            try:
                connection = psycopg2.connect(user=cls.user, 
                        password=cls.password, host=cls.host, port=cls.port)
                print("Connected to postgres db")
            except Exception as error:
                print(f"Error: Connection not established {error}")
            else:
                connection.autocommit = True
                cursor = connection.cursor()
                if not cls.check_if_db_exists(cursor):
                    sql = f"CREATE DATABASE {cls.DB_NAME}"
                    cursor.execute(sql)
                cursor.close()
                connection.close()

    @classmethod
    def create_table(cls):
        sql = f"""
                CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} 
                (
                    {cls.TABLE_COLS[0]} integer NOT NULL PRIMARY KEY,
                    {cls.TABLE_COLS[1]} numeric NOT NULL,
                    {cls.TABLE_COLS[2]} numeric NOT NULL,
                    {cls.TABLE_COLS[3]} numeric NOT NULL,
                    {cls.TABLE_COLS[4]} date NOT NULL
                )      
            """
        if cls.connection:
            try:
                cls.cursor.execute(sql)
            except Exception as e:
                print(f"Error while creating table {e}")
                cls.connection.rollback()
            else:
                cls.connection.commit()

    @classmethod
    def connect_to_db(cls):
        if cls.connection is None:
            try:
                cls.connection = psycopg2.connect(dbname=cls.DB_NAME, user=cls.user, 
                        password=cls.password, host=cls.host, port=cls.port)
                cls.cursor = cls.connection.cursor()
            except Exception as error:
                print(f"Error: Connection not established {error}")
            else:
                print("Connection established")

    @classmethod
    def get_data(cls):
        data = []
        sql = f"SELECT {cls.TABLE_COLS[0]}::text, {cls.TABLE_COLS[1]}::text, {cls.TABLE_COLS[2]}::text, TO_CHAR({cls.TABLE_COLS[4]}, 'dd.mm.yyyy') FROM {cls.TABLE_NAME}"
        if cls.connection:
            cls.cursor.execute(sql)
            data = cls.cursor.fetchall()
        
        return data
    
    @classmethod
    def add_new_data(cls, rows):
        sql = f"INSERT INTO {cls.TABLE_NAME} VALUES "
        try:
            args = ','.join(cls.cursor.mogrify("(%s,%s,%s,%s,%s)", (i[0], i[1], i[2], 
                round(float(i[2])*exchange_rate.ExchangeRate.get_exchange_rate(), 4), i[3])).decode('utf-8')
                for i in rows)
        
            cls.cursor.execute(sql + (args)) 
        except Exception as e:
            print(f"Error while adding new data into db {e}")
            cls.connection.rollback()
        else:
            cls.connection.commit()

    @classmethod
    def update_data(cls, rows):
        sql_query = f"""UPDATE {cls.TABLE_NAME} as t SET
                    {cls.TABLE_COLS[1]} = e.order_num::numeric,
                    {cls.TABLE_COLS[2]} = e.price_d::numeric,
                    {cls.TABLE_COLS[3]} = e.price_d::numeric * {exchange_rate.ExchangeRate.get_exchange_rate()},
                    {cls.TABLE_COLS[4]} = e.delivery_time::date
                    FROM (VALUES %s) AS e(id, order_num, price_d, delivery_time)
                    WHERE t.{cls.TABLE_COLS[0]} = e.id::int;"""
        try:
            psycopg2.extras.execute_values(cls.cursor, sql_query, rows, template=None, page_size=100)
        except Exception as e:
            print(f"Error while updating data in db {e}")
            cls.connection.rollback()
        else:
            cls.connection.commit()

    @classmethod
    def delete_rows(cls, rows_indx):
        if len(rows_indx)==1:
            sql = f"DELETE from {cls.TABLE_NAME} WHERE {cls.TABLE_COLS[0]} = {rows_indx[0]}"
        elif len(rows_indx)>1:
            sql  = f"DELETE from {cls.TABLE_NAME} WHERE {cls.TABLE_COLS[0]} in {rows_indx}"     
        try:
            cls.cursor.execute(sql)
        except Exception as e:
            print(f"Error while deleting rows in db {e}")
            cls.connection.rollback()
        else:
            cls.connection.commit()

    @classmethod
    def update_price(cls):
        sql = f"UPDATE {cls.TABLE_NAME} SET {cls.TABLE_COLS[3]} = {cls.TABLE_COLS[2]} * {exchange_rate.ExchangeRate.get_exchange_rate()};"
        try:
            cls.cursor.execute(sql)
        except Exception as e:
            print(f"Error while updating {cls.TABLE_COLS[3]} col in db {e}")
            cls.connection.rollback()
        else:
            cls.connection.commit()