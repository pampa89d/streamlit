import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import yfinance as yf
from datetime import datetime

import warnings
warnings.filterwarnings('ignore') 

# choose your company ticker if you need
company_ticker = 'AAPL'

# get data from ticker
ticker_data = yf.Ticker(company_ticker)
# get historical prices
ticker_df = ticker_data.history(period='1d', start='2020-6-1', end='2025-5-31')
# get company name from ticker
company_name = ticker_data.info['longName']

st.title('Stock quotes %s' % (company_name))
st.write(ticker_df.head(3))

stock_types = tuple(ticker_df.columns)
option_1 = st.selectbox('Please choose stock data', stock_types, key="selectbox_1")
#st.line_chart(ticker_df[option_1])

option_2 = st.selectbox('Please choose stock data', stock_types, key="selectbox_2")
#st.line_chart(ticker_df[option_2])

def boxplot(df: pd.DataFrame):
    df = df.loc[:, ['Open', 'Close']]
    df = df.stack(future_stack=True)
    df = df.reset_index()
    df = df.rename(columns={'level_1': 'Period', 0: 'Price'})
    df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')
    df['Date'] = pd.to_datetime(df['Date'], errors='ignore')
    df = df.groupby([pd.Grouper(key='Date', freq='MS'), 'Period'], as_index=False).agg(
        {'Price': [np.min, np.max]})
    df.columns = df.columns.droplevel(1)
    df.columns.values[2] = 'min'
    df.columns.values[3] = 'max'
    df.drop(columns=['Period'], inplace=True)
    df.set_index('Date', inplace=True)
    df = df.stack(future_stack=True)
    df = df.reset_index()
    df.columns.values[1] = 'Type'
    df.columns.values[2] = 'Price'
    df = df.groupby([pd.Grouper(key='Date', freq='MS'), 'Type'], as_index=False).mean()
    st.write(df.head())
    option_strt = st.selectbox('Please choose start date', df['Date'].to_list(),
                                key="selectbox_3")
    option_end = st.selectbox('Please choose end date', df['Date'].to_list(), 
                                key="selectbox_4")
    df = df[(df['Date'] > np.datetime64(option_strt)) &
            (df['Date'] < np.datetime64(option_end))]
    st.write(df.head())

    fig = plt.figure(figsize=(10, 10))
    sns.boxplot(data=df, x='Date', y='Price')
    st.pyplot(fig)

boxplot(ticker_df)