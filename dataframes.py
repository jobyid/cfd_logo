import pandas as pd
import numpy as np
import moonFunctions as mf
from datetime import datetime

# Moon data frame
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
m_df.sort_values(by=['date'], inplace=True)

# FTSE Data Frame
fd = pd.read_csv("FTSE 100 - 1984-2020.csv")
f_df = pd.DataFrame(fd)
f_df.rename(columns = {'Date':'date','Open':'open_d-1', 'High':'high_d-1','Low':'low_d-1', 'Close_':'close_d-1'}, inplace = True)
f_df['date'] = pd.to_datetime(f_df['date'], format="%b %d, %Y")
f_df['weekday'] = f_df['date'].dt.dayofweek
f_df['month'] = f_df['date'].dt.month
f_df['open_d-1'] = f_df['open_d-1'].shift(-1)
f_df['high_d-1'] = f_df['high_d-1'].shift(-1)
f_df['low_d-1'] = f_df['low_d-1'].shift(-1)
f_df['close_d-1'] = f_df['close_d-1'].shift(-1)
# Adjusted Close is the result, d-1 columns are the day before figures
# NOTE: .shift() to move columns up or down.


# merged data frame
final = pd.merge(m_df, f_df, on='date')
print(f_df.tail())
##print(m_df.tail())
#print(final.tail())
