import asyncio
import time
import logging
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
from portfolio_optimizer import BuildGraphAvaliacaoTics, StateClassification, BuildGraphCriadorCarteira, StateCarteira
import yfinance as yf
from typing import List
import asyncio
import pandas as pd
from bcb import sgs
import pandas as pd
from sklearn.covariance import LedoitWolf
import numpy as np
from scipy.optimize import minimize
from IPython.display import display
import matplotlib.pyplot as plt
import datetime
import time
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

graph_tics = BuildGraphAvaliacaoTics()

graph_build = graph_tics.compile()


async def classificar_tics(tic, data_inicio, data_fim):
    
    response = await graph_build.ainvoke(
            StateClassification(
                {
                    "tic": tic,
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                    "avaliacao_analise": "",
                    "description_avaliacao_analise": "",
                    "interacao": 0,
                }
            )
        )

    return response

async def rodando_tics(sequencia_datas, tics):
    result_tics_datas = {}
    for data_inicio, data_fim in sequencia_datas.items():
        results_tics = {}
        for tic in tics:
            try:
                results_tics[tic] = await classificar_tics(tic, data_inicio, data_fim)
            except Exception as e:
                logger.error(f"❌ Erro ao processar {tic}: {e}")
                results_tics[tic] = {}
            time.sleep(1)
            logger.info(f"✅ {tic} concluído para a {data_inicio} ate {data_fim}!")
        result_tics_datas[f"{data_inicio}_to_{data_fim}"] = results_tics
        logger.info(f"Conclusao para as datas:{data_inicio} e {data_fim}")
    return result_tics_datas

async def rodando_tics_sem_sequencia(data_inicio, data_fim, tics):
    results_tics = {}
    for tic in tqdm(tics):
        try:
            results_tics[tic] = await classificar_tics(tic, data_inicio, data_fim)
        except Exception as e:
            logger.error(f"❌ Erro ao processar {tic}: {e}")
            results_tics[tic] = None
        logger.info(f"✅ {tic} concluído!")
    return results_tics
    

async def _invoke_tic(tic: str, data_inicio: str, data_fim: str):
    try:
        start = time.time()
        logger.info(f"🚀 Iniciando {tic}")
        
        result = await graph_build.ainvoke(
            StateClassification({
                "tic": tic,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "avaliacao_analise": "",
                "description_avaliacao_analise": "",
                "interacao": 0,
            })
        )
        
        elapsed = time.time() - start
        logger.info(f"✅ {tic} concluído em {elapsed:.2f}s")
        return result
    except KeyError as e:
        logger.error(f"❌ Tic nao encontrado {tic} para {data_inicio} a {data_fim}")
        return None
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar {tic}: {e}")
        return None


async def run_all_tics(tics, data_inicio: str, data_fim: str):
    start_total = time.time()
    
    tasks = [_invoke_tic(tic, data_inicio, data_fim) for tic in tics]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed_total = time.time() - start_total
    logger.info(f"⏱️  Tempo total: {elapsed_total:.2f}s")
    
    return dict(zip(tics, results_list))

def transformando_data_frame_para_markdown(results):
    try:
        results_pd = pd.DataFrame.from_dict(results).T
    except Exception as e:
        results_pd = pd.DataFrame.from_dict(results, orient="index").T
    dados_markdown = results_pd.loc[:, ["classification", "analysis"]].reset_index().rename(columns={"index": "tic"}).to_markdown()
    return dados_markdown

def correlacao(tics:List[str], data_inicio: str, data_fim: str):
    tics_yf = [tic + ".SA" for tic in tics]

    df = yf.download(tics_yf, start=data_inicio, end=data_fim, interval="1mo")["Close"]
    
    returns = df.pct_change()[4:]
    # Calcula a matriz de correlação
    correlacao = returns.corr()

    return correlacao.to_markdown()


def markowitz_opt(returns: pd.DataFrame):
    # === Estatísticas ===
    mu = returns.mean()  # retorno médio esperado
    # matriz de covariância com Ledoit–Wolf shrinkage
    lw = LedoitWolf().fit(returns)
    Sigma = lw.covariance_

    n = len(mu)

    # Retorno alvo (por exemplo, retorno médio da amostra de treino)
    target_return = mu.mean()

    # === Funções auxiliares ===
    def portfolio_performance(w, mu, Sigma):
        ret = np.dot(w, mu)
        vol = np.sqrt(np.dot(w.T, np.dot(Sigma, w)))
        return ret, vol

    def objective(w, mu, Sigma, target):
        ret, vol = portfolio_performance(w, mu, Sigma)
        return vol  # minimiza a volatilidade

    # === Restrições ===
    constraints = (
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},              # soma = 1
        {'type': 'eq', 'fun': lambda w: np.dot(w, mu) - target_return},  # retorno alvo
    )
    bounds = tuple((0, 1) for _ in range(n))  # sem short

    # === Otimização ===
    w0 = np.repeat(1/n, n)
    opt = minimize(
        objective, w0, args=(mu, Sigma, target_return),
        method='SLSQP', bounds=bounds, constraints=constraints
    )

    weights = opt.x

    # === Aplicação dos pesos ao conjunto de retornos ===
    markowitz_cr = (1 + (weights * returns).sum(axis=1)).cumprod()

    weights_markowitz = pd.DataFrame(
        np.tile(weights, (len(returns), 1)),  # repete o vetor em todas as linhas
        index=returns.index,
        columns=returns.columns
    )

    return weights_markowitz, markowitz_cr

def get_selic_multiplos_periodos(data_inicio, data_fim, anos_por_janela=5):
    """
    Busca dados da SELIC em janelas de X anos para contornar limitação da API
    """
    inicio = pd.to_datetime(data_inicio)
    fim = pd.to_datetime(data_fim)
    
    # Lista para armazenar os dataframes
    dados_completos = []
    
    # Criar janelas
    current_start = inicio
    
    while current_start < fim:
        current_end = min(current_start + pd.DateOffset(years=anos_por_janela), fim)
        
        print(f"Buscando dados de {current_start.date()} até {current_end.date()}...")
        
        try:
            # Fazer requisição para a janela atual
            dados_janela = sgs.get({'selic': 11, 
                                    #'cdi' :12
                                    }, 
                                   start=current_start.strftime('%Y-%m-%d'),
                                   end=current_end.strftime('%Y-%m-%d'))
            
            dados_completos.append(dados_janela)
            print(f"  ✓ {len(dados_janela)} registros obtidos")
            
        except Exception as e:
            print(f"  ✗ Erro ao buscar dados: {e}")

        current_start = current_end + pd.Timedelta(days=1)

    if dados_completos:
        selic_completo = pd.concat(dados_completos)
        selic_completo = selic_completo[~selic_completo.index.duplicated(keep='first')]
        selic_completo = selic_completo.sort_index()
        
        print(f"\n✓ Total de registros: {len(selic_completo)}")
        print(f"✓ Período: {selic_completo.index.min().date()} até {selic_completo.index.max().date()}")
        
        return selic_completo
    else:
        print("Nenhum dado foi obtido!")
        return None
    
def daily_returns(prices):
    return prices.pct_change()[1:]

def daily_returns_carteira(prices, pesos):
    pesos_porcentagem = pesos_porcentagem = [peso/100 for peso in pesos]
    variacao_diaria_carteira = (prices.pct_change()[1:] * (pesos_porcentagem)).sum(axis=1)
    return variacao_diaria_carteira

def annualized_volatility(daily_ret, trading_days=252):
    return daily_ret.std() * np.sqrt(trading_days)

def annualized_mean_return(daily_ret, trading_days=252):
    return daily_ret.mean() * trading_days

def cagr(prices):
    days = (prices.index[-1] - prices.index[0]).days
    years = days / 365.25
    return (prices.iloc[-1] / prices.iloc[0])**(1/years) - 1 if years > 0 else np.nan

def max_drawdown(prices):
    cum_max = prices.cummax()
    drawdowns = (prices - cum_max) / cum_max
    return drawdowns.min()

def avg_drawdown(prices):
    dd = (prices / prices.cummax()) - 1
    negatives = dd < 0
    groups = (negatives.astype(int).diff() != 0).cumsum()
    avg_dds = []
    for _, grp in dd.groupby(groups):
        if (grp < 0).any():
            avg_dds.append(grp.min())
    return np.mean(avg_dds) if avg_dds else 0.0

def calmar_ratio(prices):
    ann_ret = cagr(prices)
    mdd = max_drawdown(prices)
    return ann_ret / abs(mdd) if mdd != 0 else np.nan

def sortino_ratio(daily_ret, required_return=0.0, trading_days=252):
    rr_daily = (1 + required_return)**(1/trading_days) - 1
    downside = daily_ret[daily_ret < rr_daily] - rr_daily
    if downside.size == 0:
        return np.nan
    dd = np.sqrt((downside**2).mean()) * np.sqrt(trading_days)
    ann_ret = annualized_mean_return(daily_ret, trading_days)
    return (ann_ret - required_return) / dd if dd != 0 else np.nan

def compute_metrics(price_df):
    metrics = {}
    for col in price_df.columns:
        p = price_df[col].dropna()
        #dr = daily_returns_carteira(p, pesos)
        metrics[col] = {
            "retorno_medio_anual": annualized_mean_return(p),
            "volatilidade_anual": annualized_volatility(p),
            "cagr": cagr(p),
            "max_drawdown": max_drawdown(p),
            "avg_drawdown": avg_drawdown(p),
            "calmar": calmar_ratio(p),
            "sortino": sortino_ratio(p)
        }
    return pd.DataFrame(metrics).T


def normalizar_pesos(weights_dict, target_sum=100, tolerancia=0.01):
    """
    Normaliza os pesos para somarem exatamente o target_sum.
    
    Args:
        weights_dict: Dicionário com os pesos {ticker: peso}
        target_sum: Soma alvo (padrão: 100)
        tolerancia: Tolerância para considerar soma correta (padrão: 0.01)
    
    Returns:
        Dicionário com pesos normalizados
    """
    total_atual = sum(weights_dict.values())
    diferenca = abs(total_atual - target_sum)
    
    # Se já está dentro da tolerância, retorna o original
    if diferenca <= tolerancia:
        logger.info(f"✓ Pesos já somam {total_atual:.2f}% (dentro da tolerância)")
        return weights_dict
    
    # Normalização proporcional (melhor que distribuir igualmente)
    fator_normalizacao = target_sum / total_atual
    weights_normalizados = {
        ticker: peso * fator_normalizacao 
        for ticker, peso in weights_dict.items()
    }
    
    # Log da correção
    logger.warning(
        f"⚠ Pesos ajustados: {total_atual:.2f}% → {target_sum:.2f}% "
        f"(fator: {fator_normalizacao:.4f})"
    )
    
    # Verificação final
    soma_final = sum(weights_normalizados.values())
    logger.info(f"✓ Soma final: {soma_final:.4f}%")
    
    return weights_normalizados

class ComputandoMetricas:
    def __init__(self, data_inicio, 
                 data_fim, 
                 carteira,
                 valor_investido=1000):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.carteira = carteira
        self.valor_investido = valor_investido
        self.ibov, self.df = self.carregando_dados()
        self.tics_selecionados, self.pesos_carteira = self.ajustando_pesos_carteira()
    
        
    def carregando_dados(self):
        tics_selecionados = [tic if tic.endswith(".SA") else f"{tic}.SA" for tic in self.carteira.keys()]
        ibov = yf.download("^BVSP", start=self.data_inicio, end=self.data_fim)["Close"]
        df = yf.download(tics_selecionados, start=self.data_inicio, end=self.data_fim)["Close"]
        df.dropna(axis=1, how='all', inplace=True)
        return ibov, df
    
    def cumulative_returns(self):
        return (self.df.apply(daily_returns)+1).cumprod()
    
    def ajustando_pesos_carteira(self):
        dict_carteiras = self.carteira.copy()
        tic_validos = list(self.df.columns)
        carteira_valida = {key: value for key, value in dict_carteiras.items() if key + ".SA" in tic_validos}
        carteira_valida = {
            key: value for key, value in dict_carteiras.items()
            if (key.endswith(".SA") and key in tic_validos) or 
            (not key.endswith(".SA") and key + ".SA" in tic_validos)
        } 
        carteira_pesos_acoes_validos = normalizar_pesos(carteira_valida)
        tics_selecionados = list(carteira_pesos_acoes_validos.keys())
        pesos = list(carteira_pesos_acoes_validos.values()) 
        return tics_selecionados, pesos
        
    def computando_marcowitz(self):
        weights_markowitz, markowitz_cr = markowitz_opt(self.df.pct_change().dropna())
        return weights_markowitz, markowitz_cr
        
    def daily_returns_carteira_markowitz(self):
        weights_markowitz, markowitz_cr = self.computando_marcowitz()
        pesos_markowitz = [peso*100 for peso in weights_markowitz.iloc[-1].to_list()]
        retornos_carteira_markowitz = daily_returns_carteira(self.df, pesos_markowitz)
        return retornos_carteira_markowitz
    
    def retornos_diarios_carteira(self):
        retornos_diarios_carteira = daily_returns_carteira(self.df, self.pesos_carteira)
        return retornos_diarios_carteira
    
    def retornos_diarios_ibov(self):
        retorno_diario = self.ibov.pct_change()[1:]
        return retorno_diario
    
    def data_frame_comparacao_retorno_diario(self):
        retornos_carteira = self.retornos_diarios_carteira()
        retornos_ibov = self.retornos_diarios_ibov()
        retornos_markowitz = self.daily_returns_carteira_markowitz()
        comparacao_carteira = pd.concat([retornos_carteira, 
                                 retornos_ibov, 
                                 retornos_markowitz], axis=1,).rename(columns={0: "Carteira", 
                                                                               "^BVSP": "IBOV", 
                                                                               1: "Markowitz"})
        return comparacao_carteira
    
    def metrica_comparacao_carteira_ibov_retornos_markowitz(self):
        comparacao_carteira = self.data_frame_comparacao_retorno_diario()
        comp_metrics = compute_metrics(comparacao_carteira)
        return comp_metrics
    
    def retorno_menetario_ibov(self):
        ibov_retornos = (self.ibov.pct_change()[1:]+1).cumprod() *self.valor_investido
        return ibov_retornos
    
    def retorno_carteira_monetario(self):
        pesos_frac = [p/100 for p in self.pesos_carteira]
        valor_investido_carteira = [self.valor_investido * peso for peso in pesos_frac]
        retorno_carteira = (self.cumulative_returns() * valor_investido_carteira).sum(axis=1)
        return retorno_carteira
    
    def data_frame_comparacao_retorno_monetario(self):
        ibov_retornos = self.retorno_menetario_ibov()
        retorno_carteira = self.retorno_carteira_monetario()
        _ , markowitz_cr = self.computando_marcowitz()
        selic = self.retorno_selic()

        retorno_acumulado_monetario = pd.concat([ibov_retornos, retorno_carteira, markowitz_cr*self.valor_investido, selic], axis=1).rename(columns={"^BVSP": "IBOV", 0: "Carteira", 1: "Markowitz", "selic":"Selic"})
        return retorno_acumulado_monetario
    
    def retorno_selic(self):
        selic = get_selic_multiplos_periodos(self.data_inicio, self.data_fim)
        selic_acumulada =  ((selic/100 + 1).cumprod())*self.valor_investido
        return selic_acumulada
    
    def print_results(self, save_path="../data/"):
        import os
        from datetime import datetime
        
        # Criar diretório se não existir
        os.makedirs(save_path, exist_ok=True)
    
        
        metrics = self.metrica_comparacao_carteira_ibov_retornos_markowitz()
        retorno_acumulado_monetario = self.data_frame_comparacao_retorno_monetario()
        
        print("\n" + "="*40)
        print("📊 Métricas de Comparação das Carteiras")
        print("="*40)
        
        # Salvar métricas em CSV
        metrics_file = os.path.join(save_path, "metricas.csv")
        metrics.to_csv(metrics_file)
        print(f"✅ Métricas salvas em: {metrics_file}")
    
        display(metrics.style.set_caption("Métricas das Carteiras").background_gradient(cmap="Blues"))
    
        plt.figure(figsize=(10, 6))
        cores = {'IBOV': '#1f77b4', 'Carteira': '#2ca02c', 'Markowitz': '#d62728', 'Selic': "#d66427"}

        for nome in ['IBOV', 'Carteira', 'Markowitz', 'Selic']:
            plt.plot(
                retorno_acumulado_monetario.index,
                retorno_acumulado_monetario[nome],
                label=nome,
                color=cores[nome]
            )
            ultimo_x = retorno_acumulado_monetario.index[-2]
            ultimo_y = retorno_acumulado_monetario[nome].iloc[-2]
            plt.text(
                ultimo_x, ultimo_y,
                f'R$ {ultimo_y:,.2f}',
                color=cores[nome],
                fontsize=11,
                va='center',
                fontweight='bold'
            )

        plt.legend()
        plt.xlabel("Data")
        plt.ylabel("Retorno Monetário da Carteira")
        plt.title(f"Retorno Monetário da Carteira vs Ibov vs Markowitz (Valor inicial de R$ {self.valor_investido})")
        
        # Salvar gráfico
        grafico_file = os.path.join(save_path, f"grafico_retornos.png")
        plt.savefig(grafico_file, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico salvo em: {grafico_file}")
        
        plt.show()
        
        # Salvar retornos acumulados em CSV
        retornos_file = os.path.join(save_path, f"retornos_acumulados.csv")
        retorno_acumulado_monetario.to_csv(retornos_file)
        print(f"✅ Retornos acumulados salvos em: {retornos_file}")
        
        print("\n" + "="*40)
        
        return retorno_acumulado_monetario
    

def sequencia_datas(start, end, freq="QS"):
    
    data_hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    
    periodo_datas = pd.date_range(start=start, end=data_hoje, freq=freq)
    
    datas_dict = {}
    
    for data in periodo_datas:
        novos_trimestres = pd.date_range(end=data, periods=8, freq='QS')
        data_inicio = novos_trimestres[0].strftime("%Y-%m-%d")
        data_fim = novos_trimestres[-1].strftime("%Y-%m-%d")
        if data_fim > data_hoje:
            data_fim = data_hoje
            datas_dict[data_inicio] = data_fim
        else:
            datas_dict[data_inicio] = data_fim
        
    datas_dict = {k: v for k, v in datas_dict.items() if v <= end}

    return datas_dict
    

def selecionar_tics_bom_excelente(dict_tics):
    classificacao_boa = [
   "good", "excellent",
    ]
    response = {}
    for k, v in dict_tics.items():
        try:
            if v is not None and v.get('classification').lower() in classificacao_boa:
                response[k] = v
        except Exception as e:
            continue
            logger.error(f"Erro ao processar {k}: {e}")
    
    return response

def verificando_valores_nulos(pesos_carteiras, precos_carteira):
    #dict_keys = pesos_carteiras[values]['tickers_weights'].copy()
    null = precos_carteira.isna().any()
    list_name_null = precos_carteira.loc[:,null].columns.to_list()
    
    dict_keys = {
        (key if key.endswith(".SA") else f"{key}.SA"): value 
        for key, value in pesos_carteiras.items()
    }
    valor_do_tic_null = 0
    for tic in list_name_null:
        valor_do_tic_null += dict_keys[tic]
        dict_keys.pop(tic)  
    
    quantidade_sobrou = len(dict_keys)
    
    if quantidade_sobrou == 0:
        return {}  # Evitar divisão por zero
    
    valor_para_cada_tic = valor_do_tic_null / quantidade_sobrou
    
    dict_com_novos_valores = {}
    for key, value in dict_keys.items():
        dict_com_novos_valores[key] = value + valor_para_cada_tic
    
    return dict_com_novos_valores


def daily_returns(prices):
    return prices.pct_change()[1:]

def cumulative_returns(df):
    return (df.apply(daily_returns)+1).cumprod()

def retorno_carteira_monetario(df, pesos, valor_investido):
    pesos_frac = [p/100 for p in pesos]
    valor_investido_carteira = [valor_investido * peso for peso in pesos_frac]
    retorno_carteira = (cumulative_returns(df) * valor_investido_carteira).sum(axis=1)
    return retorno_carteira

def retorno_percentual_acao_individual(pesos_carteiras, precos_carteira):
    """pesos_frac = [p/100 for p in pesos_carteiras[chaves[keys]].values()]
    valor_investido_carteira = [1000 * peso for peso in pesos_frac]
    retorno_carteira = (cumulative_returns(precos_carteira[chaves[keys]]) * valor_investido_carteira)"""
    
    
    pesos_frac = [p/100 for p in pesos_carteiras.values()]
    valor_investido_carteira = [1000 * peso for peso in pesos_frac]
    
    # Usar diretamente precos_df (já é o DataFrame correto)
    retorno_carteira = cumulative_returns(precos_carteira) * valor_investido_carteira
    
    retorno_percentual = retorno_carteira.apply(
        lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0] * 100
    )
    return retorno_percentual