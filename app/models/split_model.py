from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class SplitDataModel(BaseModel):
    lines: List[Dict[str, Any]]


class SplitOutputModel(BaseModel):
    code: int
    message: str
    data: Optional[SplitDataModel] = None


class SplitModel(BaseModel):
    url: str
