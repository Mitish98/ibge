import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# URL da API do IBGE
link = "https://servicodados.ibge.gov.br/api/v3/agregados/8418/periodos/2019/variaveis/12749?localidades=N2[all]"

# Fazendo a requisição
requisicao = requests.get(link)
informacoes = requisicao.json()

# Extraindo os dados para um DataFrame
dados = []
for resultado in informacoes[0]['resultados'][0]['series']:
    estado = resultado['localidade']['nome']
    valor = float(resultado['serie']['2019'])
    dados.append({'Localidade': estado, 'Quilômetros quadrados': valor})

df = pd.DataFrame(dados)

# Criando o gráfico de barras com Plotly
fig_bar = px.bar(df, 
             x='Localidade', 
             y='Quilômetros quadrados',
             title='Área Urbanizada por Grandes Regiões no Brasil',
             labels={'Valor': 'Valor', 'Estado': 'Estado'})

# Criando o gráfico de pizza com Plotly
fig_pie = px.pie(df,
                 values='Quilômetros quadrados',
                 names='Localidade')
                

# Exibindo no Streamlit
st.title('Dados Abertos do IBGE')

# Adicionando espaço entre os gráficos
st.markdown("<br><br>", unsafe_allow_html=True)

# Criando três colunas para exibir os gráficos com espaço no meio
col1, col_espaco, col2 = st.columns([4, 1, 3])

with col1:
    st.plotly_chart(fig_bar, use_container_width=True)
    
with col2:
    st.plotly_chart(fig_pie, use_container_width=True)

# Adicionando fonte dos dados
st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/8418/periodos/2019/variaveis/12749?localidades=N2[all]")