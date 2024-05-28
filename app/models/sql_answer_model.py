from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class SQLAnswerDataModel(BaseModel):
    result: List[Dict[str, Any]]
    answer: str


class SQLAnswerOutputModel(BaseModel):
    code: int
    message: str
    data: Optional[SQLAnswerDataModel] = None


class SQLAnswerDatasetModel(BaseModel):
    name: str
    url: str


class SQLAnswerModel(BaseModel):
    question: str
    query: str
    datasets: List[SQLAnswerDatasetModel]
