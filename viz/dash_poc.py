# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

#app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = Dash(__name__)

col_to_use = ["from", "to", "value", "type", "blockTimestamp"]
all_transactions = pd.read_parquet('../ethereum_collector/ethereum_transactions/', engine='pyarrow', columns=col_to_use)

'''
all_transactions = pd.DataFrame({
    "from": ["toto", "ulul", "ulul", "titi", "toto", "toto"],
    "value": [4, 1, 2, 2, 4, 5],
    "type": ["0x1", "0x1", "0x0", "0x0", "0x2", "0x2"],
    "blockTimestamp": ["2022-11-28 08:05:00", "2022-11-28 09:15:00", "2022-11-29 18:46:09", "2022-11-27 22:55:20", "2022-11-28 09:35:43", "2022-11-29 08:05:00"]
})

'''
#print(all_transactions.shape)
# sum of values
transac_total_value = all_transactions['value'].sum()

# number of transactions
num_of_transac = len(all_transactions.index)



fig1 = px.pie(all_transactions, values="value", names="type", title="value by type")

fig2 = px.bar(all_transactions, x="type", y="value", title="number of transactions by type")

fig3 = px.histogram(all_transactions, x="blockTimestamp", title="transactions per day")

app.layout = html.Div(children=[
    html.H1(children='Ethereum transactions POC'),

    html.Div(children=f'Number of transactions : {num_of_transac}'),

    html.Div(children=f'Total value : {transac_total_value}'),

    dcc.Graph(
        id='value by type',
        figure=fig1
    ),

    dcc.Graph(
        id='number of transactions by type',
        figure=fig2
    ),

    dcc.Graph(
        id='transactions by day',
        figure=fig3
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

