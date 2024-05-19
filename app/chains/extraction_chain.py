import json
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from app.constants import MODEL_NAME
from app.models import ExtractionModel, ExtractionOutputModel
from app.prompts import EXTRACTION_PROMPT

load_dotenv()


class ExtractionChain:
    def _extract(self, data: ExtractionModel) -> str:
        examples = json.dumps(jsonable_encoder(data.examples))
        format_instructions = json.dumps(jsonable_encoder(data.format_instructions))
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        prompt = ChatPromptTemplate.from_messages([("human", EXTRACTION_PROMPT)])
        chain = prompt | chat | StrOutputParser()
        return chain.invoke(
            {
                "question": data.question,
                "type_description": format_instructions,
                "examples": examples,
            }
        )

    def invoke(self, data: ExtractionModel) -> ExtractionOutputModel:
        try:
            information = self._extract(data)
        except:
            return ExtractionOutputModel(code=400, message="_extract error")
        return ExtractionOutputModel(
            code=200,
            message="success",
            data=json.loads(information),
        )
