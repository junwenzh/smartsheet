import os
import logging
import json
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, exc as sqlalchemy_exc
from update_or_append import update_or_append
from typing import Dict

load_dotenv()

logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def app():
    queries = load_queries('queries/queries.json')

    # Create database engines
    dw_engine = create_engine(create_connection_string('dw'), fast_executemany=True)
    qnxt_engine = create_engine(create_connection_string('qnxt'), fast_executemany=True)
    
    # Iterate over queries
    for name, query in queries.items():
        try:
            process_query(name, query, dw_engine, qnxt_engine)
        except Exception as e:
            logging.error(f"Error processing {name}: {e}")

def load_queries(filepath: str) -> Dict[str, Dict]:
    """Load queries from a JSON file."""
    with open(filepath) as json_file:
        return json.load(json_file)

def process_query(name: str, query: Dict, dw_engine, qnxt_engine):
    """Process a single query."""
    engine = get_engine(query['database'], dw_engine, qnxt_engine)
    sql = load_sql_file(query['sql'])

    try:
        for chunk in pd.read_sql(sql, engine, chunksize=1000):
            update_or_append(query['id'], chunk, query['primary_column'])
    except sqlalchemy_exc.SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError in query {name}: {e}")

def load_sql_file(filepath: str) -> str:
    """Load SQL query from a file."""
    with open(f'./queries/{filepath}') as sql_file:
        return sql_file.read()

def get_engine(database: str, dw_engine, qnxt_engine):
    """Get the engine for the specified database."""
    if database == 'dw':
        return dw_engine
    elif database == 'qnxt':
        return qnxt_engine
    else:
        raise ValueError(f"Database {database} not found")

def create_connection_string(server: str) -> str:
    """Create a connection string based on the server type."""
    address = os.getenv(f'{server}_ADDRESS')
    database = os.getenv(f'{server}_DATABASE')
    driver = 'ODBC Driver 17 for SQL Server'
    if server == 'dw':
        return f'DRIVER={driver};SERVER={address};DATABASE={database};Trusted_Connection=yes;'
    elif server == 'qnxt':
        username = os.getenv(f'{server}_USERNAME')
        password = os.getenv(f'{server}_PASSWORD')
        return f'DRIVER={driver};SERVER={address};DATABASE={database};UID={username};PWD={password};'
    else:
        raise ValueError(f"Server {server} configuration not found")

if __name__ == '__main__':
    app()
