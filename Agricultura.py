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
def load_data1(url1,url2,url3,url4):
  git = 'https://raw.githubusercontent.com/rllopes2uem/classDashBoard/main/'
  file1 = 'Dados_AC_10_22.csv'
  file2 = 'Dados_QP_10_22.csv'
  file3 = 'Dados_VP_10_22.csv'
  Area = pd.read_csv(git+file1)
  Producao = pd.read_csv(git+file2)
  Valor = pd.read_csv(git+file3)
  Ano = Area['Ano'].unique().tolist()
  cult_temp = pd.read_csv(git + 'Temp.csv',sep=';', header=None)[0].values.tolist()
  cult_perm = pd.read_csv(git + 'Perm.csv',sep=';', header=None)[0].values.tolist()

##
