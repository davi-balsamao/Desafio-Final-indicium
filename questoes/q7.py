import pandas as pd
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Importação e inicialização dos dados base com Pandas
produtos = pd.read_csv('../data/raw/produtos_raw.csv')
vendas = pd.read_csv('../data/raw/vendas_2023_2024.csv')

# Isolando o produto alvo "Motor Evo Dash 155" entre os IDs cadastrados
target_product = "Motor de Popa Yamaha Evo Dash 155HP"
target_id = produtos.loc[produtos['name'] == target_product, 'code'].values[0]

# Criando cópia manipulável convertendo os campos de data limitados
v_target = vendas[vendas['id_product'] == target_id].copy()
v_target['sale_date_dt'] = pd.to_datetime(v_target['sale_date'], format='mixed', dayfirst=True)

# Estruturando calendário linear para suportar buracos matemáticos

datas_completas = pd.date_range(start='2023-01-01', end='2024-01-31', freq='D')
df_vendas_diarias = v_target.groupby('sale_date_dt')['qtd'].sum().reset_index()

# Fill_value aplicando zeros forçados p/ preenchimento nas ausências diárias
df_analise = pd.DataFrame({'sale_date_dt': datas_completas})
df_analise = pd.merge(df_analise, df_vendas_diarias, on='sale_date_dt', how='left').fillna({'qtd': 0})
df_analise.set_index('sale_date_dt', inplace=True)

# Aplicação da rolagem Baseline construindo Média Móvel a partir da janela de 7 períodos
# Inserção de "shift" contornando distorção de Data Leakage nas predições
df_analise['SMA_7D_Previsao'] = df_analise['qtd'].shift(1).rolling(window=7).mean()

# Particionando as etapas lógicas de Treino e o cenário de estresse em Teste
treino = df_analise.loc[:'2023-12-31']
teste = df_analise.loc['2024-01-01':'2024-01-31']

# Validando a resposta em MAE - Erro Absoluto Médio final da implementação
mae_score = mean_absolute_error(teste['qtd'], teste['SMA_7D_Previsao'])

print(f"Produto: {target_product}")
print(f"Métrica MAE em Janeiro de 2024: {mae_score:.2f} unidades\n")

# Configuração de exibição via matplotlib validando e plotando Janeiro/2024
plt.figure(figsize=(12, 5))
plt.plot(teste.index, teste['qtd'], label='Vendas Reais (Janeiro 2024)', color='blue', marker='o')
plt.plot(teste.index, teste['SMA_7D_Previsao'], label='Previsão SMA (Baseline)', color='orange', linestyle='--', marker='x')
plt.title(f'Previsão vs Real: {target_product}')
plt.ylabel('Vendas Diárias')
plt.legend()
plt.tight_layout()
plt.show()




prev_q72 = round(teste.loc['2024-01-01':'2024-01-07', 'SMA_7D_Previsao'].sum())
print(f"[VALIDAÇÃO MATEMÁTICA CONSOLIDADA] Projeção da janela referenciada calculada no mês: {prev_q72}")