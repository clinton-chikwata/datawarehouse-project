import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
     Copy song_data and log_data into staged tables
     :param cur: cursor object that allows Python to execute PostgreSQL commands in a database session
     :param conn:connection created to the database
    """
    for query in copy_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print(e)


def insert_tables(cur, conn):
    """
    Extract data from staged tables and tranform and  insert into the fact schema tables
    :param cur: cursor object that allows Python to execute PostgreSQL commands in a database session
    :param conn:connection created to the database
    """
    for query in insert_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print(e)



def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    conn = None
    try:
       conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    except psycopg2.Error as e:
        print(e)

    if conn:
        cur = conn.cursor()
        load_staging_tables(cur, conn)
        insert_tables(cur, conn)
        conn.close()

if __name__ == "__main__":
    main()