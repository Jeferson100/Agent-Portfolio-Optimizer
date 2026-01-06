import json 
import yfinance as yf
import datetime
import logging
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

with open("../data/carteira_resultado.json", "r") as f:
    carteira_resultado = json.load(f)
    
with open("../data/resultado_carteira_futuro/trimestre_atual.json", "r") as f:
    trimestre_salvo = json.load(f)
    
logger.info("Dados da carteira carregados com sucesso.")
    
tics = list(carteira_resultado['tickers_weights'].keys())

date_now = datetime.datetime.now().strftime("%Y-%m-%d")

trimestre_atual = pd.date_range(end=date_now, periods=1, freq='QS').strftime("%Y-%m-%d")[0]

if trimestre_salvo != trimestre_atual:
    resultado_trimestre_anterior = pd.read_csv(f'../data/resultado_carteira_futuro/resultado_carteira_atual.csv')
    resultado_trimestre_anterior.to_csv(f'../data/resultado_carteira_futuro/resultado_carteira_{trimestre_atual}.csv')
    logger.info(f'Mudou o trimestre. Salvando novo arquivo com o nome resultado_carteira_{trimestre_atual}.csv')
else:
    logger.info(f'Mesmo trimestre!')

df_carteira = pd.DataFrame()

df_carteira.index = [i.split(".")[0] for i in carteira_resultado['tickers_weights'].keys()]

for tic in tics:
    precos = yf.download(tic, start=trimestre_atual, end=date_now)["Close"]
    valor_inicial = round(float(precos.iloc[0]),2)
    valor_final = round(float(precos.iloc[-1]),2)
    
    df_carteira.loc[tic.split(".")[0], 'preco_inicial'] = valor_inicial
    df_carteira.loc[tic.split(".")[0],'preco_atual'] = valor_final
    
    data_inicial = precos.index[0].strftime("%Y-%m-%d")
    data_final = precos.index[-1].strftime("%Y-%m-%d")

logger.info("Precos obtidos com sucesso.")

df_carteira.rename(columns={'preco_inicial': f'preco_inicial({data_inicial})', 'preco_atual': f'preco_atual({data_final})'}, inplace=True)

df_carteira['pesos_carteira'] = carteira_resultado['tickers_weights'].values()

df_carteira['pesos_carteira'] = df_carteira['pesos_carteira'].apply(lambda x: round((x/100),2))

df_carteira['diferenca_inicio_atual'] = df_carteira.iloc[:,1] - df_carteira.iloc[:,0] 

df_carteira['diferenca_inicio_atual(em %)'] = round(df_carteira['diferenca_inicio_atual'] / df_carteira.iloc[:,0],4)

df_carteira['valor_inicial_investido_1000'] = (df_carteira['pesos_carteira']*1000)

df_carteira['valor_atual_investido_1000'] = round((df_carteira['diferenca_inicio_atual(em %)'] + 1) * df_carteira['valor_inicial_investido_1000'],2)

logger.info("Valores computados com sucesso.")

with open("../data/resultado_carteira_futuro/trimestre_atual.json", "w") as f:
    json.dump(trimestre_atual,f)
    
df_carteira.to_csv('../data/resultado_carteira_futuro/resultado_carteira_atual.csv')

logger.info("Arquivo salvo com sucesso.")

logger.info("Processo finalizado com sucesso.")
    

    