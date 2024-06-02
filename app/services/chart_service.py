import uuid
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List
from app.constants import DOMAIN_NAME
from app.models import (
    ChartModel,
    ChartOutputModel,
    ChartDataModel,
)


class ChartService:
    def _get_values(self, data: ChartModel, key: str) -> List[str]:
        values = []
        for item in data.data:
            values.append(item[key])
        return values

    def _get_plot(self, data: ChartModel) -> str:
        if data.type == "line":
            plt.plot(self._get_values(data, data.x), self._get_values(data, data.y))
            plt.title(data.title)
            plt.xlabel(data.x)
            plt.ylabel(data.y)
        elif data.type == "bar":
            plt.bar(self._get_values(data, data.x), self._get_values(data, data.y))
            plt.title(data.title)
            plt.xlabel(data.x)
            plt.ylabel(data.y)
        else:
            df = pd.DataFrame(data.data)
            plt.table(cellText=df.values, colLabels=df.columns, loc="center")
            plt.title(data.title)
            plt.axis("off")
        path = f"chart/{uuid.uuid4()}.png"
        url = f"{DOMAIN_NAME}/{path}"
        plt.tight_layout()
        plt.savefig(f"assets/{path}")
        plt.close()
        return url

    def invoke(self, data: ChartModel) -> ChartOutputModel:
        try:
            url = self._get_plot(data)
        except:
            return ChartOutputModel(code=400, message="_get_plot error")
        return ChartOutputModel(
            code=200,
            message="success",
            data=ChartDataModel(url=url),
        )
