import os
from sqlalchemy import create_engine

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

def get_engine(connection_string: str):
    """Get a SQLAlchemy engine."""
    return create_engine(connection_string, fast_executemany=True)
