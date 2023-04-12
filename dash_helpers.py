import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, register_page, get_asset_url
from dash_bootstrap_templates import load_figure_template

def proj_buttons2(href1, href2):
    button_container = html.Div(
                            children=[
                                html.A(
                                    html.Button(
                                            "Overview",
                                            style={
                                                'color':'white',
                                                'font-size':'20px',
                                                'background-color':'#666600',
                                            },
                                    ),
                                    href=href1,
                                    style={
                                        'padding':'0px 15px 0px 0px',
                                        'textAlign':'center'
                                    }
                                ),
                                html.A(
                                    html.Button(
                                            "Code",
                                            style={
                                                'color':'white',
                                                'font-size':'20px',
                                                'background-color':'#666600',
                                            },
                                    ),
                                    href=href2,
                                    style={
                                        'padding':'0px 0px 0px 15px',
                                        'textAlign':'center'
                                    }
                                ),
                            ],
                            style={
                                'padding':'0px 0px 10px 0px',
                                'textAlign':'center'
                            }
                        )
    return button_container


def proj_buttons3(href1, href2, href3, button3='Dashboard'):
    button_container = html.Div(
                            children=[
                                html.A(
                                    html.Button(
                                            "Overview",
                                            style={
                                                'color':'white',
                                                'font-size':'20px',
                                                'background-color':'#666600',
                                            },
                                    ),
                                    href=href1,
                                    style={
                                        'padding':'0px 15px 0px 0px',
                                        'textAlign':'center'
                                    }
                                ),
                                html.A(
                                    html.Button(
                                            "Code",
                                            style={
                                                'color':'white',
                                                'font-size':'20px',
                                                'background-color':'#666600',
                                            },
                                    ),
                                    href=href2,
                                    style={
                                        'padding':'0px 15px 0px 15px',
                                        'textAlign':'center'
                                    }
                                ),
                                html.A(
                                    html.Button(
                                            button3,
                                            style={
                                                'color':'white',
                                                'font-size':'20px',
                                                'background-color':'#666600',
                                            },
                                    ),
                                    href=href3,
                                    style={
                                        'padding':'0px 0px 0px 15px',
                                        'textAlign':'center'
                                    }
                                ),
                            ],
                            style={
                                'padding':'0px 0px 10px 0px',
                                'textAlign':'center'
                            }
                        )
    return button_container


def proj_image(src, height='75%', width='75%'):
    image_container = html.Div(
                children=[
                    html.Img(
                        src=r'assets/{}'.format(src),
                        style={
                            'padding':'3px',
                            'height':height,
                            'width':width,
                            'border':'2px solid burlywood',
                            'margin':'0px 0px 5px 0px'
                                        }

                                    ),
                            
                                ]
                            
                            
                            )
    return image_container

def Navbar():
    layout = html.Div(
        [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(
                    dbc.NavLink(
                        "HOME",
                        href="/",
                        style={
                            'color':'white',
                            'font-size': '22px',
                            'font-family': 'Montserrat, Helvetica, Arial, sans-serif',
                            'font-weight':'bold'
                
                        }
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "PORTFOLIO",
                        href="/portfolio",
                        style={
                            'color':'white',
                            'font-size': '22px',
                            'font-family': 'Montserrat, Helvetica, Arial, sans-serif',
                            'font-weight':'bold'
                        }
                    )
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "ABOUT",
                        href="/about",
                        style={
                            'color':'white',
                            'font-size':'22px',
                            'font-family': 'Montserrat, Helvetica, Arial, sans-serif',
                            'font-weight':'bold'

                        }
                    )
                )
                    
            ],
            brand="DYLAN JORLING, CFA",
            color="#004640",
            brand_style={
                    'color': 'white',
                    'font-size': '45px',
                    'font-family': 'Montserrat, Helvetica, Arial, sans-serif',
                    'font-weight': 'bold',
                    'letter-spacing': '-2px',
                    'padding':'0px'
            },
            style={
                'border-top':'3px solid #ae5000',
                'padding':'0px',
                'margin':'0px'
                },

        ),
        
        dbc.Row(
            [
            dbc.Col(
                html.H2(
                    '',
                    style={
                        'color': 'linen',
                        'font-size':'12px'
                    }
                ),
                style={
                    'background-color':'#004640',
                    'border-bottom': '3px solid #ae5000',
                    'textAlign':'center',
                    'width':'33%'
                }
            ),
            dbc.Col(
                html.H2(
                    'QUANT FINANCE | STATISTICAL ANALYSIS | DATA SCIENCE',
                    style={
                        'color': 'linen',
                        'font-size':'12px'
                    }
                ),
                style={
                    'background-color':'#004640',
                    'border-bottom': '3px solid #ae5000',
                    'textAlign':'center',
                    'width':'34%'
                }
            ),
            dbc.Col(
                children=[
                    html.A(
                        "RESUMÉ",
                        href="/assets/resume.pdf",
                        style={
                            'color': 'linen',
                            'font-size':'12px',
                            'padding':'0px 5px 0px 0px'
                        }
                    ),

                    html.A(
                        "CONTACT",
                        href="/contact",
                        style={
                            'color': 'linen',
                            'font-size':'12px',
                            'padding':'0px 0px 0px 5px'
                        }
                    ),
                ],
                style={
                    'background-color':'#004640',
                    'border-bottom': '3px solid #ae5000',
                    'font-color': 'linen',
                    'textAlign':'center',
                    'padding':'0px 0px 0px 0px',
                    'width':'33%'
                }
                
            ),
        ],
        style={
            'textAlign':'center'
        }
    ),

    ],
)

    return layout

def page_top():
    top = dbc.Row(
            [
            Navbar()
            ]
        )
    return top

def page_bottom(col1='#666600', col2='#ae5000', col3='white'):
    bottom = dbc.Stack(
                [
                dbc.Col(
                    children=[
                        html.A(
                            href="https://www.linkedin.com/in/dylan-jorling-cfa-75729045/",
                            children=[
                                html.Img(
                                    src=r'assets/li.png',
                                    alt="Link to my LinkedIn",
                                    style={
                                        'color': 'white',
                                        'margin':'5px 5px 3px 0px',
                                        'height':'50px'
                                    }
                                )
                            ]
                        ),
                        html.A(
                            href="https://github.com/dkjorling",
                            children=[
                                html.Img(
                                    src=r'assets/gh.png',
                                    alt="Link to my GitHub",
                                    style={
                                        'color': 'white',
                                        'padding':'5px 0px 3px 5px',
                                        'height':'50px'
                                    }
                                ),
                            ]
                        )
                    ],
                    style={
                        'background-color':col1,
                        'textAlign':'center',
                    }
                ),
                dbc.Col(
                    html.H5(
                        'Copyright © 2023 | Dylan Jorling',
                        style={
                            'color': col3,
                            'padding':'0px 0px',
                            'font-size':'12px',
                        }
                    ),
                    style={
                    'background-color':col1,
                    'textAlign':'center',
                    }
                ),
                ],
                style={
                    'background-color':col1,
                    'textAlign':'center',
                    'position':'fixed',
                    'bottom':'0',
                    'width':'100%',
                    'border-top':'3px solid {}'.format(col2)
                },
            )
    return bottom



def dashboard_navbar(name, col1, col2, col3):
    navbar = html.Div(
                [
                dbc.Row(
                    dbc.Col(
                        children=[
                            
                            html.A(
                                "Documentation",
                                href="/{}/dashboard/documentation".format(name),
                                style={
                                    'padding':'0px 5px 0px 0px',
                                    'color':col2
                                }
                            ),

                            html.A(
                                "Overview",
                                href="/{}".format(name),
                                style={
                                    'padding':'0px 5px 0px 5px',
                                    'color':col2
                                }
                            ),

                            html.A(
                                "Portfolio",
                                href="/portfolio",
                                style={
                                    'padding':'0px 0px 0px 5px',
                                    'color':col2
                                }
                            ),
                        ],
                        style={
                            'background-color':col1,
                            'border-bottom': '3px solid {}'.format(col3),
                            'font-color': col2,
                            'font-size':'18px',
                            'textAlign':'right',
                            'margin':'0px 30px 0px 0px',
                            'font-family': 'Montserrat, Helvetica, Arial, sans-serif',
                            'font-weight':'bold',
                            
                        }
                    ),
                )
                ]
            )

    return navbar

def dashboard_navbar2(name, col1, col2, col3):
    navbar = html.Div(
                [
                dbc.Row(
                    dbc.Col(
                        children=[
                            
                            html.A(
                                "Dashboard",
                                href="/{}/dashboard".format(name),
                                style={
                                    'padding':'0px 5px 0px 0px',
                                    'color':col2
                                }
                            ),

                            html.A(
                                "Overview",
                                href="/{}".format(name),
                                style={
                                    'padding':'0px 5px 0px 5px',
                                    'color':col2
                                }
                            ),

                            html.A(
                                "Portfolio",
                                href="/portfolio",
                                style={
                                    'padding':'0px 0px 0px 5px',
                                    'color':col2
                                }
                            ),
                        ],
                        style={
                            'background-color':col1,
                            'border-bottom': '3px solid {}'.format(col3),
                            'font-color': col2,
                            'font-size':'18px',
                            'textAlign':'right',
                            'margin':'0px 30px 0px 0px',
                            'font-family': 'Montserrat, Helvetica, Arial, sans-serif',
                            'font-weight':'bold',
                            
                        }
                    ),
                )
                ]
            )

    return navbar

