import re
import json
import pandas as pd
from typing import List
from sqlite3 import connect
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from app.constants import MODEL_NAME
from app.models import SQLQueryModel, SQLQueryOutputModel
from app.prompts import (
    MYSQL_PROMPT,
    POSTGRES_PROMPT,
    MSSQL_PROMPT,
    ORACLE_PROMPT,
    SQLITE_PROMPT,
    ANSWER_PROMPT,
)

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

    def _unwrap_tag(self, text: str) -> str:
        prefix = "SQLQuery:"
        suffix = "SQLResult"
        pattern = f"{prefix}(.*?){suffix}"
        content = re.compile(pattern, re.DOTALL)
        match = content.search(text)
        return match.group(1) if match else ""

    def _get_prompt(self, engine: str) -> str:
        return (
            self._sql_prompts[engine]
            if engine in self._sql_prompts
            else self._sql_prompts["sqlite"]
        )

    def _get_result(self, data: SQLQueryModel, query: str) -> str:
        connection = connect(":memory:")
        for table in data.tables:
            df = pd.read_csv(table.url)
            df.to_sql(name=table.name, con=connection)
        df = pd.read_sql(query, connection)
        return df.to_json(orient="records")

    def _get_query(self, data: SQLQueryModel) -> str:
        examples = json.dumps(jsonable_encoder(data.examples))
        table_info = json.dumps(jsonable_encoder(data.tables))
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        engine = "sqlite" if len(self._get_urls(data)) > 0 else data.engine
        prompt = ChatPromptTemplate.from_messages([("human", self._get_prompt(engine))])
        chain = prompt | chat | StrOutputParser()
        output = chain.invoke(
            {
                "question": data.question,
                "examples": examples,
                "table_info": table_info,
                "top_k": 5,
            }
        )
        return " ".join(self._unwrap_tag(output).splitlines()).strip()

    def _get_answer(self, query: str, result: str, question: str) -> str:
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        prompt = ChatPromptTemplate.from_messages([("human", ANSWER_PROMPT)])
        chain = prompt | chat | StrOutputParser()
        return chain.invoke({"question": question, "query": query, "result": result})

    def invoke(self, data: SQLQueryModel) -> SQLQueryOutputModel:
        query = self._get_query(data)
        if len(self._get_urls(data)) > 0:
            result = self._get_result(data, query)
            answer = self._get_answer(query, result, data.question)
            return SQLQueryOutputModel(
                query=query,
                result=json.loads(result),
                answer=answer,
            )
        return SQLQueryOutputModel(query=query)
