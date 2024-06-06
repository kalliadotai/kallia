from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ChartDataModel(BaseModel):
    url: str


class ChartOutputModel(BaseModel):
    code: int
    message: str
    data: Optional[ChartDataModel] = None


class ChartModel(BaseModel):
    type: Optional[str] = ""
    title: Optional[str] = ""
    xlabel: Optional[str] = ""
    ylabel: Optional[str] = ""
    data: List[Dict[str, Any]]
