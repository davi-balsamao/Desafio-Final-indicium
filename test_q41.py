import pandas as pd
import requests
import duckdb

vendas = pd.read_csv('data/raw/vendas_2023_2024.csv')
custos = pd.read_csv('data/processed/custos_importacao.csv')

vendas['sale_date_dt'] = pd.to_datetime(vendas['sale_date'], format='mixed', dayfirst=True)
custos['start_date_dt'] = pd.to_datetime(custos['start_date'], format='%d/%m/%Y')
custos = custos.rename(columns={'product_id': 'id_product'})

url_bcb = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='01-01-2023'&@dataFinalCotacao='12-31-2024'&$format=json"
resp = requests.get(url_bcb)
df_ptax = pd.DataFrame(resp.json()['value'])
df_ptax['data_ptax'] = pd.to_datetime(df_ptax['dataHoraCotacao']).dt.normalize()
df_ptax = df_ptax[['data_ptax', 'cotacaoVenda']].drop_duplicates('data_ptax')

query_q4 = """
WITH ptax_prep AS (
    SELECT 
        v.id_product,
        v.sale_date_dt,
        v.qtd,
        v.total AS receita_brl,
        (SELECT p.cotacaoVenda FROM df_ptax p WHERE p.data_ptax <= v.sale_date_dt ORDER BY p.data_ptax DESC LIMIT 1) AS taxa_cambio_data,
        (SELECT c.usd_price FROM custos c WHERE c.id_product = v.id_product AND c.start_date_dt <= v.sale_date_dt ORDER BY c.start_date_dt DESC LIMIT 1) AS custo_usd
    FROM vendas v
),
calculo_custo AS (
    SELECT 
        id_product,
        receita_brl,
        (qtd * custo_usd * taxa_cambio_data) AS custo_total_brl
    FROM ptax_prep
),
calculo_prejuizo AS (
    SELECT 
        id_product,
        receita_brl,
        CASE 
            WHEN custo_total_brl > receita_brl THEN (custo_total_brl - receita_brl)
            ELSE 0 
        END AS prejuizo
    FROM calculo_custo
)
SELECT 
    id_product,
    SUM(receita_brl) AS receita_total,
    SUM(prejuizo) AS prejuizo_total,
    (SUM(prejuizo) / SUM(receita_brl)) AS percentual_perda
FROM calculo_prejuizo
GROUP BY id_product
ORDER BY prejuizo_total DESC;
"""
res = duckdb.query(query_q4).to_df()
print(res.head())
