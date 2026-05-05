from typing import Any, List

import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

from ..coleta_dados import DadosIndicadoresTecnicos


class TratandoDadosIndicadores(DadosIndicadoresTecnicos):
    def coletando_indicadores(self) -> pd.DataFrame:
        return self.pegando_indicadores_tecnicos()

    def tratando_indicadores(self) -> pd.DataFrame:
        indicadores = self.coletando_indicadores()
        indicadores = indicadores.reset_index()
        indicadores["Date"] = indicadores["Date"].dt.strftime("%Y-%m-%d")  # type: ignore
        return indicadores

    def indicadores_data_loader(self) -> List[Any]:
        return DataFrameLoader(
            self.tratando_indicadores(), page_content_column="Date"
        ).load()
