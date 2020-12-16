import pandas as pd
import numpy as np
import moonFunctions as mf
from datetime import datetime

md2 = pd.read_csv("Moon phase on 3 January 1984P2.csv")
md1 = pd.read_csv("Moon phase on 3 January 1984.csv")
m_df  = pd.DataFrame(md1)
m_df2 = pd.DataFrame(md2)

m_df = m_df.append(m_df2)
m_df.rename(columns = {'Text1':'dist_to_moon','Date':'date'}, inplace = True)
m_df['date'] = m_df['date'].map(lambda x: x.lstrip('Moon phase details at '))
m_df['date'] = m_df['date'].map(lambda x:datetime.strptime(x, "%d %B %Y"))
m_df['dist_to_moon'] = m_df['dist_to_moon'].map(lambda x: x.rstrip('km').replace(",",""))
m_df['illumination'] = m_df['illumination'].map(lambda x: x.rstrip('% Visible'))

fd = pd.read_csv("^FTSE.csv")
f_df = pd.DataFrame(fd)
f_df.rename(columns = {'Date':'date'}, inplace = True)
f_df['date'] = f_df['date'].map(lambda x:datetime.strptime(x, "%Y-%m-%d"))
final = pd.merge(m_df, f_df, on='date')
print(m_df.size)
