import torch
from typing import List
from sentence_transformers import CrossEncoder
from app.constants import RERANK_MODEL_NAME
from app.models import RerankModel, RerankOutputModel, RerankDataModel, RerankHitModel


class RerankService:
    def _rerank(self, data: RerankModel) -> List[RerankHitModel]:
        model = CrossEncoder(
            RERANK_MODEL_NAME,
            max_length=512,
            default_activation_function=torch.nn.Sigmoid(),
        )
        query_text_pairs = [[data.query, text] for text in data.documents]
        scores = model.predict(query_text_pairs)
        output = []
        for i, (text, score) in enumerate(zip(data.documents, scores)):
            output.append({"id": i, "score": score, "text": text})
        hits = sorted(output, key=lambda x: x["score"], reverse=True)
        return hits[: data.top_n]

    def invoke(self, data: RerankModel) -> RerankOutputModel:
        try:
            hits = self._rerank(data)
        except:
            return RerankOutputModel(code=400, message="_rerank error")
        return RerankOutputModel(
            code=200,
            message="success",
            data=RerankDataModel(hits=hits),
        )
