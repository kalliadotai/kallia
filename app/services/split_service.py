import fitz
import requests
from typing import Any, Dict, List
from app.models import SplitModel, SplitOutputModel, SplitDataModel


class SplitService:
    def _is_empty(self, text: str) -> bool:
        return text.replace("\n", "").strip() == ""

    def _split(self, data: SplitModel) -> List[Dict[str, Any]]:
        response = requests.get(data.url)
        document = fitz.open(stream=response.content, filetype="pdf")
        lines = []
        for i in range(len(document)):
            page = document[i]
            for item in page.get_text("blocks"):
                text = item[4]
                if self._is_empty(text) == False:
                    lines.append({"page": i, "text": text})
        return lines

    def invoke(self, data: SplitModel) -> SplitOutputModel:
        try:
            lines = self._split(data)
        except:
            return SplitOutputModel(code=400, message="_split error")
        return SplitOutputModel(
            code=200,
            message="success",
            data=SplitDataModel(lines=lines),
        )
