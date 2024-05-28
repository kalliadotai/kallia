import uuid
import duckdb
import pathlib
from typing import List
from datetime import datetime


def get_name() -> str:
    return uuid.uuid4()


def get_path() -> str:
    return f"db/{datetime.today().strftime('%Y/%m')}"


def create(db_name: str, db_path: str, table_names: List[str], urls: List[str]):
    pathlib.Path(db_path).mkdir(parents=True, exist_ok=True)
    with duckdb.connect(f"{db_path}/{db_name}.db") as con:
        for index, item in enumerate(table_names):
            con.sql(f"CREATE TABLE {item} AS SELECT * FROM '{urls[index]}'")


def find(db_name: str, db_path: str, query: str) -> str:
    with duckdb.connect(f"{db_path}/{db_name}.db") as con:
        output = con.sql(query).df()
    return output.to_json(orient="records")
