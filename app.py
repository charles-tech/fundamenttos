import fundamentus
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Configuração inicial do Streamlit
st.set_page_config(page_title="Análise Fundamentalista", layout="wide")

# Obter os dados
df = fundamentus.get_resultado()

# Configurar os valores padrão e permitir edição pelo usuário em porcentagem
mrgebit_min = st.sidebar.number_input('Margem EBIT mínima (%)', min_value=0.0, max_value=100.0, value=20.0)
dy_min = st.sidebar.number_input('Dividend Yield mínimo (%)', min_value=0.0, max_value=100.0, value=8.0)
dy_max = st.sidebar.number_input('Dividend Yield máximo (%)', min_value=0.0, max_value=100.0, value=15.0)
roe_min = st.sidebar.number_input('ROE mínimo (%)', min_value=0.0, max_value=100.0, value=20.0)

# Converter porcentagens para a forma decimal
mrgebit_min /= 100
dy_min /= 100
dy_max /= 100
roe_min /= 100

# Outras variáveis
pl_max = st.sidebar.number_input('P/L máximo', min_value=0.0, max_value=20.0, value=8.0)
pvp_max = st.sidebar.number_input('P/VP máximo', min_value=0.0, max_value=5.0, value=1.5)

# Botão para aplicar o filtro
if st.sidebar.button('Pesquisar'):
    # Aplicar múltiplas condições com os valores editáveis
    filtro1 = df[(df['pl'] < pl_max) & 
                 (df['mrgebit'] > mrgebit_min) & 
                 (df['dy'] >= dy_min) & (df['dy'] <= dy_max) & 
                 (df['pvp'] <= pvp_max) & 
                 (df['roe'] >= roe_min)]

    # Converter as colunas para porcentagem
    filtro1['mrgebit'] = (filtro1['mrgebit'] * 100).round(2).astype(str) + '%'
    filtro1['dy'] = (filtro1['dy'] * 100).round(2).astype(str) + '%'
    filtro1['roe'] = (filtro1['roe'] * 100).round(2).astype(str) + '%'

    # Ordenar os resultados
    filtro1_sorted = filtro1.sort_values('dy', ascending=False)

    # Exibir o DataFrame usando Streamlit
    st.write("### Dados Filtrados")
    st.dataframe(filtro1_sorted)

    # Criar um gráfico de barras para o campo 'dy'
    plt.figure(figsize=(10, 5))
    bars = plt.bar(filtro1_sorted.index, filtro1_sorted['dy'].str.rstrip('%').astype(float), color='skyblue')
    plt.xlabel('Índice')
    plt.ylabel('DY (%)')
    plt.title('Gráfico de DY para Empresas Filtradas')
    plt.xticks(rotation=90)  # Rotaciona os rótulos do eixo x para melhor visualização
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição

    # Adicionar os valores percentuais no topo de cada barra
    for bar, dy in zip(bars, filtro1_sorted['dy']):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), dy, ha='center', va='bottom')

    # Usar Streamlit para exibir o gráfico abaixo do DataFrame
    st.write("### Gráfico de DY")
    st.pyplot(plt)