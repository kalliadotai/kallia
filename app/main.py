from typing import Annotated
from fastapi import Depends, FastAPI
from app.chains import SQLQueryChain, ExtractionChain, APIRequestChain
from app.models import (
    SQLQueryModel,
    SQLQueryOutputModel,
    ExtractionModel,
    ExtractionOutputModel,
    APIRequestModel,
    APIRequestOutputModel,
)

app = FastAPI()
v1 = FastAPI()


@v1.post("/sql_query")
def sql_query(
    data: SQLQueryModel,
    chain: Annotated[SQLQueryChain, Depends(SQLQueryChain)],
) -> SQLQueryOutputModel:
    return chain.invoke(data)


@v1.post("/extraction")
def extraction(
    data: ExtractionModel,
    chain: Annotated[ExtractionChain, Depends(ExtractionChain)],
) -> ExtractionOutputModel:
    return chain.invoke(data)


@v1.post("/api_request")
def api_request(
    data: APIRequestModel,
    chain: Annotated[APIRequestChain, Depends(APIRequestChain)],
) -> APIRequestOutputModel:
    return chain.invoke(data)


app.mount("/api/v1", v1)
