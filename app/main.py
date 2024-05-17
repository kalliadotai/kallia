from typing import Annotated
from fastapi import Depends, FastAPI
from app.chains import SQLQueryChain
from app.models import (
    SQLQueryModel,
    SQLQueryOutputModel,
)

app = FastAPI()
v1 = FastAPI()


@v1.post("/sql_query")
def query_generation(
    data: SQLQueryModel,
    chain: Annotated[SQLQueryChain, Depends(SQLQueryChain)],
) -> SQLQueryOutputModel:
    return chain.invoke(data)


app.mount("/api/v1", v1)
