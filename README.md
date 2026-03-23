# Desafio Final - Indicium

Resolução do Desafio Final do programa **Lighthouse Indicium** feito pelo candidato **Davi Ladeira Balsamão**. Este repositório contém as soluções, análises de dados e modelagens preditivas desenvolvidas como parte do desafio técnico.

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
├── data/
│   ├── raw/                # Arquivos de dados originais (eg. vendas_2023_2024.csv, produtos_raw.csv, custos_importacao.json)
│   └── processed/          # Arquivos de dados limpos e processados gerados pelos scripts
├── notebooks/
│   └── resolucao.ipynb     # Jupyter Notebook principal contendo todo fluxo de análise exploratória, validações matemáticas e Modelos (RandomForest, LinearRegression, SMA) com as respostas descritivas solicitadas
├── questoes/               # Scripts isolados resolvendo e otimizando questões específicas (Questões 2.1, 3.1 e 7)
│   ├── q2.1.py             # Script para padronização de categorias de produtos e limpeza de dados (duplicatas e tipagem)
│   ├── q3.1.py             # Script de tratamento e unnesting do JSON de custos de importação usando `json_normalize` e salvando o resultado em CSV
│   └── q7.py               # Script para implementação do modelo preditivo BaseLine (SMA 7 dias) eviatndo Data Leakage da demanda de um produto alvo ("Motor de Popa Yamaha Evo Dash 155HP")
├── README.md               # Documentação principal do repositório
└── assets/                 # Imagens base, outputs gráficos ou documentações adicionais caso aplicável
```

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Manipulação de Dados:** Pandas, JSON
*   **Machine Learning / Previsões:** Scikit-Learn
*   **Visualização de Dados:** Matplotlib
*   **Ambiente de Desenvolvimento:** Jupyter Notebook, VS Code

## 🚀 Como Executar o Projeto

Certifique-se de possuir o Python instalado e de preferência em um ambiente virtual (`venv`, `conda`).

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd Desafio-Final-indicium
```

2. **Instale as dependências (caso não as possua localmente):**
```bash
pip install pandas scikit-learn matplotlib jupyter
```

3. **Execução pelo Jupyter Notebook:**
A visualização detalhada de todas as análises e processos (Insights de Venda, Análises de Performance e Modelagem principal guiada) está centralizada no notebook. Execute:
```bash
jupyter notebook notebooks/resolucao.ipynb
```

4. **Execução dos scripts isolados:**
Para testar a modularidade e automação propostas nas questões específicas, você pode rodar os scripts da pasta `questoes/` pelo terminal (verifique se os caminhos dos datasets `data/raw/` estão corretos à partir da raiz que você executará).

Exemplo:
```bash
# Na raiz do projeto ('Desafio-Final-indicium')
cd questoes
python q7.py
python q2.1.py
python q3.1.py
```

## 📈 Principais Soluções Aplicadas

*   **Limpeza e Estruturação (q2.1/q3.1):** Aplicação intensa de expressões regulares (regex) e manipulação vetorial do pandas para conversão de moedas (R$), lowercase operations e desaninhar dados tabulares (JSON Flatten) visando eficiência computacional.
*   **Previsão de Demanda (q7):** Estabelecimento de Baseline através de Médias Móveis (SMA janela 7D), criação do calendário de controle contínuo (`date_range`) para evitar falhas em datas faltantes, uso assertivo de `.shift(1)` prevenindo vazamento de dados (*Data Leakage*), validado com cálculo de erro MAE (Mean Absolute Error). 
