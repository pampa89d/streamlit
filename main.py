import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

import warnings
warnings.filterwarnings('ignore') 

st.title('Data analysis application')
upload_file = st.file_uploader('Choose CSV file', type='CSV')

# 1. data processing
@st.cache_data  # Add caching for better performance
def load_data(path) -> pd.DataFrame:
    # read and preparung file
    tips = pd.read_csv(path, sep=',')
    day_dict = {'Thur': 1, 'Fri': 2, 'Sat': 3, 'Sun': 4}
    tips.sort_values(by='day', key=lambda x: x.map(day_dict), 
                     inplace=True)
    tips.drop('Unnamed: 0', axis=1, inplace=True)
    return tips

@st.cache_data
def add_time_col(df: pd.DataFrame, col_name: str,
                 start_date = '2023-01-01',
                 end_date = '2023-01-31') -> pd.DataFrame:
    date_range = pd.date_range(start=start_date, end=end_date, freq='D').to_list()
    df[col_name] = np.random.choice(date_range, size=df.shape[0])
    return df

def plot_tips_dynamic(df: pd.DataFrame):
    tips_by_tm = df.loc[:, ['time_order', 'tip']].groupby(
            pd.Grouper(key='time_order', freq='D')).sum()
    tips_by_tm.reset_index(inplace=True)
    fig, ax = plt.subplots(figsize=(6, 4), dpi=50)
    fig.set_facecolor("#c3e2cf")
    ax.set_facecolor("#ECF0F0")
    ax.plot(tips_by_tm['time_order'].dt.day, tips_by_tm['tip'])
    ax.xaxis.set_major_locator(MaxNLocator(10))                              # reduce X iterval,  import requires
    ax.axhline(y=tips_by_tm['tip'].mean(), color='red', 
            linestyle='--', linewidth=2, alpha=0.7, 
            label='mean tips')   # set line on grid
    plt.xlim(1, tips_by_tm['time_order'].shape[0])
    plt.xlabel('day of month', size=7)
    plt.ylabel('tips', size=7)
    plt.xticks(size=7)
    plt.yticks(size=7)
    plt.legend(fontsize=7)
    plt.grid()
    st.pyplot(fig)

def total_bill(df: pd.DataFrame):
    g = sns.relplot(data=df, x=df['time_order'].dt.day, y='total_bill',
            hue='day', kind='line', height=15, aspect=1.2)
    # kind=line() show mean values and 95% Confidence inteval
    g.map(plt.axhline, y=df['total_bill'].mean(), color="#AB0CF5", 
          linestyle='--', alpha=0.9)
    g._legend.remove()
    plt.xlabel('day of month', size=25)
    plt.ylabel('bill size', size=25)
    plt.xticks(size=25)
    plt.yticks(size=25)
    plt.legend(frameon=True, fontsize=25)
    plt.grid()
    st.pyplot(g)

def relat_bill(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4), dpi=50)
    fig.set_facecolor("#c3e2cf")
    ax.set_facecolor("#ECF0F0")
    sns.scatterplot(data=df, x='total_bill', y='tip', hue='day', legend='auto')
    ax.set_xlabel('bill', size=7)
    ax.set_ylabel('tip', size=7)
    ax.tick_params(axis='x', size=7)
    ax.tick_params(axis='y', size=7)
    plt.xticks(size=7)
    plt.yticks(size=7)
    plt.grid(linestyle='--')
    plt.legend(fontsize=7)
    plt.show()
    st.pyplot(fig)

# 2. upload file
if upload_file is not None:
    tips = load_data(upload_file)
    st.write(tips.head())
    # add column with days
    tips = add_time_col(tips, 'time_order')

    # add dynamic tips plot due to time
    st.write('#### Dynamic tips due to time')
    plot_tips_dynamic(tips)

    # add dynamic tips plot due to time
    st.write('#### Total bill plot')
    total_bill(tips)

    # add dynamic tips plot due to time
    st.write('#### Relationship beetween total bill and tips')
    relat_bill(tips)

else:
    st.stop()
