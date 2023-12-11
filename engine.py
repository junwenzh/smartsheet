import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def create_connection_string(server: str) -> str:
    """Create a connection string based on the server type."""
    address = os.getenv(f'{server}_ADDRESS')
    database = os.getenv(f'{server}_DATABASE')
    driver = '{SQL Server}'
    if server == 'DW':
        return f'DRIVER={driver};SERVER={address};DATABASE={database};Trusted_Connection=yes;'
    elif server == 'QN':
        username = os.getenv(f'{server}_USERNAME')
        password = os.getenv(f'{server}_PASSWORD')
        return f'DRIVER={driver};SERVER={address};DATABASE={database};UID={username};PWD={password};'
    elif server == "DM":
        username = os.getenv(f'{server}_USERNAME')
        password = os.getenv(f'{server}_PASSWORD')
        return f'DRIVER={driver};SERVER={address};DATABASE={database};UID={username};PWD={password};'
    else:
        raise ValueError(f"Server {server} configuration not found")

def get_engine(connection_string: str):
    """Get a SQLAlchemy engine."""
    url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    return create_engine(url, fast_executemany=True)
