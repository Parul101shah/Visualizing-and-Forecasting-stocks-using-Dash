import dash
from dash import dcc
from dash import html
from datetime import datetime as dt
import yfinance as yf
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px #Plotly Express library to create line plot
from model import prediction

# Internal CSS
styles = {
    'container': {
        'background-color': '#F6F5C8',
    },
     'containerr': {
        'background-color': '#16A9CC',
    }
   
}
# Initializing the app(This creates new dash application)
app = dash.Dash(__name__)  


# html layout of site
# _________________________________________________________________________________________________________________________________________________________________________________________________
app.layout = html.Div(
    [
        html.Div(
        [
                # left Side
                html.P("Welcome to the Stock Dash App!", className="start",style={'display': 'flex','color': '#FCFCFC','text-align':'center', 'font-size': '30px','font-weight':'100%','font-family':'Sans-serif','padding':'43px'} ),
                html.Div([  #Input text
                    html.P("Input stock code: ",style={'color': '#FCFCFC','font-size':'18px','font-weight':'100%','font-family':'Sans-serif','padding':'1px','margin-left':'25px','display': 'flex'}),
                    html.Div([ #Actual Input field
                        # dcc is used to take input from dash
                        dcc.Input(id="dropdown_tickers", type="text",placeholder="Enter stock code...", style={'background-color': '#FEFEFF', 'color': 'grey','padding':'16px','margin-left':'20px'}),
                        html.Button("Submit", id='submit',style={'color':'#16A9CC','background-color': '#16A9CC','font-size': '16px','padding-bottom':'24px','padding-top':'11px','border-radius': '3px', 'cursor': 'pointer','margin-right':'7px'}),
                    ],
                            className="form")
                ],
                         className="input-place"),
                html.Div([#Data Range
                    dcc.DatePickerRange(id='my-date-picker-range',
                                        # Min date allowed is (year,month,date)(9-aug 1995)
                                        min_date_allowed=dt(1995, 8, 5),
                                        max_date_allowed=dt.now(), #Current date
                                        initial_visible_month=dt.now(),
                                        end_date=dt.now().date(),
                                        style={'margin-right':'1px'}),
                ],
                className="date"),
                html.Div([# Three buttons and an input field
                    html.Button("Stock Price", className="stock-btn", id="stock",style={'color':'#212024','background-color': '#FDCF4A','font-size': '15px','border': 'none','padding': '10px 20px', 'cursor': 'pointer','margin-left':'2px','border-radius': '4px'}),
                    html.Button("Indicators",className="indicators-btn",id="indicators",style={'color':'#212024','background-color': '#FDCF4A','font-size': '15px','border': 'none','padding': '10px 20px', 'cursor': 'pointer','border-radius': '4px'}),
                    dcc.Input(id="n_days",type="text",placeholder="Number of days...",style={'background-color': '#FEFEFF', 'color': 'grey','padding':'3px','margin-left':'1px'}),
                    html.Button("Forecast", className="forecast-btn", id="forecast",style={'color':'#212024','background-color': '#FDCF4A','font-size': '15px','border': 'none','padding': '10px 20px','padding-bottom': '17px', 'cursor': 'pointer','border-radius': '4px'})
                ],
                 className="buttons"),
            ],className="nav",style=styles['containerr']
        ),

        #Right Side
        html.Div(
        [
                html.Div(
                [  # header
                        html.Img(id="logo"),
                        html.P(id="ticker")
                ],
                className="header"),
                html.Div(id="description", className="decription_ticker"),
                html.Div([], id="graphs-content"),
                html.Div([], id="main-content"),
                html.Div([], id="forecast-content")
        ],
        className="content"
        ),
    ],
    className="container", style=styles['container']
    )
# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________

# callback for company info
@app.callback([
    Output("description", "children"),
    Output("logo", "src"),
    Output("ticker", "children"),
   
], [Input("submit", "n_clicks")], [State("dropdown_tickers", "value")]) #State represents the current value of the input
def update_data(n, val  ):
    if n is None:
         return (
            html.Div([
                html.P("HELLO !! , THIS IS STOCK VISUALIZING AND FORECASTING APPLICATION ", style={'margin': '10px','color':'#DE0406','font-size': '23px','font-weight':'100%','font-family':'Sans-serif','display': 'flex'}),
                html.P("Please enter a legitimate stock code to get details.", style={'margin': '5px','font-size': '20px','font-weight':'100%','font-family':'Sans-serif','display': 'flex'}),
                html.P("Press STOCK PRICE to get closing and opening prices of a stock over time.", style={'margin': '5px','font-size': '20px','font-weight':'100%','font-family':'Sans-serif','display': 'flex'}),
                html.P("Press INDICATORS to get Exponential Moving Average (EMA) indicator for the stock's closing price.", style={'margin': '5px','font-size': '20px','font-weight':'100%','font-family':'Sans-serif','display': 'flex'}),
                html.P("Press FORECAST to get forecasted stock prices based on a specified number of days.", style={'margin': '5px','font-size': '20px','font-weight':'100%','font-family':'Sans-serif','display': 'flex'})
            ]),
            "https://cdn.pixabay.com/photo/2018/04/19/19/40/stocks-3334074_1280.jpg",
            "STOCK APP"
        )

# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________

def get_stock_price_fig(df):
                #x-coordinate   y-coordinate
    fig = px.line(df,x="Date", y=["Close", "Open"],title="Closing and Openning Price vs Date")
    return fig


# callback for stocks graphs 
@app.callback([
    Output("graphs-content", "children"),
], [
    Input("stock", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("dropdown_tickers", "value")])
def stock_price(n,start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate  #special exception that can be raised in a Dash callback function callback function stops executing, and the current state of the output components remains unchanged.
    else:
        if start_date != None:
            # Yahoo Finance retrieve stock price data for a specified stock code (val) and date range.
            df = yf.download(val, str(start_date), str(end_date))
        else:
            df = yf.download(val) #It fetches the entire available historical data for the stock.
    # the index of the DataFrame is reset to the default sequential integer index.
    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]

# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________
def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,x="Date", y="EWA_20", title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines+markers')
    return fig


# callback for indicators
@app.callback([Output("main-content", "children")], [
    Input("indicators", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("dropdown_tickers", "value")])
def indicators(n, start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        return [""]

    if start_date == None:
        df_more = yf.download(val)
    else:
        df_more = yf.download(val, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)]
# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________

# callback for forecast
@app.callback([Output("forecast-content", "children")],
              [Input("forecast", "n_clicks")],
              [State("n_days", "value"),
               State("dropdown_tickers", "value")])
def forecast(n, n_days, val):
    if n== 0:
        return ("Invalid must be greater than 0")
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate
    fig = prediction(val, int(n_days)+1)
    return [dcc.Graph(figure=fig)]

# run a Dash application
if __name__ == '__main__':
    app.run_server(debug=True)  

