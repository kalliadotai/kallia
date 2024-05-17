import re
import json
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

    def _unwrap_tag(self, output: str) -> str:
        prefix = "SQLQuery:"
        suffix = "SQLResult"
        pattern = f"{prefix}(.*?){suffix}"
        content = re.compile(pattern, re.DOTALL)
        match = content.search(output)
        return match.group(1) if match else ""

    def _get_prompt(self, engine: str) -> str:
        return (
            self._sql_prompts[engine]
            if engine in self._sql_prompts
            else self._sql_prompts["sqlite"]
        )

    def invoke(self, data: SQLQueryModel) -> SQLQueryOutputModel:
        examples = json.dumps(jsonable_encoder(data.examples))
        table_info = json.dumps(jsonable_encoder(data.tables))
        chat = ChatGroq(temperature=0, model_name=MODEL_NAME)
        prompt = ChatPromptTemplate.from_messages(
            [("human", self._get_prompt(data.engine))]
        )
        chain = prompt | chat | StrOutputParser()
        raw_output = chain.invoke(
            {
                "question": data.question,
                "examples": examples,
                "table_info": table_info,
                "top_k": 5,
            }
        )
        output = " ".join(self._unwrap_tag(raw_output).splitlines()).strip()
        return {"data": output}
