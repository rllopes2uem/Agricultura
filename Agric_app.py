import geobr
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
# Page configuration
st.set_page_config(
    page_title="Produção Agrícola dos Municípios Brasileiros",
    page_icon= "mip_consult_icon.ico",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
#
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 35px;
}
</style>
""",
    unsafe_allow_html=True,
)

# Load data
@st.cache_data  # 👈 Add the caching decorator
def load_data(url1,url2,url3,url4,url5):
  git = 'https://raw.githubusercontent.com/rllopes2uem/classDashBoard/main/'
  Area = pd.read_csv(url1)
  Producao = pd.read_csv(url2)
  Valor = pd.read_csv(url3)
  Ano = Area['Ano'].unique().tolist()
  cult_temp = pd.read_csv(url4,sep=';', header=None)[0].values.tolist()
  cult_perm = pd.read_csv(url5,sep=';', header=None)[0].values.tolist()
##
# dados básicos dos municípios
git = 'https://raw.githubusercontent.com/rllopes2uem/classDashBoard/main/'
df_dados_ac, df_dados_pr, df_dados_vb, Temporarias, Permanentes = load_data(git + 'Dados_AC_10_22.csv', git + 'Dados_QP_10_22.csv', git + 'Dados_VP_10_22.csv', git + 'Temp.csv', git + 'Perm.csv')
#
# criando um dicionário Estado-Municípios
states = list(df_dados_ac.NOME_UF.unique())
munic = dict()
for state in range(len(states)):
    munic[states[state]] = list(df_dados_pib[df_dados_pib.NOME_UF== states[state]].MUNIC.unique())
#
#st.title(':blue[MIP Consult]')
st.markdown("<h1 style='text-align: center; color: blue;'>MIP Consult</h1>", unsafe_allow_html=True)
#
with st.sidebar:
    st.title('Produção Agrícola')
    # selecionando o Estado
    state_selec = st.selectbox('Selecione o Estado', options=list(munic.keys()))
    if state_selec != 'select':
        munic_selec = st.selectbox('Selecione o Município', options=munic[state_selec])
    press_button = st.button('Mostrar')
    #
    #if press_button: #st.button('Submit'):
    #    SG_UF = df_dados_pib[df_dados_pib.NOME_UF==state_selec].UF.unique()[0]
    #    
    #    cod_mun = df_dados_pib[(df_dados_pib.NOME_UF==state_selec)&
    #                           (df_dados_pib.NOME_MUNIC==munic_selec)].COD_MUNIC.unique()[0]
    #    
    #    TAB_PIB = df_taxas_[df_taxas_.COD_MUNIC==cod_mun]
    #    
    #    dados_mun = df_dados_pib[(df_dados_pib.UF==SG_UF) & 
    #                             (df_dados_pib.COD_MUNIC==cod_mun)]
    #    
    #    
    #    map_munic(SG_UF,cod_mun, munic_selec)
    #    tab1, tab2, pib_p, per_p, nMun = tab_pib(SG_UF,cod_mun)
    #    st.write('O estado conta com ', nMun, ' Municípios')

