import dash_bootstrap_components as dbc
import numpy as np
from dash import Dash, html, dcc, Input, Output, register_page, callback
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output

# import local .py files
import Visualizationyf as vs
import Tickers as tick
from dash_helpers import dashboard_navbar, page_bottom

colors = {
    'bg':'#1a0933',
    'purple':'#6f42c1',
    'font':'#32fbe2',
    'pink':'#ea39b8',
    'green':'#3cf281'
}

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


app.layout = html.Div(
            children=[
                dbc.Row(
                    [
                    html.H3(
                        'Real-Time Option Implied Volatility Surface',
                        style={
                        'color':colors['font'],
                        }
                    )
                    ],
                    style={
                        'font-color':'#32fbe2',
                        'background-color':'#1a0933',
                        'margin':'0px 0px 0px 30px',
                        'width':'110%'
                    }
                ),
                html.Div(
                    children=[
                        html.P(
                            "Ticker:",
                            style={
                                'color':'#32fbe2',
                                'display':'inline-block',
                                'font-size':'20px'
                            }
                        ),
                        dcc.Input(
                            id="sel_asset1",
                            type="text",
                            placeholder="Ticker",
                            value='SPY',
                            style={
                                'background-color': colors['font'],
                                'font-color': colors['purple'],
                                'textAlign':'center',
                                'width':'70px',
                                'display':'inline-block',
                                'margin':'0px 15px 10px 15px'
                            }
                        ),
                        html.Div(
                            id='asset_price',
                            style={
                                'color':'#32fbe2',
                                'font-color':'#32fbe2',
                                'display':'inline-block',
                                'font-size':'20px'
                            }
                        )

                        ],
                        style={
                            'display':'flex',
                            'border-bottom':'3px solid #6f42c1',
                            'padding':'0px 0px 0px 45px',
                            'width':'110%'
                        }
                    ),

                dbc.Row(
                    [
                    dcc.Graph(
                        id='vol_surface',
                        style={
                            'height':'100%'
                        }
                        
                    )
                    ],
                    style={
                        'background-color':'#1a0933',
                        'width':'110%',
                        'border-bottom':'2px solid #44d9e8',
                        
                    }
                ),
                dbc.Row(
                    [
                    dbc.Col(
                        [
                        html.Div(
                            children=[
                                html.P(
                                    "Expiration:",
                                    style={
                                        'color':'#32fbe2',
                                        'display':'inline-block',
                                        'font-size':'20px'
                                    }
                                ),
                                dcc.Input(
                                    id="sel_exp",
                                    type="text",
                                    placeholder="Ticker",
                                    value='12-15-23',
                                    style={
                                        'background-color': colors['font'],
                                        'font-color': colors['purple'],
                                        'textAlign':'center',
                                        'width':'90px',
                                        'display':'inline-block',
                                        'margin':'0px 0px 10px 15px'
                                    }
                                ),

                                ],
                                style={
                                    'display':'flex',
                                    'border-bottom':'3px solid #6f42c1',
                                    'padding':'0px 0px 0px 45px',
                                    'width':'110%'
                                }
                        ),
                        ]
                    ),
                    dbc.Col(
                        [
                        html.Div(
                            children=[
                                html.P(
                                    "Strike:",
                                    style={
                                        'color':'#32fbe2',
                                        'display':'inline-block',
                                        'font-size':'20px'
                                    }
                                ),
                                dcc.Input(
                                    id="sel_strike",
                                    type="number",
                                    placeholder="Strike",
                                    value=410,
                                    style={
                                        'background-color': colors['font'],
                                        'font-color': colors['purple'],
                                        'textAlign':'center',
                                        'width':'70px',
                                        'display':'inline-block',
                                        'margin':'0px 0px 10px 15px'
                                    }
                                ),

                                ],
                                style={
                                    'display':'flex',
                                    'border-bottom':'3px solid #6f42c1',
                                    'padding':'0px 0px 0px 45px',
                                    'width':'110%'
                                }
                        ),
                        ]
                    ),
                    ]
                ),
                dbc.Row(
                    [
                    dbc.Col(
                        [
                        dcc.Graph(
                            id='vol_exp'
                        )
                        ]
                    ),
                    dbc.Col(
                        [
                        dcc.Graph(
                            id='vol_strike'
                        )
                        ]
                    ),
                    ]
                ),
                dbc.Row(
                    style={
                        'background-color':'#6f42c1',
                        'height':'300px',   
                        'width':'110%'
                    }
                ),
            ],
            style={
                'background-color':'#1a0933'
            }
        )
                
    
@callback(
    Output('vol_surface', 'figure'),
    Input('sel_asset1', 'value')
)

def update_fig_1(asset):
    fig = vs.plot_surface(asset)
    
    return fig

@callback(
    Output('asset_price', 'children'),
    Input('sel_asset1', 'value')
)

def update_price(asset):
    price = tick.get_price(asset)
    return "Current Underlying Price: {}".format(price)

@callback(
    Output('vol_exp', 'figure'),
    Input('sel_asset1', 'value'),
    Input('sel_exp', 'value')
)

def update_fig_2(asset, exp):
    fig = vs.plot_exp(asset, exp)
    
    return fig

@callback(
    Output('vol_strike', 'figure'),
    Input('sel_asset1', 'value'),
    Input('sel_strike', 'value')
)

def update_fig_3(asset, strike):
    fig = vs.plot_strike(asset, strike)
    
    return fig



if __name__ == '__main__':
    app.run(debug=False)