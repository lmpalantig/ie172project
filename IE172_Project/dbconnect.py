import psycopg2
import pandas as pd

def getdblocation():
    """Establish a connection to the PostgreSQL database."""
    db = psycopg2.connect(
        host='localhost',
        database='ie172project',  # Use your database name here
        user='postgres',
        password='112774',  # Replace with your password
        port=5432
    )
    return db

def modifyDB(sql, values):
    """
    Execute an SQL query that modifies the database (e.g., INSERT, UPDATE, DELETE).
    """
    db = getdblocation()
    cursor = db.cursor()
    try:
        cursor.execute(sql, values)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()

def getDataFromDB(sql, values=None, dfcolumns=None):
    """
    Fetch data from the database using an SQL query.
    Arguments:
    - sql: The SQL query string (can include placeholders like %s).
    - values: A tuple or list of values for placeholders (default: None).
    - dfcolumns: A list of column names for the resulting DataFrame (default: None).
    Returns:
    - A pandas DataFrame containing the query results.
    """
    db = getdblocation()
    cursor = db.cursor()
    try:
        cursor.execute(sql, values)
        rows = cursor.fetchall()
        if dfcolumns:
            return pd.DataFrame(rows, columns=dfcolumns)
        else:
            return pd.DataFrame(rows)
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()
