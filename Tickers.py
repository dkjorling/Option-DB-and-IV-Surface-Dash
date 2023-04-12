# import libraries
import pandas as pd
import numpy as np
import yahooquery as yq
import yfinance as yf
import datetime as dt

def init_tickers():
    sp500 = pd.read_csv(main_data_path + 'sp500.csv')
    ndx100 = pd.read_csv(main_data_path + 'ndx.csv')
    top_etfs = pd.read_csv(main_data_path + 'top_etfs.csv')
    top_com_etfs = pd.read_csv(main_data_path + 'top_com_etfs.csv')

    sp500_list = list(sp500['Symbol'])
    ndx100_list = list(ndx100['Symbol'])
    top_etfs_list = list(top_etfs['Symbol'])
    top_com_etfs_list = list(top_com_etfs['Ticker'])

    tickers = sp500_list + ndx100_list + top_etfs_list + top_com_etfs_list
    tickers = sorted(list(set(tickers)))


    ### Check for bad tickers ###
    bad = []
    for t in tickers:
        try:
            tick.get_data([t])
        except:
            print("{} has no options".format(t))
            bad.append(t)
        
    for b in bad:
        tickers.remove(b)
    print(len(tickers))
    
    return tickers

def get_price(ticker):
    t = yf.Ticker(ticker)
    fi = t.fast_info
    price = np.round(fi['lastPrice'], 2)
    return str(price)

def get_data(tickers):
    """This function pulls options data for specified tickers passed in a list"""
    
    # create empty dictionaries to store stock and option dfs
    ticker_dict_stocks = {}
    ticker_dict_options = {}
    # iterate through each ticker
    for ticker in tickers:
        
        # create yf object
        t = yf.Ticker(ticker)
        fi = t.fast_info
        
        # take timestamp and clarify open or close...could potentially move time data into the load_data function??
        time = dt.datetime.now()
        if time.hour < 12:
            oc = 'o'
        else:
            oc = 'c'
        
        # iterate through options expirations
        options = t.options
        exp_dfs = []
        for exp in options:
            chain = t.option_chain(exp)
            df = pd.concat([chain.calls, chain.puts], axis=0).reset_index().drop('index', axis=1)
            exp_dfs.append(df)
            #print("Exp {} added".format(exp))
        
        # concat expirations into single df
        df_option = pd.DataFrame()
        for df in exp_dfs:
            df.drop(columns=['lastTradeDate','lastPrice','inTheMoney', 'contractSize',
                             'currency', 'change', 'percentChange'], inplace=True)
            if df_option.shape[0] == 0:
                df_option = df
            else:
                df_option = pd.concat([df_option, df], axis=0)
        
        # feature engineer
        df_option = df_option.reset_index().drop('index', axis=1)
        df_option['date'] = time.date()
        df_option['time'] = time.time()
        df_option['expiration'] = df_option['contractSymbol'].str.extract(r'(\d{6})[CP]')
        df_option['expiration'] = pd.to_datetime(df_option['expiration'], format='%y%m%d')
        df_option['ttm'] = (df_option['expiration'] - dt.datetime.now()).dt.days
        df_option['type'] = df_option['contractSymbol'].str.extract(r'\d{6}([CP])')
        df_option['ticker'] = df_option['contractSymbol'].str.extract(r'(\w+)\d{6}[CP]')
        df_option['fv'] = np.round((df_option['bid'] + df_option['ask']) / 2, 2)
        df_option.drop(columns=['contractSymbol'], inplace=True)
        df_option['oc'] = oc
        df_option['price'] = np.round(fi['lastPrice'], 2)
        
        # create stock df
        df_stock = pd.DataFrame(columns=['date', 'time', 'ticker',
                                         'price', 'high', 'low',
                                         'market_cap', 'volume', 'oc'],
                                index=np.zeros(1))
        
        df_stock['date'] = time.date()
        df_stock['time'] = time.time()
        df_stock['ticker'] = t.ticker
        df_stock['price'] = np.round(fi['lastPrice'], 2)
        df_stock['high'] = np.round(fi['dayHigh'], 2)
        df_stock['low'] = np.round(fi['dayLow'], 2)
#        df_stock['market_cap'] = fi['marketCap']
        df_stock['volume'] = fi['lastVolume']
        df_stock['oc'] = oc
        
        # insert dfs into dictionary
        ticker_dict_options[ticker] = df_option
        ticker_dict_stocks[ticker] = df_stock
    
    if len(ticker_dict_options) == 1:
        return ticker_dict_options[tickers[0]], ticker_dict_stocks[tickers[0]]
    else:
        return ticker_dict_options, ticker_dict_stocks
    
def get_data_yq(ticker):
    """This function pulls options data for specified ticker"""
    # create yq object
    t = yq.Ticker(ticker)
    price = yf.Ticker(ticker).fast_info['lastPrice']
    time = dt.datetime.now()
        
    # get options data
    dfo = t.option_chain
    dfo.drop(columns=['contractSymbol', 'currency', 'lastPrice', 'change',
                 'percentChange', 'contractSize', 'lastTradeDate', 'inTheMoney'], inplace=True)
    dfo.reset_index(inplace=True)
    dfo['date'] = time
    dfo['optionType'] = dfo['optionType'].str[0].str.upper()
    dfo['oid'] = dfo['symbol'] + dfo['expiration'].dt.strftime('%y%m%d') + '_' + dfo['strike'].astype(str) + dfo['optionType']
    dfo['spid'] = dfo['symbol'] + dfo['date'].dt.strftime('%y%m%d_%H:%M')
    dfo['ttm'] = (dfo['expiration'] - dfo['date']).dt.days
    dfo['fv'] = np.round((dfo['bid'] + dfo['ask']) / 2, 2)
    dfo['impliedVolatility'] = np.round(dfo['impliedVolatility'], 4)
    
    # get stock data
    dfs = pd.DataFrame(columns=['id', 'ticker', 'date', 'price', 'high', 'low', 'volume'],
                            index=np.zeros(1))
    sd = t.summary_detail[ticker]
    dfs['ticker'] = ticker
    dfs['date'] = time
    dfs['price'] = np.round(price, 2)
    dfs['high'] = sd['dayHigh']
    dfs['low'] = sd['dayLow']
    dfs['volume'] = int(sd['volume'] / 1000)
    dfs['id'] = dfs['ticker'] + dfs['date'].dt.strftime('%y%m%d_%H:%M')
        
    return dfo, dfs
    
    
def get_data_yq_grouped(tickers):
    """This function pulls options data for specified tickers passed in list"""
    # create yq object
    ticker_string = " ".join(tickers)
    t = yq.Ticker(ticker_string)
    time = dt.datetime.now()
        
    # get options data
    dfo = t.option_chain
    dfo.drop(columns=['contractSymbol', 'currency', 'lastPrice', 'change',
                 'percentChange', 'contractSize', 'lastTradeDate', 'inTheMoney'], inplace=True)
    dfo.reset_index(inplace=True)
    dfo['date'] = time
    
    # get stock data
    dfs = pd.DataFrame(columns=['date', 'ticker', 'price', 'high', 'low', 'volume'],
                            index=np.zeros(len(tickers)))
    sd = t.summary_detail
    dfs['date'] = [time for tick in tickers]
    dfs['ticker'] = [tick for tick in tickers]
    dfs['price'] = [sd[tick]['bid'] for tick in tickers]
    dfs['high'] = [sd[tick]['dayHigh'] for tick in tickers]
    dfs['low'] = [sd[tick]['dayLow'] for tick in tickers]
    dfs['volume'] = [sd[tick]['volume'] for tick in tickers]
    
        
    return dfo, dfs
    
    
