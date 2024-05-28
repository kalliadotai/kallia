import json
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from app.constants import MODEL_NAME
from app.models import SQLQueryModel, SQLQueryOutputModel, SQLQueryDataModel
from app.prompts import (
    MYSQL_PROMPT,
    POSTGRES_PROMPT,
    MSSQL_PROMPT,
    ORACLE_PROMPT,
    SQLITE_PROMPT,
)
from app.utils import unwrap_tag

load_dotenv()


class SQLQueryChain:
    _sql_prompts = {
        "mysql": MYSQL_PROMPT,
        "postgres": POSTGRES_PROMPT,
        "mssql": MSSQL_PROMPT,
        "oracle": ORACLE_PROMPT,
        "sqlite": SQLITE_PROMPT,
    }

    def _get_prompt(self, engine: str) -> str:
        return (
            self._sql_prompts[engine]
            if engine in self._sql_prompts
            else self._sql_prompts["sqlite"]
        )

    def _get_query(self, data: SQLQueryModel) -> str:
        examples = json.dumps(jsonable_encoder(data.examples))
        tables = json.dumps(jsonable_encoder(data.tables))
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        prompt = ChatPromptTemplate.from_messages(
            [("human", self._get_prompt(data.engine))]
        )
        chain = prompt | chat | StrOutputParser()
        output = chain.invoke(
            {
                "question": data.question,
                "examples": examples,
                "tables": tables,
                "top_k": 5,
            }
        )
        query = unwrap_tag("SQLQuery:", "SQLResult", output)
        return " ".join(query.splitlines()).strip()

    def invoke(self, data: SQLQueryModel) -> SQLQueryOutputModel:
        try:
            query = self._get_query(data)
        except:
            return SQLQueryOutputModel(code=400, message="_get_query error")
        return SQLQueryOutputModel(
            code=200,
            message="success",
            data=SQLQueryDataModel(query=query),
        )
