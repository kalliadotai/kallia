import json
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from app.constants import MODEL_NAME
from app.models import APIResponseModel, APIResponseOutputModel, APIResponseDataModel
from app.prompts import API_RESPONSE_PROMPT

load_dotenv()


class APIResponseChain:
    def _summarize(self, data: APIResponseModel) -> str:
        document = json.dumps(jsonable_encoder(data.document))
        response = json.dumps(jsonable_encoder(data.response))
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        prompt = ChatPromptTemplate.from_messages([("human", API_RESPONSE_PROMPT)])
        chain = prompt | chat | StrOutputParser()
        return chain.invoke(
            {
                "question": data.question,
                "document": document,
                "response": response,
            }
        )

    def invoke(self, data: APIResponseModel) -> APIResponseOutputModel:
        try:
            summary = self._summarize(data)
        except:
            return APIResponseOutputModel(code=400, message="_summarize error")
        return APIResponseOutputModel(
            code=200,
            message="success",
            data=APIResponseDataModel(summary=summary),
        )
