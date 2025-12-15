import warnings

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")


class PassivoTotalMenosDivida:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker=self.ticker)

    def passivo_nao_circulante(self) -> float:
        passivo_nao_circulante = self.stock.get_balancesheet(freq="yearly")
        if isinstance(passivo_nao_circulante, pd.DataFrame):
            if (
                "TotalNonCurrentLiabilitiesNetMinorityInterest"
                in passivo_nao_circulante.index
            ):
                out_terrenos = passivo_nao_circulante.loc[
                    "TotalNonCurrentLiabilitiesNetMinorityInterest"
                ][0]
            else:
                out_terrenos = 0
            if isinstance(out_terrenos, pd.Series):
                return float(out_terrenos.iloc[0])
            return float(out_terrenos)
        return 0.0

    def passivos_circulante(self) -> float:
        passivo_circulante = self.stock.get_balancesheet(freq="yearly")
        if isinstance(passivo_circulante, pd.DataFrame):
            if "CurrentLiabilities" in passivo_circulante.index:
                out_terrenos = passivo_circulante.loc["CurrentLiabilities"][0]
            else:
                out_terrenos = 0
            if isinstance(out_terrenos, pd.Series):
                return float(out_terrenos.iloc[0])
            return float(out_terrenos)
        return 0.0

    def divida_total(self) -> float:
        divida_total = self.stock.get_balancesheet(freq="yearly")
        if isinstance(divida_total, pd.DataFrame):
            if "TotalDebt" in divida_total.index:
                divida_total = divida_total.loc["TotalDebt"][0]
            else:
                divida_total = 0
            if isinstance(divida_total, pd.Series):
                return float(divida_total.iloc[0])
            return float(divida_total)
        return 0.0

    def valor_total_passivo_menos_divida(self) -> float:
        divida_tota = self.divida_total()
        passivo_circu = self.passivos_circulante()
        passivo_nao_circu = self.passivo_nao_circulante()
        return passivo_circu + passivo_nao_circu - divida_tota
