from typing import List, Optional
from pydantic import BaseModel


class RerankHitModel(BaseModel):
    id: int
    score: float
    text: str


class RerankDataModel(BaseModel):
    hits: List[RerankHitModel]


class RerankOutputModel(BaseModel):
    code: int
    message: str
    data: Optional[RerankDataModel] = None


class RerankModel(BaseModel):
    query: str
    documents: List[str]
    top_n: Optional[int] = 10
