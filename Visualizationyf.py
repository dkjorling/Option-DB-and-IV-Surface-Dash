import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
from datetime import datetime as dt
from dash_bootstrap_templates import load_figure_template

import Tickers as tick


def my_template():
    template = load_figure_template("vapor")
    return template

def plot_strike(ticker, strike, end_date=None, option='C'):
    
    df, _ = tick.get_data([ticker])
    if end_date != None:
        df = df[df['expiration'] < end_date]

    #filter df
    df = df[(df['strike'] == strike) & (df['type'] == option) & (df['impliedVolatility'] >= 0.01)][['impliedVolatility', 'expiration', 'type']]
    df = df.groupby('expiration').mean(numeric_only=True)
    
    # plot average IV through time
    title = ticker + " " + str(strike) + " Strike Implied Volatility through Time"
    layout = go.Layout(title=title, xaxis=dict(title='Expiration'), yaxis=dict(title='IV'), template=my_template())
    fig = go.Figure(layout=layout)
    
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['impliedVolatility'],
                            mode='lines'))
    
    return fig

def plot_exp(ticker, exp, option='C'):
    df, _ = tick.get_data([ticker])
    
    df = df[(df['expiration'] == exp) & (df['type'] == option) & (df['impliedVolatility'] >= 0.01)][['impliedVolatility', 'strike', 'type']]
    df = df.groupby('strike').mean(numeric_only=True)
    
    # plot average IV through time
    title = ticker + " " + str(exp) + " Expiration Implied Volatility through Strike Space"
    layout = go.Layout(title=title, xaxis=dict(title='Strike'), yaxis=dict(title='IV'), template=my_template())
    fig = go.Figure(layout=layout)
    
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['impliedVolatility'],
                            mode='lines'))
    
    return fig


def plot_surface(ticker,  option='C', start_date='01-01-21', end_date='12-31-30', pct_cut=(1, 10)):
    df, _ = tick.get_data([ticker])
    
    price = df['price'].mean()
    lower = price - (pct_cut[0] * price)
    upper = price + (pct_cut[1] * price)
    
    df = df[(df['strike'] >= lower) & (df['strike'] <= upper)]
    df = df[(df['expiration'] >= start_date) & (df['expiration'] <= end_date)]
    
    df = df[df['type'] == option]
        
    df = df[['impliedVolatility', 'strike', 'expiration', 'price']]

    title = ticker + " Implied Volatility Surface"
    layout = go.Layout(
                    title=title,
                    scene = dict(
                        xaxis = dict(
                            title='Expiration'),
                        yaxis = dict(
                            title='Strike'),
                        zaxis = dict(
                            title='Implied Vol')),
                    margin=dict(t=35, r=0, l=0, b=0),
                    template=my_template())
    
    fig = go.Figure(layout=layout)
    
    fig.add_trace(go.Mesh3d(z=df['impliedVolatility'],
                                     x=df['expiration'],
                                     y=df['strike']))

    camera = dict(
                eye=dict(x=2, y=2, z=0.1)
            )

    fig.update_layout(scene_camera=camera)
                       

    return fig
                   




