import os
import logging
import pandas as pd
from dotenv import load_dotenv
from engine import create_connection_string, get_engine
from query_loader import load_queries, load_sql_file
from update_or_append import update_or_append
from sqlalchemy import exc as sqlalchemy_exc

load_dotenv()

logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def app():
    queries = load_queries('queries/queries.json')

    # Create database engines
    dw_engine = get_engine(create_connection_string('dw'))
    qnxt_engine = get_engine(create_connection_string('qnxt'))

    # Iterate over queries
    for name, query in queries.items():
        try:
            process_query(name, query, dw_engine, qnxt_engine)
        except Exception as e:
            logging.error(f"Error processing {name}: {e}")

def process_query(name: str, query: dict, dw_engine, qnxt_engine):
    """Process a single query."""
    engine = dw_engine if query['database'] == 'dw' else qnxt_engine
    sql = load_sql_file(f'queries/{query["sql"]}')

    try:
        for chunk in pd.read_sql(sql, engine, chunksize=1000):
            update_or_append(query['id'], chunk, query['primary_column'])
    except sqlalchemy_exc.SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError in query {name}: {e}")

if __name__ == '__main__':
    app()
