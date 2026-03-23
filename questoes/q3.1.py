import pandas as pd
import json
import os

# Carregando o arquivo JSON
with open('../data/raw/custos_importacao.json', 'r', encoding='utf-8') as f:
    dados_json = json.load(f)

# Utilizando json_normalize para desaninhar (flatten) a lista 'historic_data'
df_custos = pd.json_normalize(
    dados_json, 
    record_path=['historic_data'], 
    meta=['product_id', 'product_name', 'category']
)

# Reordenando as colunas conforme a imagem solicitada
df_custos = df_custos[['product_id', 'product_name', 'category', 'start_date', 'usd_price']]

# Visão do dataframe resultante
display(df_custos.head())

# Garantindo que o diretório exista e salvando em CSV
os.makedirs('../data/processed', exist_ok=True)
df_custos.to_csv('../data/processed/custos_importacao.csv', index=False, encoding='utf-8')
print("Arquivo salvo com sucesso em: data/processed/custos_importacao.csv")
