import pandas as pd
import logging
import warnings
from langchain_nvidia_ai_endpoints import ChatNVIDIA 
from dotenv import load_dotenv
import json
import datetime

load_dotenv()

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

carteira_atual = pd.read_csv("../data/resultado_carteira_futuro/resultado_carteira_atual.csv", index_col=0)

try:
    with open('../README.md', 'r', encoding='utf-8') as file:
        readme_content = file.readlines()
except UnicodeDecodeError:
    with open('../README.md', 'r', encoding='latin-1') as file:
        readme_content = file.readlines()
        
with open("../data/resultado_carteira_futuro/variacao_carteira_porcentagem.json", "r") as f:
    variacao_carteira_porcentagem = json.load(f)
     
logger.info("Arquivo README.md carregado com sucesso.")

carteira_atual_markdown = carteira_atual.to_markdown()

PROMPT = """
You are a senior investment analyst specialized in stock portfolio analysis.

</Context>
You will receive data from a stock portfolio for the current quarter with the following information:
{carteira}

The variation of the portfolio in this period is {variacao_carteira_porcentagem}%.

The value invested of R$1,000 is for portfolio total.

</Context>

<Your Task>
Develop an objective commentary on the portfolio's performance, analyzing:
1. **Overall Performance**: Evaluate whether the portfolio is showing satisfactory or unsatisfactory performance
</Your Task>

<Style Guidelines>
- Technical but accessible language
- Avoid excessive jargon
- Use concrete data when available
- Be assertive in your conclusions
</Style Guidelines>

<Format>
- Length: approximately 500 words

-Begin your analysis directly, without preambles such as "The portfolio is having a performance...".

-Always answer in Portuguese.
</Format>
"""

PROMPT_FORMATADO = PROMPT.format(carteira=carteira_atual_markdown, variacao_carteira_porcentagem=variacao_carteira_porcentagem)

llm = ChatNVIDIA(model="meta/llama-4-maverick-17b-128e-instruct")

response = llm.invoke([{"role": "user", "content": PROMPT_FORMATADO}])

logger.info("Comentário gerado com sucesso.")

logger.info("Atualizando trimestre atual no README.md.")

date_now = datetime.datetime.now().strftime("%Y-%m-%d")

trimestre_atual = pd.date_range(end=date_now, periods=1, freq='QS').strftime("%Y-%m-%d")[0]


logger.info("Atualizando README.md com comentario e tabela de resultados do trimestre.")
section_found = False
for i, line in enumerate(readme_content):
    if '### 📊 Tabela Resultados' in line:
        index_inicio = i
    if '🤖 Agentes e Fluxos de Trabalho' in line:
        index_fim = i

readme_content = readme_content[:index_inicio+1] + readme_content[index_fim-1:]
        
readme_content.insert(index_inicio + 1, f"\n{carteira_atual_markdown}\n\n### 💬 Comentário sobre a carteira\n{response.content}\n\n")

logger.info("Atualizando README.md metricas de desempenho da carteira historico.")

metric = pd.read_csv("../data/metricas_carteiras_historico.csv", index_col=0)

metrics_markdow = (metric.round(3)*100).to_markdown()

for i, line in enumerate(readme_content):
    if '### 📊 Metricas de Desempenho' in line:
        index_inicio = i
    if '### 🛠️ Metodologia da Simulação' in line:
        index_fim = i

readme_content = readme_content[:index_inicio+1] + readme_content[index_fim-1:]
        
readme_content.insert(index_inicio + 1, f"\n{metrics_markdow}\n\n\n")

#readme_content = ''.join(readme_content)

logger.info("Atualizando README.md lista de todas as ações avaliadas.")

url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv"

setor = pd.read_csv(url, index_col=0, parse_dates=True)

setor_markdown = setor.to_markdown()

for i, line in enumerate(readme_content):
    if '## 🔍 Lista de ações avaliadas' in line:
        index_inicio = i
    if '## 📁 Estrutura do projeto' in line:
        index_fim = i

readme_content = readme_content[:index_inicio+1] + readme_content[index_fim-1:]
        
readme_content.insert(index_inicio + 1, f"\n{setor_markdown}\n\n\n")

readme_content = ''.join(readme_content)

logger.info("Arquivo README.md atualizado com sucesso.")

try:
    with open('../README.md', 'w', encoding='utf-8') as file:
        file.writelines(readme_content)  
except:
    with open('../README.md', 'w', encoding='latin-1') as file:
        file.writelines(readme_content)
        
logger.info("Arquivo README.md salvo com sucesso.")

    