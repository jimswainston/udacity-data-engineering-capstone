import pandas as pd
import warnings
import pandas.io.sql as sqlio
import psycopg2
from psycopg2 import sql
from psycopg2.errors import ForeignKeyViolation


def primary_key_count_test(connection,table_name,primary_key):
    """
    Test to see if a database table has the same number of rows as unique primary keys. 
    Use this to check if every row in your table has a unique primary key.
    
    Parameters
    ----------
    connection  : a psycopg2 connection object
        Handles the connection to a PostgreSQL database instance
    table_name  : the name of the table being tested
    primary_key : the column name that contains the primary key for a record
    
    """

    conn = connection

    primary_key_check = sql.SQL("""select 
    count ({primary_key}) as total_rows, count (distinct {primary_key}) as unique_primary_keys
    from {table_name}
    """).format(table_name = sql.Identifier(table_name),
    primary_key = sql.Identifier(primary_key),)

    #use to debug issues with query composition
    #print(primary_key_check.as_string(conn))

    result = sqlio.read_sql_query(primary_key_check, conn)
    total_rows = result.iloc[0]['total_rows']
    total_primary_keys = result.iloc[0]['total_rows']
    
    if total_rows == total_primary_keys:
        print("Primary key check passed for table " + table_name + "\n")
        print("total_rows is " + str(total_rows) +"\n")
        print("total_primary_keys is " + str(total_rows))
    else:
        print("Primary Key Check failed for table" + table_name +  " Each row does not have a unique primary key\n")
        print("total_rows is " + str(total_rows) +  "\n")
        print("total_primary_keys is " + str(total_rows))
        

    
def foreign_key_constraint_test(connection,table_name,primary_key,key_value):

    conn = connection
    
    fk_constraint_check = sql.SQL("""
    delete from {table_name}
    where {primary_key} = {id}
    """).format(table_name = sql.Identifier(table_name),
    primary_key = sql.Identifier(primary_key),
    id = sql.Literal(key_value),
    )
    
    try:
        result = sqlio.read_sql_query(fk_constraint_check, conn)
    except sqlio.DatabaseError as e:
        if isinstance(e.__cause__, ForeignKeyViolation):
            print("Foreign key constraint test passed. Database threw the correct error as shown below \n")
            print(e.__cause__)
    else:
        print("Foreign key consraint test failed. Data deleted that could be referenced from another table")

        
  
    
  
        
