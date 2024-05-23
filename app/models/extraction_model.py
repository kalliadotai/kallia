from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ExtractionDataModel(BaseModel):
    information: Dict[str, Any]


class ExtractionOutputModel(BaseModel):
    code: int
    message: str
    data: Optional[ExtractionDataModel] = None


class ExtractionExampleModel(BaseModel):
    input: str
    output: Dict[str, Any]


class ExtractionEnumModel(BaseModel):
    description: Optional[str] = ""
    value: str


class ExtractionFormatInstructionModel(BaseModel):
    name: str
    description: Optional[str] = ""
    type: str
    enum: Optional[List[ExtractionEnumModel]] = []


class ExtractionModel(BaseModel):
    question: str
    format_instructions: List[ExtractionFormatInstructionModel]
    examples: Optional[List[ExtractionExampleModel]] = []
