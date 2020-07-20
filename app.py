import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from Asian_Option_CRR_GRW_V4 import *
from descriptions import list_input
import base64


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML', "./assets/mathjax.js"])
server = app.server

bg_color="#506784",
font_color="#F3F6FA"


email = "michelvanderhulst@student.uclouvain.be"

graph_stock_simul = ''' #### Stock simulation (GRW) '''
graph_port_details_text = ''' #### Portfolio before/after rebalancing'''
graph_nbr_shares = ''' #### Shares held before/after rebalancing'''
graph_cash = ''' #### Cash account before/after rebalancing'''
graph_option_price = ''' #### Option price'''
graph_option_intrinsic = ''' #### Option intrinsic value'''


def header():
    return html.Div(
                id='app-page-header',
                children=[#html.Div(html.A(
                      #            id='lsm-logo', 
                      #            children=[html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open("output-onlinepngtools (1).png", 'rb').read()).decode()))],
                      #            href="https://uclouvain.be/en/faculties/lsm",
                      #            target="_blank", #open link in new tab
                      #            style={'margin':'20px'}
                      #              ), style={"display":"inline-block"}),
                    #
                    #
                    # html.Div(
                       #  html.A(
                       #    id="nova-logo", 
                       #    children=[html.Img(src="data:image/png;base64,{}".format(base64.b64encode(open("output-onlinepngtools (2).png",'rb').read()).decode()))],
                       #    href="https://www2.novasbe.unl.pt/en/",
                       #    style={"margin":"-45px"}
                       #      ), style={"display":"inline-block"}),
                    #
                    #
                    html.Div(children=[html.H3("Asian option replication strategy app"),
                                       html.H4("Cox-Ross-Rubinstein model")
                                      ],
                             style={"display":"inline-block", "font-family":'sans-serif'}),
                    #
					html.Div(children=[dbc.Button("References", id="popover-references", outline=True, style={"color":"white", 'border': 'solid 1px white'}),
                                       dbc.Popover(children=[dbc.PopoverHeader("References"),
                                                             dbc.PopoverBody(["Academical references: ", 
                                                             				  html.Br(),  
                                                             				  "- Vrins, F. (2020). Lecture notes of the course Derivatives Pricing. Louvain School of Management",
                                                             				  html.Br(),
                                                             				  "- Shreve, S. (2004). Stochastic Calculus for Finance I: The Binomial Asset Pricing Model (Springer Finance)",
                                                             				  html.Br(),
                                                             				  "- Yuxing, Y. (2017). Python for Finance (2nd edition).",
                                                                              html.Hr(), 
                                                                              "Web app reference:",
                                                                              html.Br(),
                                                                              "- Rankin, Z. (2019). A gentle intro to Dash development, accessed online at https://towardsdatascience.com/a-gentle-introduction-to-dash-development-and-deployment-f8b91990d3bd",
                                                                              ]),],
                                                   id="popover-ref",
                                                   is_open=False,
                                                   target="popover-references"),
                                       ],
                              style={"display":"inline-block", "font-family":"sans-serif", 'marginLeft': '55%'}),
					#
					#
                    html.Div(children=[dbc.Button("About", id="popover-target", outline=True, style={"color":"white", 'border': 'solid 1px white'}),
                                       dbc.Popover(children=[dbc.PopoverHeader("About"),
                                                             dbc.PopoverBody(["Michel Vanderhulst",                             
                                                                              f"\n {email}", 
                                                                              html.Hr(), 
                                                                              "This app was built for my Master's Thesis, under the supervision of Prof. Frédéric Vrins (frederic.vrins@uclouvain.be)."]),],
                                                   id="popover",
                                                   is_open=False,
                                                   target="popover-target"),
                                       ],
                              style={"display":"inline-block", "font-family":"sans-serif", "padding":5 }),
                         ],
                style={
                    'background': bg_color,
                    'color': font_color,
                    'padding':20,
                    'margin':'-10px',
                }
            )



def body():
    return html.Div(children=[
            html.Div(id='left-column', children=[
                dcc.Tabs(
                    id='tabs', value='The app',
                    children=[
                        dcc.Tab(
                            label='The app',
                            value='The app',
                            children=html.Div(children=[
                                html.Br(),
                                html.H4('What is this app?', style={"text-align":"center"}),
                                html.P(
                                    """
                                    This app computes the replication strategy of Asian options on a set of given, comparing the Cox-Ross-Rubinstein model and strategy option price.
                                    """
                                ),
                                html.P(
                                    """
                                    The goal is to showcase that the price is truly arbitrage-free, i.e. that both risk-neutral pricing and replicating strategy have the same values. 
                                    """
                                ),
                                html.P(
                                    """
                                    Read more about options : 
                                    https://en.wikipedia.org/wiki/Option_(finance)
                                    
                                    """
                                ),
                            ])
                        ),
                        dcc.Tab(
                            label="Model",
                            value="Model",
                            children=[html.Div(children=[
                                html.Br(),
                                html.H4("The Cox-Ross-Rubinstein model", style={"text-align":"center"}),
                                html.P([
                                    """
                                    The Cox-Ross-Rubinstein model (CRR) is an example of a multi-period market model of the stock price.                                     
                                    """]),
                                html.Hr(),
                                html.H4("Model assumptions", style={"text-align":"center"}),
                                "Its main assumptions are:",
                                html.Ul([html.Li("Does not consider dividends and transaction costs"), 
                                         html.Li("The volatility and risk-free rate are assumed constant"),
                                         html.Li("Fraction of shares can be traded"),
                                         html.Li("The underlying asset can only either go 'up' by a fixed factor \(u<1\) or 'down' by \(0<d<1\)."),
                                         html.Li("The log-returns are independent at all periods")]),
                                html.Hr(),
                                html.H4("Underlying asset dynamics", style={"text-align":"center"}),
                                html.P([
                                    """Under CRR, the underlying asset follows a geometric random walk with 
                                    drift \(\mu\delta\) and volatility \(\sigma\sqrt{\delta}\). The probability to go 'up' and 'down' are respectively \(p\) and \(1-p\) (under \(\mathcal{P}\)).
                                    The stock price at period \(i\) can be modeled as a function of a binomial random variable, and the constant 'up' and 'down' factors
                                    computed: $$u=e^{\mu\delta+\sigma\sqrt{\delta}}$$ $$d=e^{\mu\delta-\sigma\sqrt{\delta}}$$. The \(\mathcal{Q}\)-probability allowing the discounted
                                    stock price to be a martingale amounts to the \(p\) value (under \(\mathcal{Q}\)) that leads to the martingale property: \(p=\\frac{e^{r}-d}{u-d}\).
                                    """])
                                ])]),
                        #
                        #
                        dcc.Tab(
                            label="Approach",
                            value="Methodology",
                            children=[html.Div(children=[
                                html.Br(),
                                html.H4("Methodology followed", style={"text-align":"center"}),
                                html.P([
                                    """
                                    To prove that the risk-neutral price is arbitrage-free, let us try to perfectly replicate it with a strategy. If the strategy is successfull, then 
                                    the price is unique and therefore arbitrage-free. For an Asian option, we will also denote with \(s_0\) the stock price at time 0 and \(Y_n=\sum_{k=0}^{n}s_k\) the sum of the 
                                    stock prices between times zero and n. From there, the payoff at time 3 will be \((\\frac{1}{4}Y_{3}-K)^+\) with strike K. Then, let \(V_n(s,y)\) be the price of
                                    the Asian option at node n if \(s_n=s\) and \(Y_n=y\).
                                    """]),
                                html.Hr(),
                                html.H4("Risk-neutral pricing", style={"text-align":"center"}),
                                html.P([
                                    """
                                    With the CRR, the stock tree and the option intrinsic value are easily computed at all nodes. Under the pricing measure, the option
                                    price of a node is simply the discounted value of the two children nodes. The price tree is therefore filled backwards,
                                    starting from the leaves (i.e. the payoff). 
                                    """]),
                                html.H4("Replicating portfolio", style={"text-align":"center"}),
                                html.P([
                                    """
                                    Then, if the price computed is truly arbitrage-free, a replication strategy can be based on this price: \(\pi_{0} = V_{0}(s,y)\).
                                     At each period, the number of shares to hold is given by \(\Delta_{n}(s,y) = \\frac{V_{n+1}(us, y + us)-V_{n+1}(ds, y + ds)}{(u-d)s}\). 
                                     The initial amount of cash will be \(c_{0} = \pi_{0} - \Delta_{0}(s,y)s_{0}\). At each node, a portfolio rebalancing is needed to ensure that the portfolio value is 
                                     equal to the option price. Before the rebalancing, \(\Delta\) is the same from node to node, the cash account grew at 
                                     the risk-free rate \(c_{n}=c_{n-1}e^{r}\), and the portfolio is the sum of both equity and cash positions \(\pi_{n} = c_{n}+\Delta_{n}(s,y)s_{n}\). 
                                     The rebalancing is done by updating the shares to hold \(\Delta_{n}(s,y) = \\frac{V_{n+1}(us, y + us)-V_{n+1}(ds, y + ds)}{(u-d)s}\) and ensuring that the value
                                      of the strategy before and after the rebalancing is the same \(c_{n}=\pi_{n}-(\Delta_{n-1}-\Delta_{n})s_{n}\). The tree is computed forward, 
                                      and will at all times replicate with option price. At the end of it we obtain the option payoff.
                                    """]),
                                ])]),
                        #
                        #
                        dcc.Tab(
                            label='Input',
                            value='Input',
                            children=html.Div(children=[
                                                html.Br(),
                                                #
                                                html.P(
                                                    """
                                                    Hover your mouse over any input to get its definition.                           
                                                    """
                                                ),
                                                dcc.Dropdown(
                                                    id='CallOrPut',
                                                    options=[{'label':'Asian Call option', 'value':"Call"},
                                                             {'label':'Asian Put option', 'value':"Put"}],
                                                    value='Call'),
                                                #
                                                html.Br(),
                                                #
                                                html.Div(children=[html.Label('Spot price', title=list_input["Spot price"], style={'font-weight': 'bold', "text-align":"center", "width":"25%",'display': 'inline-block'} ),
                                                                   dcc.Input(id="S", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                                                   html.Label("Strike", title=list_input["Strike"], style={'font-weight': 'bold',"text-align":"center", "width":"25%",'display': 'inline-block'} ),
                                                                   dcc.Input(id="K", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                                                  ],),                     
                                                #
                                                html.Div(children=[html.Label("Drift", title=list_input["Drift"], style={'font-weight': 'bold', 'display': 'inline-block'}),
                                                                   html.Label(id="drift", style={'display': 'inline-block'}),
                                                                  ]),
                                                #
                                                dcc.Slider(id='mu', min=-0.30, max=0.30, value=0.10, step=0.01, marks={-0.30: '-30%', 0.30: '30%'}),
                                                #
                                                html.Div([html.Label('Volatility', title=list_input["Volatility"], style={'font-weight': 'bold', "display":"inline-block"}),
                                                          html.Label(id="sigma", style={"display":"inline-block"}),]),  
                                                #
                                                dcc.Slider(id='vol', min=0, max=1, step=0.01, value=0.20, marks={0:"0%", 1:"100%"}),
                                                #
                                                html.Div([html.Label('Risk-free rate', title=list_input["Risk-free rate"], style={'font-weight': 'bold', "display":"inline-block"}),
                                                          html.Label(id="riskfree", style={"display":"inline-block"}),]),  
                                                dcc.Slider(id='Rf', min=0, max=0.1, step=0.01, value=0.05, marks={0:"0%", 0.1:"10%"}),
                                                #
                                                html.Div([html.Label('Maturity', title=list_input["Maturity"], style={'font-weight':'bold', "display":"inline-block"}),
                                                          html.Label(id="matu", style={"display":"inline-block"}),]),                                        
                                                dcc.Slider(id='T', min=0.25, max=5, 
                                                           marks={0.25:"3 months", 5:"5 years"}, step=0.25, value=3),
                                                #
                                                html.Br(),
                                                html.Div(children=[html.Label('Tree periods', title=list_input["Tree periods"], style={'font-weight': 'bold', "text-align":"center", "width":"25%",'display': 'inline-block'} ),
                                                                   dcc.Input(id="tree_periods", value=3, type='number', style={"width":"16%", 'display': 'inline-block'}),
                                                                  ],),
                                                ])),
        ],),], style={'float': 'left', 'width': '25%', 'margin':"30px"}),
    ])



def graphs():
    return html.Div(id='right-column', 
                    children=[
                        html.Br(),
                        html.Div([
                            html.Div(children=[dcc.Markdown(children=graph_option_intrinsic),
                                               dcc.Graph(id='option_intrinsic'),],
                                     style={"float":"right", "width":"45%", "display":"inline-block"}),
                            html.Div(children=[dcc.Markdown(children=graph_stock_simul),
                                               dcc.Graph(id='stock_simul'),],
                                     style={"float":"right", "width":"55%", "display":"inline-block"}),
                                ]),
                        html.Div([
                            html.Div(children=[dcc.Markdown(children=graph_option_price),
                                               dcc.Graph(id='option_price'),],
                                     style={"float":"right", "width":"45%", "display":"inline-block"}),
                            html.Div(children=[dcc.Markdown(children=graph_port_details_text),
                                               dcc.Graph(id='port_details'),],
                                     style={"float":"right", "width":"55%", "display":"inline-block"}),
                                ]),
                        html.Div([
                            html.Div(children=[dcc.Markdown(children=graph_cash),
                                               dcc.Graph(id='cash_acc'),],
                                     style={"float":"right", "width":"45%", "display":"inline-block"}),
                            html.Div(children=[dcc.Markdown(children=graph_nbr_shares),
                                               dcc.Graph(id='nbr_shares'),],
                                     style={"float":"right", "width":"55%", "display":"inline-block"}),
                                ]),


                             ], 
                    style={'float': 'right', 'width': '70%'})



app.layout = html.Div(
                id='main_page',
                children=[
                    dcc.Store(id='memory-output'),
                    header(),
                    body(),
                    graphs(),
                         ],
                     )


@app.callback(
	Output('memory-output', 'data'),
	[Input('CallOrPut', 'value'),
     Input("S","value"),
     Input("K", "value"),
     Input("Rf", "value"),
     Input("T","value"),
     Input("mu","value"),
     Input("vol", "value"),
     Input("tree_periods", "value"),])
def get_rep_strat_data(CallOrPut, S, K, Rf,T,mu,vol,tree_periods):
	nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = RepStrat_Asian_Option_CRR_GRW_V4(CallOrPut, S, K, Rf, T, mu, vol, tree_periods)
																
	return nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown

@app.callback(
    Output('stock_simul', 'figure'),
    [Input('memory-output', 'data'),])
def graph_stock_simul(data):
	nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

	return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        #margin={"t":15},
        margin=dict(
                l=0,
                #r=50,
                #b=100,
                t=15,
                #pad=4
            ),
        # showlegend=False,
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        legend=dict(
            x=0,
            y=0.8,
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)'),
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            showlegend=False,
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=stocksLabel,
	        	showlegend=False,
	        	hoverinfo='none',
	        	),
	        go.Scatter(
	        	x=[None],
	        	y=[None],
	        	mode='markers',
	        	name=f'Up factor: {u}'
	        	),
	     	go.Scatter(
	        	x=[None],
	        	y=[None],
	        	mode='markers',
	        	name=f'Down factor: {d}'
	        	),
	     	go.Scatter(
	        	x=[None],
	        	y=[None],
	        	mode='markers',
	        	name=f'Prob up: {probUp}'
	        	),
	     	go.Scatter(
	        	x=[None],
	        	y=[None],
	        	mode='markers',
	        	name=f'Prob down: {probDown}'
	        	),
	    ],
}


@app.callback(
    Output('port_details', 'figure'),
    [Input('memory-output', 'data'),])
def graph_portf_details(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin=dict(
                l=0,
                #r=50,
                #b=100,
                t=15,
                #pad=4
            ),
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=portfolioLabel,
	        	hoverinfo='none',
	        	),
	    ],
}


@app.callback(
    Output('nbr_shares', 'figure'),
    [Input('memory-output', 'data'),])
def graph_nbr_of_shares(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data

		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin=dict(
                l=0,
                #r=50,
                #b=100,
                t=15,
                #pad=4
            ),        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
				),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=nbrofsharesLabel,
	        	hoverinfo='none',
	        	),
	    ],
}

@app.callback(
    Output('cash_acc', 'figure'),
    [Input('memory-output', 'data'),])
def graph_cash_account(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin=dict(
                l=0,
                #r=50,
                #b=100,
                t=15,
                #pad=4
            ),
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=cashLabel,
	        	hoverinfo='none',
	        	),
	    ],
}

@app.callback(
    Output('option_price', 'figure'),
    [Input('memory-output', 'data'),])
def graph_option_pricee(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin=dict(
                l=0,
                #r=50,
                #b=100,
                t=15,
                #pad=4
            ),
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=optionpriceLabel,
	        	hoverinfo='none',
	        	),
	    ],
}

@app.callback(
    Output('option_intrinsic', 'figure'),
    [Input('memory-output', 'data'),])
def graph_option_pricee(data):
		nbrofsharesLabel, cashLabel, portfolioLabel, optionpriceLabel, intrinsicLabel, stocksLabel, edge_x, edge_y, node_x, node_y, u, d, probUp, probDown = data
		return{
       'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        showlegend=False,
        margin=dict(
                l=0,
                #r=50,
                #b=100,
                t=15,
                #pad=4
            ),
        xaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,},  # numbers below}
        yaxis={'showgrid': False, # thin lines in the background
    		   'zeroline': False, # thick line at x=0
               'visible': False,}  # numbers below}
    ),
    	'data': [
	        go.Scatter(
	            x=edge_x,
	            y=edge_y,
	            mode='lines',
	            line=dict(width=0.5),
	            hoverinfo='none',
	            ),
	        go.Scatter(
	        	x=node_x,
	        	y=node_y,
	        	mode='markers+text',
	        	marker=dict(size=40),
	        	text=intrinsicLabel,
	        	hoverinfo='none',
	        	),
	    ],
}

@app.callback(Output('drift', 'children'),
              [Input('mu', 'value')])
def display_value(value):
    return f': {int(value*100)}%'

@app.callback(Output('sigma', 'children'),
              [Input('vol', 'value')])
def display_value2(value):
    return f': {int(value*100)}%'

@app.callback(Output('riskfree', 'children'),
              [Input('Rf', 'value')])
def display_value3(value):
    return f': {int(value*100)}%'

@app.callback(Output('matu', 'children'),
              [Input('T', 'value')])
def display_value4(value):
    if value==0.25 or value==0.5 or value==0.75:
        return f": {int(value*12)} months"
    elif value == 1:
        return f': {value} year'
    else:
        return f': {value} years'

@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("popover-ref", "is_open"),
    [Input("popover-references", "n_clicks")],
    [State("popover-ref", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)