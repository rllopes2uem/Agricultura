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
  #git = 'https://raw.githubusercontent.com/rllopes2uem/classDashBoard/main/'
  Area = pd.read_csv(url1)
  Producao = pd.read_csv(url2)
  Valor = pd.read_csv(url3)
  #Ano = Area['Ano'].unique().tolist()
  cult_temp = pd.read_csv(url4,sep=';', header=None)[0].values.tolist()
  cult_perm = pd.read_csv(url5,sep=';', header=None)[0].values.tolist()
  return Area, Producao, Valor, cult_temp, cult_perm
#
def map_munic(state, condado, Database):
     db = Database[(Database.NAME_UF==state)&(Database.MUNIC==condado)]
     UF = db.iloc[0,2]
     SUF = db.iloc[0,3]
     Munic = db.iloc[0,7]
     full_state = geobr.read_municipality(code_muni=str(UF), year=2020)
     full_munic = geobr.read_municipality(code_muni=Munic, year=2020)
     fig, ax = plt.subplots(figsize=(4,4), dpi=300)
     full_state.plot(facecolor="#FFFFFF", edgecolor="#696969", linewidth=.1, ax=ax)
     full_munic.plot(facecolor="#3572EF", edgecolor="#3572EF", linewidth=.1,ax=ax)
     ax.set_title("Município "+ condado + " - "+ str(SUF), fontsize=12)
     ax.axis("off")
     st.pyplot(fig)
     
##
# dados básicos dos municípios
git = 'https://raw.githubusercontent.com/rllopes2uem/classDashBoard/main/'
df_dados_ac, df_dados_pr, df_dados_vb, Temporarias, Permanentes = load_data(git + 'Dados_AC_10_22.csv', git + 'Dados_QP_10_22.csv', git + 'Dados_VP_10_22.csv', git + 'Temp.csv', git + 'Perm.csv')
#
# criando um dicionário Estado-Municípios
states = list(df_dados_ac.NAME_UF.unique())
munic = dict()
for state in range(len(states)):
    munic[states[state]] = list(df_dados_ac[df_dados_ac.NAME_UF== states[state]].MUNIC.unique())
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
    
    culturas = df_dados_ac.columns[9:].tolist()
    #culturas.insert(0,"Temporárias")
    #culturas.insert(1,"Permanentes")
    cultura = st.selectbox("Selecione a Cultura", options=(culturas))
    #
    press_button = st.button('Mostrar')
    #
    if press_button: #st.button('Submit'):
        #df_dados_ac, df_dados_pr, df_dados_vb,
        D_Area = df_dados_ac[(df_dados_ac.NAME_UF==state_selec)&(df_dados_ac.MUNIC==munic_selec)][cultura]
        D_Prod = df_dados_pr[(df_dados_pr.NAME_UF==state_selec)&(df_dados_pr.MUNIC==munic_selec)][cultura]
        D_Valor = df_dados_vb[(df_dados_vb.NAME_UF==state_selec)&(df_dados_vb.MUNIC==munic_selec)][cultura]

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
        map_munic(state_selec, munic_selec,df_dados_ac)
    #    tab1, tab2, pib_p, per_p, nMun = tab_pib(SG_UF,cod_mun)
    #    st.write('O estado conta com ', nMun, ' Municípios')
# App layout
col = st.columns((1.5, 3.25, 3.25), gap='small')
## Column 1
with col[0]:
    if press_button:
        with st.container(border=True):
                ac1 = D_Area.iloc[-1]
                ac2 = D_Area.iloc[-2]
                Dac = ((ac1-ac2)/ac2)
                st.metric(label="Área", 
                          value="{:.0f} ha".format(ac1), 
                          delta="{:.3f} %".format(Dac))
                del(ac1,ac2,Dac)
        #
        with st.container(border=True):
                pd1 = D_Prod.iloc[-1]
                pd2 = D_Prod.iloc[-2]
                Dpd = ((pd1-pd2)/pd2)
                st.metric(label="Produção", 
                          value="{:.0f} ton".format(pd1), 
                          delta="{:.3f} %".format(Dpd))
                del(pd1,pd2,Dpd)
        #
        with st.container(border=True):
                vl1 = D_Valor.iloc[-1]
                vl2 = D_Valor.iloc[-2]
                Dvl = ((vl1-vl2)/vl2)
                st.metric(label="Valor", 
                          value="R$ {:.0f} mil".format(vl1), 
                          delta="{:.3f} %".format(Dvl))
                del(vl1,vl2,Dvl)
        #
        with st.container(border=True):
                ac1 = D_Area.iloc[-1]
                ac2 = D_Area.iloc[-2]
                pd1 = D_Prod.iloc[-1]
                pd2 = D_Prod.iloc[-2]
                pdv1 = (pd1/ac1)
                pdv2 = (pd2/ac2)
                Dpdv = ((pdv1-pdv2)/pdv2)
                st.metric(label="Produtividade", 
                          value="{:.3f} ton/ha".format(pdv1), 
                          delta="{:.3f} %".format(Dpdv))
                del(ac1,ac2,pd1,pd2,pdv1,pdv2,Dpdv)
#
## Column 2
#with col[1]:
#    if press_button:

#
## Column 3
#with col[2]:
#    if press_button:
