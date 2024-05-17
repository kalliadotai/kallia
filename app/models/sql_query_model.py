from typing import List, Optional
from pydantic import BaseModel


class SQLQueryOutputModel(BaseModel):
    data: str


class SQLQueryExampleModel(BaseModel):
    input: str
    output: str


class SQLQueryColumnModel(BaseModel):
    name: str
    description: Optional[str] = ""
    type: str


class SQLQueryReferencesModel(BaseModel):
    table_name: str
    column_name: str


class SQLQueryForeignKeyModel(BaseModel):
    name: str
    references: SQLQueryReferencesModel


class SQLQueryTableModel(BaseModel):
    name: str
    description: Optional[str] = ""
    columns: List[SQLQueryColumnModel]
    primary_keys: Optional[List[str]] = []
    foreign_keys: Optional[List[SQLQueryForeignKeyModel]] = []


class SQLQueryModel(BaseModel):
    question: str
    tables: List[SQLQueryTableModel]
    examples: List[SQLQueryExampleModel]
    engine: Optional[str] = ""
