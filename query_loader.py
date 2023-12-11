import json
from typing import Dict

def load_queries(filepath: str) -> Dict[str, Dict]:
    """Load queries from a JSON file."""
    with open(filepath) as json_file:
        return json.load(json_file)

def load_sql_file(filepath: str) -> str:
    """Load SQL query from a file."""
    with open(filepath) as sql_file:
        return sql_file.read()
