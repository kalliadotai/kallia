from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from app.chains import (
    SQLQueryChain,
    SQLAnswerChain,
    ExtractionChain,
    APIRequestChain,
    APIResponseChain,
)
from app.models import (
    SQLQueryModel,
    SQLQueryOutputModel,
    SQLAnswerModel,
    SQLAnswerOutputModel,
    ExtractionModel,
    ExtractionOutputModel,
    APIRequestModel,
    APIRequestOutputModel,
    APIResponseModel,
    APIResponseOutputModel,
    ChartModel,
    ChartOutputModel,
)
from app.services import ChartService

app = FastAPI()
v1 = FastAPI()


@v1.post("/sql_query")
def sql_query(
    data: SQLQueryModel,
    chain: Annotated[SQLQueryChain, Depends(SQLQueryChain)],
) -> SQLQueryOutputModel:
    return chain.invoke(data)


@v1.post("/sql_answer")
def sql_answer(
    data: SQLAnswerModel,
    chain: Annotated[SQLAnswerChain, Depends(SQLAnswerChain)],
) -> SQLAnswerOutputModel:
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


@v1.post("/api_response")
def api_response(
    data: APIResponseModel,
    chain: Annotated[APIResponseChain, Depends(APIResponseChain)],
) -> APIResponseOutputModel:
    return chain.invoke(data)


@v1.post("/chart")
def chart(
    data: ChartModel,
    service: Annotated[ChartService, Depends(ChartService)],
) -> ChartOutputModel:
    return service.invoke(data)


app.mount("/api/v1", v1)

app.mount("/chart", StaticFiles(directory="assets/chart"), name="chart")
