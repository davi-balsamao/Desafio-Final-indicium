import json

nb_path = r'c:\Davi\Desafio-Final-indicium\notebooks\resolucao.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The Python code for cell
code_source = """import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar os dados
vendas = pd.read_csv('../data/raw/vendas_2023_2024.csv')
custos = pd.read_csv('../data/processed/custos_importacao.csv')

# Conversão de datas para 'datetime' visando o merge_asof
vendas['sale_date_dt'] = pd.to_datetime(vendas['sale_date'], format='mixed', dayfirst=True)
vendas = vendas.sort_values('sale_date_dt')

custos['start_date_dt'] = pd.to_datetime(custos['start_date'], format='%Y-%m-%d') # The processed CSV from Q3 uses ISO format
custos = custos.sort_values('start_date_dt')
custos = custos.rename(columns={'product_id': 'id_product'})

# 2. Match do Custo USD unitário pela data da venda usando merge_asof (backward)
# (Busca o custo vigente mais recente que seja <= a data de venda)
df_merged = pd.merge_asof(
    vendas,
    custos[['id_product', 'start_date_dt', 'usd_price']],
    left_on='sale_date_dt',
    right_on='start_date_dt',
    by='id_product',
    direction='backward'
)

# 3. Consumir a API do Banco Central (PTAX) para o período 2023-2024
url_bcb = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='01-01-2023'&@dataFinalCotacao='12-31-2024'&$format=json"
resp = requests.get(url_bcb)
ptax_data = resp.json()['value']

df_ptax = pd.DataFrame(ptax_data)
# O campo 'dataHoraCotacao' traz a data original do câmbio
df_ptax['data_ptax'] = pd.to_datetime(df_ptax['dataHoraCotacao']).dt.normalize()
df_ptax = df_ptax[['data_ptax', 'cotacaoVenda']].drop_duplicates('data_ptax').sort_values('data_ptax')

# Faz um merge asof para encontrar a cotação correta. 
# Quando houver vendas em finais de semana ou feriados, pegará a última cotação útil anterior (direction='backward')
df_final = pd.merge_asof(
    df_merged,
    df_ptax,
    left_on='sale_date_dt',
    right_on='data_ptax',
    direction='backward'
)

# 4. Cálculo de Custo, Receita e Prejuízo
# Custo Total BRL = Quantidade vendida * Custo Unitário USD * Cotação PTAX Venda do dia
df_final['custo_total_brl'] = df_final['qtd'] * df_final['usd_price'] * df_final['cotacaoVenda']

# Identificar prejuízo: quando o Custo BRL supera a Receita(total) BRL
df_final['teve_prejuizo'] = df_final['custo_total_brl'] > df_final['total']
df_final['valor_prejuizo'] = df_final.apply(lambda row: row['custo_total_brl'] - row['total'] if row['teve_prejuizo'] else 0, axis=1)

# 5. Agregação por id_produto
df_agg = df_final.groupby('id_product').agg(
    receita_total=('total', 'sum'),
    prejuizo_total=('valor_prejuizo', 'sum')
).reset_index()

# Percentual de perda
df_agg['percentual_perda'] = df_agg['prejuizo_total'] / df_agg['receita_total']

display(df_agg.head())
"""

plot_source = """# Parte 2 - Gráfico dos produtos com prejuízo
df_prejuizo = df_agg[df_agg['prejuizo_total'] > 0].sort_values(by='prejuizo_total', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_prejuizo, x='id_product', y='prejuizo_total', palette='Reds_r', order=df_prejuizo['id_product'])
plt.title('Prejuízo Total por Produto (BRL)')
plt.xlabel('ID do Produto')
plt.ylabel('Prejuízo Total (R$)')
plt.tight_layout()
plt.show()
"""

explanation_source = """### Parte 3 — Explicação sobre o Desenvolvimento

**1. Qual data de câmbio você utilizou?**
Utilizamos as datas de fechamento PTAX Venda da API Olinda (Banco Central do Brasil) cobrindo todo o período de vendas (2023 a 2024). Para transações ocorridas em finais de semana ou feriados (dias sem cotação bancária), utilizamos um *backward merge* (`pd.merge_asof(direction='backward')`), ou seja, o algoritmo assumiu a **última cotação válida imediatamente anterior à venda** (ex: venda no Sábado usa o PTAX de Sexta).

**2. Como definiu o prejuízo?**
O prejuízo real existe apenas quando o **Custo Total em BRL excede a Receita Total da transação (`total`)**.
- Custo Total em BRL foi calculado pela fórmula: `Quantidade Registrada * Custo Unitário em USD Histórico * Taxa Cambial PTAX Média de Venda do Dia`.
- Para transações onde Custo > Receita, subtraímos a Receita do Custo para obter exatamente o delta negativo (valor do prejuízo). Se for uma venda lucrativa, a métrica isolada de "prejuízo" dessa transação é considerada 0. A métrica global de "Prejuízo Total" agregou a soma crua desses deltas numéricos por produto.

**3. Algumas suposições relevantes?**
- Como a tabela `custos_importacao.csv` tinha o preço unitário atrelado a uma "Data_Inicio", utilizei novamente a lógica de *Backward Merge* com a data da venda para identificar qual era exatamente o custo em dólar no momento exato em que a venda foi executada, protegendo a análise de mudanças de preço de importação no intermédio dos anos de 2023 e 2024.
- Foi ignorado qualquer aspecto de inflação sobre o BRL e retenção de impostos/fretes (considerado apenas preço direto de importação e custo de venda).
"""

new_cells = [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Questão 4 - Dados Públicos\n",
    "### Parte 1 — Cálculo e modelagem e Identificação de Prejuízos (Câmbio)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [s + "\\n" for s in code_source.splitlines()]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [s + "\\n" for s in plot_source.splitlines()]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": explanation_source.splitlines(keepends=True)
  }
]

nb['cells'].extend(new_cells)

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
