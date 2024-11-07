import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import json

def area_urbanizada():
    # URL da API do IBGE
    link = "https://servicodados.ibge.gov.br/api/v3/agregados/8418/periodos/2019/variaveis/12749?localidades=N2[all]"
    link2 = "https://servicodados.ibge.gov.br/api/v3/agregados/8418/periodos/2019/variaveis/12750?localidades=N2[all]"

    # Fazendo a requisição
    requisicao = requests.get(link)
    requisicao2 = requests.get(link2)
    informacoes = requisicao.json()
    informacoes2 = requisicao2.json()

    # Extraindo os dados para um DataFrame
    dados = []
    dados2 = []
    for resultado in informacoes[0]['resultados'][0]['series']:
        estado = resultado['localidade']['nome']
        valor = float(resultado['serie']['2019'])
        dados.append({'Localidade': estado, 'Quilômetros quadrados': valor})

    for resultado in informacoes2[0]['resultados'][0]['series']:
        estado = resultado['localidade']['nome']
        valor = float(resultado['serie']['2019'])
        dados2.append({'Localidade': estado, 'Quilômetros quadrados': valor})

    df = pd.DataFrame(dados)
    df2 = pd.DataFrame(dados2)

    # Criando o gráfico de barras com Plotly
    fig_bar = px.bar(df, 
                 x='Localidade', 
                 y='Quilômetros quadrados',
                 title='Áreas Urbanizadas por Grande Região',
                 labels={'Valor': 'Valor', 'Estado': 'Estado'})

    fig_bar2 = px.bar(df2,
                 x='Localidade',
                 y='Quilômetros quadrados', 
                 title='Loteamentos urbanos vazios',
                 labels={'Valor': 'Valor', 'Estado': 'Estado'})

    # Criando o gráfico de pizza com Plotly
    fig_pie = px.pie(df,
                     values='Quilômetros quadrados',
                     names='Localidade')

    fig_pie2 = px.pie(df2,
                     values='Quilômetros quadrados',
                     names='Localidade')
    
    # Exibindo no Streamlit
    st.title('Dados Abertos do IBGE')
    st.markdown('Este projeto é uma iniciativa pessoal voltada para o consumo da API do Instituto Brasileiro de Geografia e Estatística (IBGE) para organizar as informações em visualizações gráficas, facilitando a análise, interpretação e acessibilidade de dados públicos.')

    # Adicionando espaço entre os gráficos
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.header('Urbanização')
    st.write('Esta seção oferece uma visão clara das tendências de urbanização no Brasil, permitindo uma análise detalhada sobre como as mudanças urbanas impactam a economia, o meio ambiente e a organização social.')

    # Criando três colunas para exibir os gráficos com espaço no meio
    col1, col_espaco, col2 = st.columns([4, 1, 3])

    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.plotly_chart(fig_pie, use_container_width=True)

    col3, col_espaco2, col4 = st.columns([4, 1, 3])

    with col3:
        st.plotly_chart(fig_bar2, use_container_width=True)
        
    with col4:
        st.plotly_chart(fig_pie2, use_container_width=True)

    # Adicionando fonte dos dados
    st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/8418/periodos/2019/variaveis/12749?localidades=N2[all]")
    st.markdown("**Fonte 2:** https://servicodados.ibge.gov.br/api/v3/agregados/8418/periodos/2019/variaveis/12750?localidades=N2[all]")
    with st.expander("Visualizar dados brutos (JSON)"):
        st.json(informacoes)
        st.json(informacoes2)
    


def censo_demografico():
    # URL da API do IBGE
    link = "https://servicodados.ibge.gov.br/api/v3/agregados/1298/periodos/1920|1940|1950|1960|1970|1980|1991|2000|2010/variaveis/614?localidades=N1[all]"

    # Fazendo a requisição
    requisicao = requests.get(link)
    informacoes = requisicao.json()

    # Extraindo os dados para um DataFrame
    dados = []
    for resultado in informacoes[0]['resultados'][0]['series']:
        pais = resultado['localidade']['nome']
        serie = resultado['serie']
        for ano, valor in serie.items():
            dados.append({
                'País': pais,
                'Ano': int(ano),
                'População': float(valor)
            })

    df = pd.DataFrame(dados)

    # Criando o gráfico de linha com Plotly
    fig_line = px.line(df,
                     x='Ano',
                     y='População',
                     title='Crescimento Populacional do Brasil (1920-2010)',
                     labels={'População': 'População Total', 'Ano': 'Ano do Censo'},
                     markers=True)

    # Exibindo no Streamlit
    st.header('Censo Demográfico')
    st.write('Essa seção oferece informações detalhadas sobre a composição populacional do Brasil, abrangendo aspectos como distribuição etária, gênero, escolaridade, renda, habitação, e condições de vida em todo o território nacional. Utilizando gráficos interativos e tabelas dinâmicas, a seção permite uma análise aprofundada das transformações sociais e econômicas do país ao longo dos anos.')

    # Exibindo o gráfico
    st.plotly_chart(fig_line, use_container_width=True)


    # Exibindo os dados brutos em formato JSON
    st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/1298/periodos/1920|1940|1950|1960|1970|1980|1991|2000|2010/variaveis/614?localidades=N1[all]")
    with st.expander("Visualizar dados brutos (JSON)"):
        st.json(informacoes)

def densidade_demo():
    # URL da API do IBGE
    link = "https://servicodados.ibge.gov.br/api/v3/agregados/1301/periodos/2010/variaveis/616?localidades=N2[all]"

    # Fazendo a requisição
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Extraindo os dados para um DataFrame
    dados = []
    for resultado in informacoes[0]['resultados'][0]['series']:
        localidade = resultado['localidade']['nome']
        serie = resultado['serie']
        for ano, valor in serie.items():
            dados.append({
                'Localidade': localidade,
                'Ano': int(ano),
                'Densidade Demográfica': float(valor)
            })

    df = pd.DataFrame(dados)

    # Criando o gráfico de barras com Plotly
    fig_bar = px.bar(df,
                     x='Localidade',
                     y='Densidade Demográfica',
                     color='Localidade',
                     title='Densidade Demográfica por Região (2010)',
                     labels={'Densidade Demográfica': 'Habitantes por km²', 'Localidade': 'Região'})

    # Exibindo o gráfico
    st.plotly_chart(fig_bar, use_container_width=True)

    # Exibindo os dados brutos em formato JSON
    st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/1301/periodos/2010/variaveis/616?localidades=N2[all]")
    with st.expander("Visualizar dados brutos (JSON)"):
        st.json(informacoes)


def cor():
    # URL da API do IBGE
    link = "https://servicodados.ibge.gov.br/api/v3/agregados/9605/periodos/2022/variaveis/93?localidades=N1[all]&classificacao=86[2776,2777,2778,2779,2780]"

    # Fazendo a requisição
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Extraindo os dados para um DataFrame
    dados = []
    for resultado in informacoes[0]['resultados']:
        cor = resultado['classificacoes'][0]['categoria'].values()
        valor = list(resultado['series'][0]['serie'].values())[0]
        
        if valor != '-':
            dados.append({
                'Cor': list(cor)[0],
                'População': float(valor)
            })

    df = pd.DataFrame(dados)

    # Criando o gráfico de barras com Plotly
    fig_bar = px.bar(df, 
                     x='Cor',
                     y='População',
                     title='População por Cor ou Raça declarada (2022)',
                     labels={'População': 'Número de Pessoas', 'Cor': 'Cor'})

    # Criando o gráfico de pizza com Plotly
    fig_pie = px.pie(df, 
                     names='Cor',
                     values='População',
                     title='',
                     labels={'Cor': 'Cor'})

    # Exibindo os gráficos lado a lado em colunas diferentes
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie, use_container_width=True)

    # Exibindo os dados brutos em formato JSON
    st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/9605/periodos/2022/variaveis/93?localidades=N1[all]&classificacao=86[2776,2777,2778,2779,2780]")
    with st.expander("Visualizar dados brutos (JSON)"):
        st.json(informacoes)

    
def especies_ameacadas():
    # URL da API do IBGE
    link = "https://servicodados.ibge.gov.br/api/v3/agregados/7392/periodos/2014/variaveis/10484?localidades=N1[all]&classificacao=920[48255,48256,48257,48258,48259,48260,48261,48275]|12920[119343,119344,119345,119346,119347,48240,48241]"

    # Fazendo a requisição
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Extraindo os dados para um DataFrame
    dados = []
    for resultado in informacoes[0]['resultados']:
        bioma = resultado['classificacoes'][0]['categoria'].values()
        categoria_risco = resultado['classificacoes'][1]['categoria'].values()
        valor = list(resultado['series'][0]['serie'].values())[0]
        
        if valor != '-':
            dados.append({
                'Bioma': list(bioma)[0],
                'Categoria de Risco': list(categoria_risco)[0],
                'Número de Espécies': float(valor)
            })

    df = pd.DataFrame(dados)

    # Criando o gráfico de barras com Plotly
    fig = px.bar(df, 
                 x='Bioma',
                 y='Número de Espécies',
                 color='Categoria de Risco',
                 title='Espécies Ameaçadas por Bioma e Categoria de Risco',
                 labels={'Número de Espécies': 'Número de Espécies Ameaçadas'})

    # Rotacionando os rótulos do eixo x para melhor visualização
    fig.update_xaxes(tickangle=45)

    # Exibindo no Streamlit
    st.header('Espécies Ameaçadas')
    st.write('Nessa seção, são apresentados gráficos e mapas interativos que ilustram a distribuição geográfica das espécies ameaçadas, os níveis de risco e as principais causas de ameaça, como desmatamento, mudanças climáticas e atividades humanas.')
    st.plotly_chart(fig, use_container_width=True)

    # Exibindo os dados brutos em formato JSON
    st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/7392")
    with st.expander("Visualizar dados brutos (JSON)"):
        st.json(informacoes)



def pib_e_pibpc():
    # URLs da API do IBGE
    link_pib = "https://servicodados.ibge.gov.br/api/v3/agregados/6784/periodos/1996|1997|1998|1999|2000|2001|2002|2003|2004|2005|2006|2007|2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021/variaveis/9808?localidades=N1[all]"
    link_pibpc = "https://servicodados.ibge.gov.br/api/v3/agregados/6784/periodos/1996|1997|1998|1999|2000|2001|2002|2003|2004|2005|2006|2007|2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021/variaveis/9812?localidades=N1[all]"

    # Fazendo as requisições
    requisicao_pib = requests.get(link_pib)
    requisicao_pibpc = requests.get(link_pibpc)
    informacoes_pib = requisicao_pib.json()
    informacoes_pibpc = requisicao_pibpc.json()

    # Extraindo os dados para DataFrames
    dados_pib = []
    dados_pibpc = []
    
    series_pib = informacoes_pib[0]['resultados'][0]['series'][0]['serie']
    series_pibpc = informacoes_pibpc[0]['resultados'][0]['series'][0]['serie']
    
    for ano, valor in series_pib.items():
        dados_pib.append({
            'Ano': int(ano),
            'PIB': float(valor)
        })
        
    for ano, valor in series_pibpc.items():
        dados_pibpc.append({
            'Ano': int(ano),
            'PIB per capita': float(valor)
        })

    df_pib = pd.DataFrame(dados_pib)
    df_pibpc = pd.DataFrame(dados_pibpc)

    # Criando os gráficos de linha com Plotly
    fig_pib = px.line(df_pib,
                      x='Ano', 
                      y='PIB',
                      title='Evolução do PIB Brasileiro (1996-2021)',
                      labels={'PIB': 'PIB em Milhões de Reais'},
                      markers=True)

    fig_pibpc = px.line(df_pibpc,
                        x='Ano', 
                        y='PIB per capita',
                        title='Evolução do PIB per capita Brasileiro (1996-2021)',
                        labels={'PIB per capita': 'PIB per capita em Reais'},
                        markers=True)

    # Formatando os eixos y
    fig_pib.update_layout(
        yaxis=dict(
            tickformat=',',
            title='PIB (Milhões de Reais)'
        )
    )
    
    fig_pibpc.update_layout(
        yaxis=dict(
            tickformat=',',
            title='PIB per capita (Reais)'
        )
    )

    st.header('Produto Interno Bruto (PIB)')
    st.write('Esta seção oferece gráficos e mapas que ilustram a variação do PIB em diferentes setores, como agricultura, indústria e serviços, bem como a participação econômica das regiões e estados brasileiros. Por meio dessas visualizações, é possível compreender as dinâmicas de crescimento e retração econômica, identificar tendências e analisar fatores que impactam diretamente o desenvolvimento do país. ')

    # Criando colunas para os gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig_pib, use_container_width=True)
        st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/6784/periodos/1996|1997|1998|1999|2000|2001|2002|2003|2004|2005|2006|2007|2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021/variaveis/9808?localidades=N1[all]")
        with st.expander("Visualizar dados brutos (JSON)"):
            st.json(informacoes_pib)

    with col2:
        st.plotly_chart(fig_pibpc, use_container_width=True)
        st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/6784/periodos/1996|1997|1998|1999|2000|2001|2002|2003|2004|2005|2006|2007|2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021/variaveis/9812?localidades=N1[all]")
        with st.expander("Visualizar dados brutos (JSON)"):
            st.json(informacoes_pibpc)


def salario_medio():
    # URL da API do IBGE
    link = "https://servicodados.ibge.gov.br/api/v3/agregados/1936/periodos/2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021/variaveis/10143?localidades=N1[all]"

    # Fazendo a requisição
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Extraindo os dados para um DataFrame
    dados = []
    series = informacoes[0]['resultados'][0]['series'][0]['serie']
    
    for ano, valor in series.items():
        dados.append({
            'Ano': int(ano),
            'Salário Médio': float(valor)
        })

    df = pd.DataFrame(dados)

    # Criando o gráfico de linha com Plotly
    fig = px.line(df,
                  x='Ano', 
                  y='Salário Médio',
                  title='Evolução do Salário Médio no Brasil (2008-2021)',
                  labels={'Salário Médio': 'Salário Médio em Reais'},
                  markers=True)

    # Formatando o eixo y para mostrar valores em reais
    fig.update_layout(
        yaxis=dict(
            tickformat=',',
            title='Salário Médio (Reais)'
        )
    )

    # Exibindo no Streamlit
    st.header('Demografia das Empresas e Estatísticas de Empreendedorismo')
    st.write('Esta seção apresenta dados em gráficos interativos sobre a quantidade de empresas ativas, taxas de entrada e saída do mercado, tamanho das empresas, setores predominantes e distribuição geográfica dos empreendimentos.')
    st.plotly_chart(fig, use_container_width=True)

    # Exibindo os dados brutos em formato JSON
    st.markdown("**Fonte:** https://servicodados.ibge.gov.br/api/v3/agregados/1936/periodos/2008|2009|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021/variaveis/10143?localidades=N1[all]")
    with st.expander("Visualizar dados brutos (JSON)"):
        st.json(informacoes)

'''
def x():
    # URL da API do IBGE
    link = "https://servicodados.ibge.gov.br/api/v3/agregados/9605/periodos/2022/variaveis/93?localidades=N1[all]&classificacao=86[2776,2777,2778,2779,2780]"

    # Fazendo a requisição
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    with open('dados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(informacoes, arquivo, ensure_ascii=False, indent=4)

    Prompt: 'Com base no arquivo 'dados.json', construa um gráfico com base nos modelos das funções anteriores'

'''

