import json
from typing import Any, Dict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from app.helpers import DatabaseHelper
from app.constants import MODEL_NAME
from app.models import SQLAnswerModel, SQLAnswerOutputModel, SQLAnswerDataModel
from app.prompts import SQL_ANSWER_PROMPT

load_dotenv()


class SQLAnswerChain:
    def _get_urls(self, data: SQLAnswerModel) -> List[str]:
        urls = []
        for item in data.datasets:
            urls.append(item.url)
        return urls

    def _get_table_names(self, data: SQLAnswerModel) -> List[str]:
        table_names = []
        for item in data.datasets:
            table_names.append(item.name)
        return table_names

    def _get_result(self, data: SQLAnswerModel) -> List[Dict[str, Any]]:
        db_name = DatabaseHelper.get_name()
        db_path = DatabaseHelper.get_path()
        table_names = self._get_table_names(data)
        urls = self._get_urls(data)
        DatabaseHelper.create(db_name, db_path, table_names, urls)
        output = DatabaseHelper.find(db_name, db_path, data.query)
        result = json.loads(output)
        return result if isinstance(result, list) else []

    def _get_answer(self, query: str, result: str, question: str) -> str:
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        prompt = ChatPromptTemplate.from_messages([("human", SQL_ANSWER_PROMPT)])
        chain = prompt | chat | StrOutputParser()
        return chain.invoke({"question": question, "query": query, "result": result})

    def invoke(self, data: SQLAnswerModel) -> SQLAnswerOutputModel:
        try:
            result = self._get_result(data)
        except:
            return SQLAnswerOutputModel(code=400, message="_get_result error")
        try:
            answer = self._get_answer(data.query, result, data.question)
        except:
            return SQLAnswerOutputModel(code=400, message="_get_answer error")
        return SQLAnswerOutputModel(
            code=200,
            message="success",
            data=SQLAnswerDataModel(result=result, answer=answer),
        )
