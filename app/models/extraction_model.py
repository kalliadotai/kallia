from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ExtractionOutputModel(BaseModel):
    structured_data: Dict[str, Any]


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
    examples: List[ExtractionExampleModel]
