import warnings
from typing import Any, List, cast

import pandas as pd

warnings.filterwarnings("ignore")


class VerificadorTicks:
    def __init__(self, tic: str):
        self.tic = tic

    def obtendo_ticks(self) -> List[Any]:
        pd_tic = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv"
        )
        list_tic = cast(List[str], pd_tic["tic"].to_list())

        return list_tic

    def verificando_ticks(self) -> bool:
        if self.tic in self.obtendo_ticks():
            return True
        else:
            return False
