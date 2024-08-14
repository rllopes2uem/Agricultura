import pandas as pd
import numpy as np
import plotly.express as px
#
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
