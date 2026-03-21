import json

nb_path = r'c:\Davi\Desafio-Final-indicium\notebooks\resolucao.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

code_source = """# Utilizando DuckDB para refazer o cálculo da Questão 4
import duckdb

# As variáveis vendas, custos e df_ptax já estão carregadas e tratadas nas células anteriores (Q4).
# O DuckDB compreende nativamente DataFrames Pandas armazenados na memória!

query_q4 = \"\"\"
WITH ptax_prep AS (
    -- Para cada venda, puxar o câmbio mais recente inferior ou igual à data de venda
    SELECT 
        v.id_product,
        v.sale_date_dt,
        v.qtd,
        v.total AS receita_brl,
        (SELECT p.cotacaoVenda 
         FROM df_ptax p 
         WHERE p.data_ptax <= v.sale_date_dt 
         ORDER BY p.data_ptax DESC LIMIT 1) AS taxa_cambio_data,
        (SELECT c.usd_price 
         FROM custos c 
         WHERE c.id_product = v.id_product AND c.start_date_dt <= v.sale_date_dt 
         ORDER BY c.start_date_dt DESC LIMIT 1) AS custo_usd
    FROM vendas v
),
calculo_custo AS (
    -- Cálculo do custo total da transação em BRL
    SELECT 
        id_product,
        receita_brl,
        custo_usd,
        taxa_cambio_data,
        (qtd * custo_usd * taxa_cambio_data) AS custo_total_brl
    FROM ptax_prep
),
calculo_prejuizo AS (
    -- Identificação de transações com prejuízo (custo em BRL > valor de venda em BRL)
    SELECT 
        id_product,
        receita_brl,
        CASE 
            WHEN custo_total_brl > receita_brl THEN (custo_total_brl - receita_brl)
            ELSE 0 
        END AS prejuizo
    FROM calculo_custo
)
-- Agregação solicitada
SELECT 
    id_product,
    SUM(receita_brl) AS receita_total,
    SUM(prejuizo) AS prejuizo_total,
    (SUM(prejuizo) / SUM(receita_brl)) AS percentual_perda
FROM calculo_prejuizo
GROUP BY id_product
ORDER BY prejuizo_total DESC;
\"\"\"

resultado_sql_q4 = duckdb.query(query_q4).to_df()

display(resultado_sql_q4.head(10))
"""

new_cells = [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Questão 4.1 - Código SQL\n",
    "### Reconstruindo o Cálculo de Perdas e Câmbio do Pandas para DuckDB"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [s + "\\n" for s in code_source.splitlines()]
  }
]

nb['cells'].extend(new_cells)

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
