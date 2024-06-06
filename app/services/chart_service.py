import uuid
import pathlib
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List
from datetime import datetime
from app.constants import DOMAIN_NAME
from app.models import (
    ChartModel,
    ChartOutputModel,
    ChartDataModel,
)


class ChartService:
    def get_name(self) -> str:
        return uuid.uuid4()

    def get_path(self) -> str:
        return f"chart/{datetime.today().strftime('%y%m')}"

    def _get_values(self, data: ChartModel, key: str) -> List[str]:
        values = []
        for item in data.data:
            values.append(item[key])
        return values

    def _get_plot(self, data: ChartModel) -> str:
        if data.type == "line":
            plt.plot(
                self._get_values(data, data.xlabel), self._get_values(data, data.ylabel)
            )
            plt.title(data.title)
            plt.xlabel(data.xlabel)
            plt.xticks(rotation="vertical")
            plt.ylabel(data.ylabel)
        elif data.type == "bar":
            plt.bar(
                self._get_values(data, data.xlabel), self._get_values(data, data.ylabel)
            )
            plt.title(data.title)
            plt.xlabel(data.xlabel)
            plt.xticks(rotation="vertical")
            plt.ylabel(data.ylabel)
        elif data.type == "pie":
            plt.pie(
                self._get_values(data, data.ylabel),
                autopct="%1.1f%%",
                wedgeprops={"edgecolor": "w", "linewidth": 1, "width": 0.3},
                textprops={"color": "w", "weight": "bold"},
                pctdistance=0.85,
                labels=self._get_values(data, data.xlabel),
                labeldistance=None,
            )
            plt.legend()
            plt.title(data.title)
            plt.axis("equal")
        else:
            df = pd.DataFrame(data.data)
            plt.table(
                cellText=df.values,
                colLabels=df.columns,
                colColours=["skyblue"] * len(df.columns),
                loc="center",
            )
            plt.title(data.title)
            plt.axis("off")
        path = self.get_path()
        name = self.get_name()
        pathlib.Path(f"assets/{path}").mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(f"assets/{path}/{name}.png")
        plt.close()
        return f"{DOMAIN_NAME}/{path}/{name}.png"

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
