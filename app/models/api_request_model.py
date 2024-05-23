from typing import List, Optional
from pydantic import BaseModel


class APIRequestDataModel(BaseModel):
    url: str


class APIRequestOutputModel(BaseModel):
    code: int
    message: str
    data: Optional[APIRequestDataModel] = None


class APIRequestExampleModel(BaseModel):
    input: str
    output: str


class APIRequestEnumModel(BaseModel):
    description: Optional[str] = ""
    value: str


class APIRequestParameterModel(BaseModel):
    name: str
    description: Optional[str] = ""
    type: str
    enum: Optional[List[APIRequestEnumModel]] = []


class APIRequestDocumentModel(BaseModel):
    url: str
    description: Optional[str] = ""
    parameters: List[APIRequestParameterModel]


class APIRequestModel(BaseModel):
    question: str
    document: APIRequestDocumentModel
    examples: Optional[List[APIRequestExampleModel]] = []
