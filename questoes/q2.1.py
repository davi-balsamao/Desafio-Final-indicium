import pandas as pd

# Carregando o dataset
df_produtos = pd.read_csv('../data/raw/produtos_raw.csv')

# Parte 1 — Padronize os nomes das categorias de produtos em: eletrônicos, propulsão e ancoragem.
def padronizar_categoria(cat):
    cat_lower = str(cat).lower().replace(' ', '').replace('ô', 'o').replace('ã', 'a').replace('ç', 'c')
    if 'eletr' in cat_lower:
        return 'eletrônicos'
    elif 'prop' in cat_lower:
        return 'propulsão'
    elif 'cor' in cat_lower or 'enc' in cat_lower:
        return 'ancoragem'
    return cat

df_produtos['actual_category'] = df_produtos['actual_category'].apply(padronizar_categoria)
print("Categorias padronizadas:", df_produtos['actual_category'].unique())

# Parte 2 — Converta os valores para o tipo numérico.
df_produtos['price'] = df_produtos['price'].str.replace('R$ ', '', regex=False).astype(float)
print("Tipos de dados após conversão:")
print(df_produtos.dtypes)

# Parte 3 — Remova as duplicatas.
qtd_antes = len(df_produtos)
df_produtos = df_produtos.drop_duplicates()
qtd_depois = len(df_produtos)

print(f"Registros antes: {qtd_antes} | Registros depois (sem duplicatas): {qtd_depois}")

# Visualizando o resultado final
display(df_produtos.head(10))