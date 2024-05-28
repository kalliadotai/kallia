import json
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from app.helpers import CommonHelper
from app.constants import MODEL_NAME
from app.models import APIRequestModel, APIRequestOutputModel, APIRequestDataModel
from app.prompts import API_REQUEST_PROMPT

load_dotenv()


class APIRequestChain:
    def _get_url(self, data: APIRequestModel) -> str:
        examples = json.dumps(jsonable_encoder(data.examples))
        document = json.dumps(jsonable_encoder(data.document))
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        prompt = ChatPromptTemplate.from_messages([("human", API_REQUEST_PROMPT)])
        chain = prompt | chat | StrOutputParser()
        output = chain.invoke(
            {
                "question": data.question,
                "document": document,
                "examples": examples,
            }
        )
        url = CommonHelper.unwrap_tag("<url>", "</url>", output)
        return " ".join(url.splitlines()).strip()

    def invoke(self, data: APIRequestModel) -> APIRequestOutputModel:
        try:
            url = self._get_url(data)
        except:
            return APIRequestOutputModel(code=400, message="_get_url error")
        return APIRequestOutputModel(
            code=200,
            message="success",
            data=APIRequestDataModel(url=url),
        )
