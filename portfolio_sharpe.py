import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from messari.messari import Messari
import config
import time

# Set up Messari instance
MESSARI_API_KEY = config.MESSARI_API_KEY
messari = Messari(api_key=MESSARI_API_KEY)

assets = ['bitcoin', 'ethereum', 'solana']
metric = 'price'
start = '2021-01-01'
end = '2022-01-01'
timeseries_df = messari.get_metric_timeseries(asset_slugs=assets, asset_metric=metric, start=start, end=end)
timeseries_df
closing_price_df=timeseries_df.xs('close', level=1,axis=1)

allocation={'bitcoin':.15,"ethereum":.50, "solana":.35}
for ticker in assets:
    closing_price_df[ticker+' Percent Change']=closing_price_df[ticker]/closing_price_df[ticker].iloc[0]
    closing_price_df[ticker+' Allocation'] = closing_price_df[ticker+' Percent Change']*allocation[ticker]
    closing_price_df[ticker + ' Position'] = closing_price_df[ticker+' Allocation']*1000

all_pos=closing_price_df['bitcoin Position'], closing_price_df['ethereum Position'], closing_price_df['solana Position']
portf_val = pd.concat(all_pos, axis=1)
portf_val['Total Pos']=portf_val.sum(axis=1)

cumulative_return = 100*(portf_val['Total Pos'][-1 ]/portf_val['Total Pos'][0]-1)
portf_val['Daily Return'] = portf_val['Total Pos'].pct_change(1)
sharpe_ratio=portf_val['Daily Return'].mean()/portf_val['Daily Return'].std()
annual_sharpe_ratio=(252**.5)*sharpe_ratio


#This is how to calculate the Sharpe Ratio using stocks

all_stock_df={}
companies=('AAPL', 'CSCO', 'IBM', 'AMZN')

for name in companies:
    all_stock_df[name]=pd.DataFrame()

for ticker in ('AAPL', 'CSCO', 'IBM', 'AMZN'):
    all_stock_df[ticker]=yf.download(ticker, start="2012-01-03", end="2021-12-31")

for ticker in companies:
    all_stock_df[ticker]['Norm return']=all_stock_df[ticker]['Adj Close']/all_stock_df[ticker]['Adj Close'].iloc[0]

for ticker, allocation in zip(companies,[.35,.25,.2,.2]):
    all_stock_df[ticker]['Allocation']=all_stock_df[ticker]['Norm return']*allocation
    all_stock_df[ticker]['Position']=all_stock_df[ticker]['Allocation']*10000


all_pos=[all_stock_df['AAPL']['Position'], all_stock_df['CSCO']['Position'], all_stock_df['IBM']['Position'], all_stock_df['AMZN']['Position']]
portf_val = pd.concat(all_pos, axis=1)
portf_val.columns = ['AAPL Pos','CISCO Pos','IBM Pos','AMZN Pos']
portf_val['Total Pos']=portf_val.sum(axis=1)

plt.style.use('fivethirtyeight')
portf_val.drop('Total Pos', axis=1).plot()

cumulative_return = 100*(portf_val['Total Pos'][-1 ]/portf_val['Total Pos'][0]-1)
portf_val['Daily Return'] = portf_val['Total Pos'].pct_change(1)
sharpe_ratio=portf_val['Daily Return'].mean()/portf_val['Daily Return'].std()
annual_sharpe_ratio=(252**.5)*sharpe_ratio


