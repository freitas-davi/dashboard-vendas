import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# CARREGAR DADOS
dados = pd.read_csv('sales_data.csv', sep=';')
lojas = pd.read_csv('customer_data.csv', sep=';', encoding= 'latin1')


# TITULOS
st.title('Dashboard vendas Atacadão Dia Dia')


# DADOS DAS VENDAS
dados['Data'] = pd.to_datetime(dados['Data'])
dados['Ano'] = dados['Data'].dt.year
dados['Mês'] = dados['Data'].dt.month
dados['Vendas_Totais'] = dados['Quantidade'] * dados['Valor_Unitário']

anos = sorted(dados['Ano'].unique())
ano_selecionado = st.selectbox('Selecione o ano:', anos)

dados_filtrados = dados[dados['Ano'] == ano_selecionado]

st.subheader('Tendência de Vendas Mensais')
vendas_por_mes = dados_filtrados.groupby('Mês')['Vendas_Totais'].sum()
plt.figure(figsize=(10, 6))
plt.plot(vendas_por_mes.index, vendas_por_mes.values, marker='o')
plt.title('Tendência de Vendas Mensais')
plt.xlabel('Mês')
plt.ylabel('Vendas Totais (R$)')
plt.grid(True)
st.pyplot(plt)


# Tabela com produtos mais vendidos
st.subheader('Produtos Mais Vendidos')
produtos_mais_vendidos = dados_filtrados.groupby('Produto')['Quantidade'].sum().sort_values(ascending=False)
st.table(produtos_mais_vendidos.head(10))



# CADASSTROS FEITOS POR LOJAS
cadastro_cidades = lojas['Cidade'].value_counts().reset_index()
cadastro_cidades.columns = ['Cidade', 'Total_cadastros']

# Gráfico cadastros - Barras
st.subheader('Cadastro por cidade')

fig = px.bar(
    cadastro_cidades,
    x = 'Cidade',
    y = 'Total_cadastros',
    title = 'Cadastros por cidades',
    labels = {'Cidade':'Cidade', 'Total_cadastros':'Total de cadastros'},
    text = 'Total_cadastros'
)

fig.update_traces(texttemplate='${Cadastros}', textposition='outside')
fig.update_layout(yaxis=dict(title='Total de cadastros'), xaxis= dict(title='Cidade'))

# Mostrar gráfico de barras no streamlit
st.plotly_chart(fig)