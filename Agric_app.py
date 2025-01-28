import geobr
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import statsmodels.formula.api as smf
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
def load_data(url1,url2):
  Dados_01 = pd.read_csv(url1)
  Dados_02 = pd.read_csv(url2)
  Dados = pd.concat([Dados_01, Dados_02], axis=0, ignore_index=True)
  del(Dados_01, Dados_02)
  return Dados
#
def lavouras(url3):  
    cult_ = pd.read_csv(url3,sep=';', header=None)[0].values.tolist()
    return cult_

#
def map_munic(state, condado, Database):
     db = Database[(Database.NAME_UF==state)&(Database.MUNIC==condado)]
     UF = db.iloc[0,3]
     SUF = db.iloc[0,5]
     Munic = db.iloc[0,8]
     full_state = geobr.read_municipality(code_muni=str(UF), year=2020)
     full_munic = geobr.read_municipality(code_muni=Munic, year=2020)
     fig, ax = plt.subplots(figsize=(4,4), dpi=300)
     full_state.plot(facecolor="#FFFFFF", edgecolor="#696969", linewidth=.1, ax=ax)
     full_munic.plot(facecolor="#3572EF", edgecolor="#3572EF", linewidth=.1,ax=ax)
     ax.set_title("Município "+ condado + " - "+ str(SUF), fontsize=12)
     ax.axis("off")
     st.pyplot(fig)
#
def tab_lav(db, UF, Municipio, Cultura, tipo):
    df_est = db[(db['Ano']==2023) & (db.NAME_UF==UF)][['MUNIC',Cultura]]
    df_est = df_est.sort_values(Cultura, ascending=False)
    df_est['RANK'] = list(range(1,len(df_est)+1))
    idx = df_est[df_est['MUNIC'] == Municipio]['RANK']
    if int(idx.iloc[0]) <= 5:
        table_pos = df_est.head()
    else:
        ext_mun = df_est[df_est['MUNIC'] == Municipio]
        table_pos = pd.concat([df_est.head(4),ext_mun])
		
    if tipo == 1:
        table_pos.columns = ['Munic.', 'Produção (ton.)', 'Rank']
        table_pos['Produção (ton.)'] = table_pos['Produção (ton.)'].map('{:.0f}'.format)
        table_pos['Produção (ton.)'] = table_pos['Produção (ton.)'].astype(int)
    else:
        table_pos.columns = ['Munic.', 'Rendimento (kg/ha.)', 'Rank']
	
    return table_pos, idx
#---------------------------#
def tab_nacional(db, Region, Municipio, Cultura, tipo):
    if Region=='Brasil':
        df_est = db[(db['Ano']==2023)][['MUNIC','UF', Cultura]]
    else:
        df_est = db[(db['Ano']==2023) & (db.NOME_REG==Region)][['MUNIC','UF', Cultura]]
    
    df_est = df_est.sort_values(Cultura, ascending=False)
    df_est['RANK'] = list(range(1,len(df_est)+1))
    idx = df_est[df_est['MUNIC'] == Municipio]['RANK']
    
    if int(idx.iloc[0]) <= 25:
        table_pos = df_est.head()
    else:
        ext_mun = df_est[df_est['MUNIC'] == Municipio]
        table_pos = pd.concat([df_est.head(24),ext_mun])
        
    return table_pos, idx
#---------------------------#
    
def taxa_cresc(data1):
    base = pd.DataFrame({'Ano':range(2010,2024), 'Cult':data1})
    reg = smf.ols('np.log(data1) ~ Ano', data=base)
    res = reg.fit()
    return res.params['Ano']*100
#
def graf_linha(state, condado,crops, tipo):
    if tipo==1:
         dados = df_dados_ac[(df_dados_ac.NAME_UF==state)&(df_dados_ac.MUNIC==condado)]
         tx_cresc = taxa_cresc(dados[crops])
         titulo = 'Área Colhida (em ha) - Taxa de Cresc. ' + ' {:.3f} % a.a.'.format(tx_cresc)
    elif tipo==2:
         dados = df_dados_qp[(df_dados_qp.NAME_UF==state)&(df_dados_qp.MUNIC==condado)]
         tx_cresc = taxa_cresc(dados[crops])
         titulo = 'Produção (em ton.) - Taxa de Cresc. ' + ' {:.3f} % a.a.'.format(tx_cresc)
    elif tipo==3:
         dados = df_dados_vp[(df_dados_vp.NAME_UF==state)&(df_dados_vp.MUNIC==condado)]
         tx_cresc = taxa_cresc(dados[crops])
         titulo = 'valor da Produção (R$ mil) - Taxa de Cresc. ' + ' {:.3f} % a.a.'.format(tx_cresc)
    else:
         dados = df_dados_rd[(df_dados_rd.NAME_UF==state)&(df_dados_rd.MUNIC==condado)]
         tx_cresc = taxa_cresc(dados[crops])
         titulo = 'Produtividade (ton/ha) - Taxa de Cresc. ' + ' {:.3f} % a.a.'.format(tx_cresc)
    #
    fig2 = px.line(dados, 
                   x='Ano',
                   y=crops,
                   title=titulo)
    fig2.add_annotation(x=2010, y=0.95*min(dados[crops]),
            text="Fonte: IBGE",
            showarrow=False,
            yshift=10)
    st.plotly_chart(fig2)

#
def format_number(num, pref=''):
    if num > 1000:
        if num > 1000000:
            return f'{round(num / 1000000,1)} Milhão {pref}' 
        return f'{round(num / 1000, 1)} Mil {pref}'
    return f'{round(num, 1)} {pref}'
#     
def format_valor(num):
    if num > 1000:
        if num > 1000000:
            return f'R$ {round(num / 1000000,1)} Bilhão' 
        return f'R$ {round(num / 1000, 1)} Milhão'
    return f'R$ {round(num, 1)} Mil'
#          
##
# dados básicos dos municípios
git = 'https://raw.githubusercontent.com/rllopes2uem/Agricultura/refs/heads/main/'
df_dados_ac = load_data(git + 'Dados_AC_10_2xA.csv', git + 'Dados_AC_10_2xB.csv')
df_dados_qp = load_data(git + 'Dados_QP_10_2xA.csv', git + 'Dados_QP_10_2xB.csv')
df_dados_vp = load_data(git + 'Dados_VP_10_2xA.csv', git + 'Dados_VP_10_2xB.csv')
df_dados_rd = load_data(git + 'Dados_RD_10_2xA.csv', git + 'Dados_RD_10_2xB.csv')
Temp = lavouras(git + 'Temp.csv') 
Perm = lavouras(git + 'Perm.csv') 
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
    
    culturas = df_dados_ac.columns[10:].tolist()
    #culturas.insert(0,"Temporárias")
    #culturas.insert(1,"Permanentes")
    cultura = st.selectbox("Selecione a Cultura", options=(culturas))
    #
    press_button = st.button('Mostrar')
    #
    if press_button: #st.button('Submit'):
        #df_dados_ac, df_dados_pr, df_dados_vb,
        D_Area = df_dados_ac[(df_dados_ac.NAME_UF==state_selec)&(df_dados_ac.MUNIC==munic_selec)][cultura]
        D_Prod = df_dados_qp[(df_dados_qp.NAME_UF==state_selec)&(df_dados_qp.MUNIC==munic_selec)][cultura]
        D_Valor = df_dados_vp[(df_dados_vp.NAME_UF==state_selec)&(df_dados_vp.MUNIC==munic_selec)][cultura]
        D_Rend = df_dados_rd[(df_dados_rd.NAME_UF==state_selec)&(df_dados_rd.MUNIC==munic_selec)][cultura]

    #
        map_munic(state_selec, munic_selec,df_dados_ac)
        tab1, rank1 = tab_lav(df_dados_qp, state_selec, munic_selec,cultura,1)
        tab2, rank2 = tab_lav(df_dados_rd, state_selec, munic_selec,cultura,2)
    #    st.write('O estado conta com ', nMun, ' Municípios')
# App layout
col = st.columns((1.5, 3.25, 3.25), gap='small')
## Column 1
with col[0]:
    if press_button:
        with st.container(border=True):
                ac1 = D_Area.iloc[-1]
                ac2 = D_Area.iloc[-2]
                if ac2 != 0:
                    Dac = ((ac1-ac2)/ac2)
                    st.metric(label="Área",
                              value= format_number(ac1,'ha'), 
                              delta="{:.3f} %".format(Dac))
                    del(Dac)
                else:
                    st.write('Sem Informações')
                del(ac1,ac2)
        #
        with st.container(border=True):
                pd1 = D_Prod.iloc[-1]
                pd2 = D_Prod.iloc[-2]
                if pd2 != 0:
                    Dpd = ((pd1-pd2)/pd2)
                    st.metric(label="Produção", 
                              value= format_number(pd1,'ton.'), 
                              delta="{:.3f} %".format(Dpd))
                    del(Dpd)
                else:
                    st.write('Sem Informações')
                del(pd1,pd2)
        #
        with st.container(border=True):
                vl1 = D_Valor.iloc[-1]
                vl2 = D_Valor.iloc[-2]
                if vl2 != 0:
                    Dvl = ((vl1-vl2)/vl2)
                    st.metric(label="Valor", 
                              value=format_valor(vl1), 
                              delta="{:.3f} %".format(Dvl))
                    del(Dvl)
                else:
                    st.write('Sem Informações')
                del(vl1,vl2)
        #
        with st.container(border=True):
                pdv1 = D_Rend.iloc[-1]
                pdv2 = D_Rend.iloc[-2]
                if pdv2 != 0:
                    Dpdv = ((pdv1-pdv2)/pdv2)
                    st.metric(label="Produtividade", 
                              value=format_number((pdv1/1000),'ton/ha'), 
                              delta="{:.3f} %".format(Dpdv))
                    del(Dpdv)
                else:
                    st.write('Sem Informações')
                del(pdv1,pdv2)
                #
        with st.container(border=True):
                ac1 = D_Area.iloc[-1]
                ac2 = D_Area.iloc[-2]
                vl1 = D_Valor.iloc[-1]
                vl2 = D_Valor.iloc[-2]
                if ac2!=0:
                    rnt1 = (vl1/ac1)
                    rnt2 = (vl2/ac2)
                    Dpdv = ((rnt1-rnt2)/rnt2)
                    st.metric(label="Renda da Terra", 
                              value=format_valor(rnt1)+'/ha', 
                              delta="{:.3f} %".format(Dpdv))
                    del(rnt1,rnt2,Dpdv)
                else:
                    st.write('Sem Informações')
                del(ac1,ac2,vl1,vl2)
#
## Column 2
with col[1]:
    if press_button:
        graf_linha(state_selec, munic_selec, cultura, 1)

        graf_linha(state_selec, munic_selec, cultura, 3)
        #
        st.write('Produção Estadual, em Toneladas - 2023')
        if int(rank1.iloc[0]) >4:
            st.dataframe(tab1.style.map(lambda _: 'color:blue;background-color: yellow', subset=(tab1.index[4:,],)), hide_index=True)
        else:
            a = int(rank1.iloc[0])
            b = a - 1
            st.dataframe(tab1.style.map(lambda _: 'color:blue;background-color: yellow', subset=(tab1.index[b:a,],)),
                         #tab1.style.format({'Produção (ton.)':'{:.2f}'}),
                         hide_index=True)

#
## Column 3
with col[2]:
    if press_button:
        graf_linha(state_selec, munic_selec, cultura, 2)
        
        graf_linha(state_selec, munic_selec, cultura, 4)
        #
        st.write('Produtividade Estadual, em Kg/ha - 2023')
        if int(rank2.iloc[0]) >4:
            st.dataframe(tab2.style.map(lambda _: 'color:blue;background-color: yellow', subset=(tab2.index[4:,],)),hide_index=True)
        else:
            a = int(rank2.iloc[0])
            b = a - 1
            st.dataframe(tab2.style.map(lambda _: 'color:blue;background-color: yellow', subset=(tab2.index[b:a,],)),hide_index=True)
