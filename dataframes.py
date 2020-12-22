import pandas as pd
import numpy as np
import moonFunctions as mf
from datetime import datetime

# Moon data frame
def moon_frames():
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
    #print(m_df.describe())
    return m_df

# FTSE Data Frame
def ftse_frame():
    global f_df
    fd = pd.read_csv("FTSE 100 - 1984-2020.csv")
    f_df = pd.DataFrame(fd)
    f_df.rename(
        columns={'Date': 'date', 'Open': 'open_d-1', 'High': 'high_d-1', 'Low': 'low_d-1', 'Close_': 'close_d-1', 'AdjClose__':'result'},
        inplace=True)
    f_df['date'] = pd.to_datetime(f_df['date'], format="%b %d, %Y")
    f_df['weekday'] = f_df['date'].dt.dayofweek
    f_df['month'] = f_df['date'].dt.month
    f_df['open_d-1'] = f_df['open_d-1'].shift(-1)
    f_df['high_d-1'] = f_df['high_d-1'].shift(-1)
    f_df['low_d-1'] = f_df['low_d-1'].shift(-1)
    f_df['close_d-1'] = f_df['close_d-1'].shift(-1)
    ff_df = f_df[['date', 'open_d-1','high_d-1','low_d-1', 'close_d-1', 'result']]
    #print(f_df.head())
    return ff_df

# weather data frame
def weather_frames():
    wd = pd.read_csv('weather.csv')
    w_df = pd.DataFrame(wd)
    w_df['date_str'] = w_df['dt_iso'].apply(lambda x: str(x))
    w_df['date'] = w_df['date_str'].map(lambda x: x.rstrip(':00: +0000 UTC'))
    ws7_df = w_df[w_df['date_str'].str.contains('07:00:00')]
    ws19_df = w_df[w_df['date_str'].str.contains('19:00:00')]
    wf7_df = ws7_df[['date','feels_like','pressure','rain_1h','weather_id']]
    wf7_df.rename(
        columns={'feels_like': 'feels_like_07', 'pressure': 'pressure_07', 'rain_1h': 'rain_1h_07', 'weather_id': 'weather_id_07'},
        inplace=True)
    wf7_df['date'] = pd.to_datetime(wf7_df['date'], format="%Y-%m-%d 07")
    wf19_df = ws19_df[['date','feels_like','pressure','rain_1h','weather_id']]
    wf19_df.rename(
        columns={'feels_like': 'feels_like_19-1', 'pressure': 'pressure_19-1', 'rain_1h': 'rain_1h_19-1', 'weather_id': 'weather_id_19-1'},
        inplace=True)
    wf19_df['date'] = pd.to_datetime(wf19_df['date'], format="%Y-%m-%d 19")
    wff_df = pd.merge(wf19_df, wf7_df, on='date')
    wff_df['feels_like_19-1'] = wff_df['feels_like_19-1'].shift(1)
    wff_df['pressure_19-1'] = wff_df['pressure_19-1'].shift(1)
    wff_df['rain_1h_19-1'] = wff_df['rain_1h_19-1'].shift(1)
    wff_df['weather_id_19-1'] = wff_df['weather_id_19-1'].shift(1)
    wff_df = wff_df.fillna(0)
    #print(wff_df.head())
    return wff_df

def uncertenty_frame():
    u_df = pd.read_csv('data/UK_Daily_Policy_Data.csv')
    u_df['date'] = pd.to_datetime([f'{y}-{m}-{d}' for y, m, d in zip(u_df.year, u_df.month, u_df.day)])
    u_df.rename(
        columns={ 'daily_policy_index':'daily_policy_index_d-1'},
        inplace=True)
    u_df['daily_policy_index_d-1'] = u_df['daily_policy_index_d-1'].shift(1)
    print(u_df.isnull().sum().sum())
    u_df = u_df.dropna()
    fu_df = u_df[['date', 'daily_policy_index_d-1']]
    #print(fu_df.head())
    return fu_df

def gold_frame():
    g_df = pd.read_csv('data/gold.csv')
    g_df = g_df.dropna()
    g_df.rename(
        columns={'Date': 'date', 'Open': 'gold_open_d-1', 'High': 'gold_high_d-1', 'Low': 'gold_low_d-1', 'Close_': 'gold_close_d-1'},
        inplace=True)
    g_df['date'] = pd.to_datetime(g_df['date'], format="%b %d, %Y")
    g_df['gold_open_d-1'] = g_df['gold_open_d-1'].shift(-1)
    g_df['gold_high_d-1'] = g_df['gold_high_d-1'].shift(-1)
    g_df['gold_low_d-1'] = g_df['gold_low_d-1'].shift(-1)
    g_df['gold_close_d-1'] = g_df['gold_close_d-1'].shift(-1)
    return g_df[['date','gold_open_d-1','gold_high_d-1','gold_low_d-1','gold_close_d-1']]

def oil_frame():
    o_df = pd.read_csv('data/crudeOil.csv')
    o_df = o_df.dropna()
    o_df.rename(
        columns={'Date': 'date', 'Open': 'oil_open_d-1', 'High': 'oil_high_d-1', 'Low': 'oil_low_d-1', 'Close_': 'oil_close_d-1'},
        inplace=True)
    o_df['date'] = pd.to_datetime(o_df['date'], format="%b %d, %Y")
    o_df['oil_open_d-1'] = o_df['oil_open_d-1'].shift(-1)
    o_df['oil_high_d-1'] = o_df['oil_high_d-1'].shift(-1)
    o_df['oil_low_d-1'] = o_df['oil_low_d-1'].shift(-1)
    o_df['oil_close_d-1'] = o_df['oil_close_d-1'].shift(-1)
    #print(o_df.head())
    return o_df[['date','oil_open_d-1','oil_high_d-1','oil_low_d-1','oil_close_d-1']]

def vix_frame():
    v_df = pd.read_csv('data/vix.csv')
    v_df = v_df.dropna()
    v_df.rename(
        columns={'Date': 'date', 'Open': 'vix_open_d-1', 'High': 'vix_high_d-1', 'Low': 'vix_low_d-1', 'Close_': 'vix_close_d-1'},
        inplace=True)
    v_df['date'] = pd.to_datetime(v_df['date'], format="%b %d, %Y")
    v_df['vix_open_d-1'] = v_df['vix_open_d-1'].shift(-1)
    v_df['vix_high_d-1'] = v_df['vix_high_d-1'].shift(-1)
    v_df['vix_low_d-1'] = v_df['vix_low_d-1'].shift(-1)
    v_df['vix_close_d-1'] = v_df['vix_close_d-1'].shift(-1)
    #print(o_df.head())
    return v_df[['date','vix_open_d-1','vix_high_d-1','vix_low_d-1','vix_close_d-1']]


def merge_frames(f1, f2,f3):
    f = pd.merge(f1,f2, on='date')
    final = pd.merge(f,f3, on='date')
    final = final.dropna()
    auto_final = final.iloc[0:2000]
    uncert_final = pd.merge(final, uncertenty_frame())
    #print(uncert_final.head(10))
    #print(uncert_final.describe())
    #uncert_final.to_csv('final_with_uncert.csv')
    all_df = pd.merge(final, gold_frame(), on='date')
    all_df = pd.merge(all_df, oil_frame(), on='date')
    all_df = pd.merge(all_df, vix_frame(), on='date')
    print(all_df.columns)
    all_df.to_csv('all_in.csv')
    #auto_final.to_csv("final_to_test.csv")
    return final

#print("Oil:\n",oil_frame().head(),"\n Gold: \n", gold_frame().head(), "\nVix:\n", vix_frame().head())
#uncertenty_frame()
#moon_frames()
#weather_frames()
#ftse_frame()
merge_frames(moon_frames(),weather_frames(), ftse_frame())
#merge_frames(moon_frames(),weather_frames(), ftse_frame()).to_csv('final_data.csv')
#print(merge_frames(moon_frames(),weather_frames(), ftse_frame()).describe())
