from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class APIResponseDataModel(BaseModel):
    summary: str


class APIResponseOutputModel(BaseModel):
    code: int
    message: str
    data: Optional[APIResponseDataModel] = None


class APIResponseEnumModel(BaseModel):
    description: Optional[str] = ""
    value: str


class APIResponseParameterModel(BaseModel):
    name: str
    description: Optional[str] = ""
    type: str
    enum: Optional[List[APIResponseEnumModel]] = []


class APIResponseDocumentModel(BaseModel):
    description: Optional[str] = ""
    parameters: List[APIResponseParameterModel]


class APIResponseModel(BaseModel):
    question: str
    document: APIResponseDocumentModel
    response: Dict[str, Any]
