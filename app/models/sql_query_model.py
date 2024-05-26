from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class SQLQueryDataModel(BaseModel):
    query: str
    result: Optional[List[Dict[str, Any]]] = []
    answer: Optional[str] = ""


class SQLQueryOutputModel(BaseModel):
    code: int
    message: str
    data: Optional[SQLQueryDataModel] = None


class SQLQueryExampleModel(BaseModel):
    input: str
    output: str


class SQLQueryEnumModel(BaseModel):
    description: Optional[str] = ""
    value: str


class SQLQueryColumnModel(BaseModel):
    name: str
    description: Optional[str] = ""
    type: str
    enum: Optional[List[SQLQueryEnumModel]] = []


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
    url: Optional[str] = ""


class SQLQueryModel(BaseModel):
    question: str
    tables: List[SQLQueryTableModel]
    examples: Optional[List[SQLQueryExampleModel]] = []
    engine: Optional[str] = ""
