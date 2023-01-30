import psycopg2
import constants
from sqlQueries import create_table_queries, drop_table_queries


def create_database():
    """
    - Creates and connects to the udacityprojectdb
    - Returns the connection and cursor to udacityprojectdb
    """
    
    # connect to default database
    conn = psycopg2.connect(constants.CONNECTION_STRING)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS udacityprojectdb")
    cur.execute("CREATE DATABASE udacityprojectdb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database udacityprojectdb
    conn = psycopg2.connect(constants.CONNECTION_STRING)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.

    Parameters
    ----------
    cur : a psycopg2 cursor object
        The cursor object that can be used to execute statements against the database
        
    conn : a psycopg2 connection object
        Handles the connection to a PostgreSQL database instance
    """
    for query in drop_table_queries:
        try: 
            cur.execute(query)
            #conn.commit()
        except psycopg2.Error as e: 
            print("Error: Dropping table")
            print (e)       
        


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 

    Parameters
    ----------
    cur : a psycopg2 cursor object
        The cursor object that can be used to execute statements against the database
        
    conn : a psycopg2 connection object
        Handles the connection to a PostgreSQL database instance
    """
    for query in create_table_queries:
        try: 
            cur.execute(query)
            #conn.commit()
        except psycopg2.Error as e: 
            print("Error: Creating table")
            print (e) 
        


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()