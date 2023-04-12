import pymysql
import pandas as pd
import requests
import decouple
import math
import sqlalchemy as sal
import datetime as dt
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor
from pandas.io.sql import DatabaseError
from pymysql.err import IntegrityError

import Tickers as tick

config = decouple.AutoConfig(' ')

def db_connect():
    user = config('AWS_MY_DB_ADMIN_USER')
    host = config('AWS_MY_DB_ADMIN_HOST')
    dbname = config('AWS_MY_DB_ADMIN_DBNAME')
    pw = config('AWS_MY_DB_ADMIN_PW')
    port = int(config('AWS_MY_DB_ADMIN_PORT'))

    con_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, pw, host, port, dbname)
    print(con_str)
    engine = create_engine(con_str, echo=False)
    con = engine.connect()

    return con

def drop_tables(tables=['option_prices', 'options', 'stock_prices', 'stocks']):
    
    con = db_connect()
    for tab in tables:
        qstr = 'DROP TABLE {}'.format(tab)
        con.execute(qstr)
    
    con.close()
    
def create_tables(tables=['stocks', 'stock_prices', 'options', 'option_prices']):
    con = db_connect()
    
    # create stocks table
    if 'stocks' in tables:
        qstr_list = ['CREATE TABLE IF NOT EXISTS stocks ',
                     '(ticker VARCHAR(5) NOT NULL UNIQUE, ',
                     'PRIMARY KEY(ticker))']
        qstr = "".join(qstr_list)
        con.execute(qstr)
    
    # create stock_prices table
    if 'stock_prices' in tables:
        qstr_list = ['CREATE TABLE IF NOT EXISTS stock_prices ',
                     '(id VARCHAR(17) NOT NULL, ticker VARCHAR(5), date DATETIME, ',
                     'price FLOAT(10), high FLOAT(10), low FLOAT(10), ',
                     'volume INT(12), ',
                     'PRIMARY KEY (id), FOREIGN KEY (ticker) REFERENCES stocks(ticker))']

        qstr = "".join(qstr_list)
        con.execute(qstr)
    
    # create options table
    if 'options' in tables:
        qstr_list = ['CREATE TABLE IF NOT EXISTS options ',
                     '(oid VARCHAR(19) NOT NULL, ticker VARCHAR(5), expiration DATE, strike FLOAT(8), ',
                     'type VARCHAR(1), PRIMARY KEY (oid), FOREIGN KEY (ticker) REFERENCES stocks(ticker))']

        qstr = "".join(qstr_list)
        con.execute(qstr)
    
    # create option_prices table
    if 'option_prices' in tables:
        qstr_list = ['CREATE TABLE IF NOT EXISTS option_prices ',
                     '(id INT NOT NULL AUTO_INCREMENT, oid VARCHAR(19), spid VARCHAR(17), ticker VARCHAR(5), ',
                     'bid FLOAT(10), ask FLOAT(10), fv FLOAT(10), volume INT(12), oi INT(10), iv FLOAT(8), ',
                     'date DATETIME, ttm INT(4), ', 'PRIMARY KEY (id), ',
                     'FOREIGN KEY (oid) REFERENCES options (oid), ',
                     'FOREIGN KEY (spid) REFERENCES stock_prices (id), ',
                     'FOREIGN KEY (ticker) REFERENCES stocks (ticker))']


        qstr = "".join(qstr_list)
        con.execute(qstr)
    
    # close con
    con.close()

def insert_stock(tickers):
    tickers = pd.DataFrame(data=tickers, columns=['ticker'])
    con = db_connect()
    
    try:
        tickers.to_sql('stocks', con, if_exists='append', index=False)
        print("Successfully inserted data into stocks")
    except IntegrityError as e:
        print(f'Query failed!\n\n{e}')
    except sal.exc.IntegrityError as e:
        print(f'Query failed!\n\n{e}')
    except DatabaseError as e:
        print(f'Query failed!\n\n{e}')

    con.close()  
    


def upload_data(tickers):
    """This function pulls data from yfinance and uploads to MYSQL DB"""
    
    # pull data from yfinance
    data = []
    with ThreadPoolExecutor() as executor:
        try:
            res = executor.map(tick.get_data_yq, tickers)
            for r in res:
                data.append(r)
        except:
            print("Failed to upload Data")
    
    # concat dfs for each ticker
    do = [data[i][0] for i in range(len(data))]
    do = pd.concat(do)
    ds = [data[i][1] for i in range(len(data))]
    ds = pd.concat(ds)
    
    # create specific df for options and option_prices table
    d_o = do[['oid', 'symbol', 'expiration', 'strike', 'optionType']]
    d_o.columns = ['oid', 'ticker', 'expiration', 'strike', 'type']
    
    # load previous option dataframe and compare columns to ensure no duplicate entries
    try:
        df_temp = pd.read_csv("tmp_df.csv", index_col='Unnamed: 0')
        d_o = d_o[~d_o['oid'].isin(df_temp['oid'])]
    except:
        print("Could not find temp df")
    
    # create third df for insert into option prices
    d_op = do[['oid', 'spid', 'symbol', 'bid', 'ask', 'fv',
              'volume','openInterest', 'impliedVolatility', 'date', 'ttm']]
    d_op.columns = ['oid', 'spid', 'ticker', 'bid', 'ask', 'fv',
                    'volume', 'oi', 'iv', 'date', 'ttm']
    
    
    con = db_connect()
    
    # Upload data to db
    print(dt.datetime.now())
    
    try:
        ds.to_sql('stock_prices', con, if_exists='append', index=False)
        print("Successfully inserted data into stock_prices")
    except IntegrityError as e:
        print(f'Query failed!\n\n{e}')
    except sal.exc.IntegrityError as e:
        print(f'Query failed!\n\n{e}')
    except DatabaseError as e:
        print(f'Query failed!\n\n{e}')
        
    try:
        d_o.to_sql('options', con, if_exists='append', index=False)
        print("Successfully inserted data into options")
    except IntegrityError as e:
        print(f'Query failed!\n\n{e}')
    except sal.exc.IntegrityError as e:
        print(f'Query failed!\n\n{e}')
    except DatabaseError as e:
        print(f'Query failed!\n\n{e}')
        
    try:
        d_op.to_sql('option_prices', con, if_exists='append', index=False)
        print("Successfully inserted data into option_prices")
    except IntegrityError as e:
        print(f'Query failed!\n\n{e}')
    except sal.exc.IntegrityError as e:
        print(f'Query failed!\n\n{e}')
    except DatabaseError as e:
        print(f'Query failed!\n\n{e}')
        
    # store d_o as a temporary csv file for future uploads
    
    qstr = "SELECT * FROM options"
    res = con.execute(qstr)
    df_temp = res.fetchall()
    df_temp = pd.DataFrame(df_temp)
    
    df_temp.to_csv("tmp_df.csv")
        
    con.close()
        
        
        
