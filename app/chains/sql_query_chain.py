import json
import uuid
import duckdb
import pathlib
from datetime import datetime
from typing import List
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
    ANSWER_PROMPT,
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

    def _get_urls(self, data: SQLQueryModel) -> List[str]:
        urls = []
        for table in data.tables:
            if len(table.url) > 0:
                urls.append(table.url)
        return urls

    def _get_prompt(self, engine: str) -> str:
        return (
            self._sql_prompts[engine]
            if engine in self._sql_prompts
            else self._sql_prompts["sqlite"]
        )

    def _get_result(self, data: SQLQueryModel, query: str) -> str:
        db_name = uuid.uuid4()
        year = datetime.today().year
        month = datetime.today().month
        pathlib.Path(f"db/{year}/{month}").mkdir(parents=True, exist_ok=True)
        with duckdb.connect(f"db/{year}/{month}/{db_name}.db") as con:
            for table in data.tables:
                con.sql(f"CREATE TABLE {table.name} AS SELECT * FROM '{table.url}'")
            result = con.sql(query).df()
        return result.to_json(orient="records")

    def _get_query(self, data: SQLQueryModel) -> str:
        examples = json.dumps(jsonable_encoder(data.examples))
        tables = json.dumps(jsonable_encoder(data.tables))
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        engine = data.engine if len(self._get_urls(data)) == 0 else "sqlite"
        prompt = ChatPromptTemplate.from_messages([("human", self._get_prompt(engine))])
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

    def _get_answer(self, query: str, result: str, question: str) -> str:
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        prompt = ChatPromptTemplate.from_messages([("human", ANSWER_PROMPT)])
        chain = prompt | chat | StrOutputParser()
        return chain.invoke({"question": question, "query": query, "result": result})

    def invoke(self, data: SQLQueryModel) -> SQLQueryOutputModel:
        try:
            query = self._get_query(data)
        except:
            return SQLQueryOutputModel(code=400, message="_get_query error")
        if len(self._get_urls(data)) == 0 or len(query) == 0:
            return SQLQueryOutputModel(
                code=200,
                message="success",
                data=SQLQueryDataModel(query=query),
            )
        try:
            result = self._get_result(data, query)
        except:
            return SQLQueryOutputModel(code=400, message="_get_result error")
        try:
            answer = self._get_answer(query, result, data.question)
        except:
            return SQLQueryOutputModel(code=400, message="_get_answer error")
        return SQLQueryOutputModel(
            code=200,
            message="success",
            data=SQLQueryDataModel(
                query=query,
                result=json.loads(result),
                answer=answer,
            ),
        )
