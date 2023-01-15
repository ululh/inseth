# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
col_to_use = ["from", "to", "value", "type", "blockTimestamp"]
all_transactions = pd.read_parquet('../ethereum_collector/ethereum_transactions/', engine='pyarrow', columns=col_to_use)

#print(all_transactions.shape)
# sum of values
transac_total_value = all_transactions['value'].sum()

# number of transactions
num_of_transac = len(all_transactions.index)



fig1 = px.pie(all_transactions, values="value", names="type", title="value by type")

fig2 = px.bar(all_transactions, x="type", y="value", color="from", title="number of transactions by type")

app.layout = html.Div(children=[
    html.H1(children='Ethereum transactions'),

    html.Div(children=f'Number of transactions : {num_of_transac}'),

    html.Div(children=f'Total value : {transac_total_value}'),

    dcc.Graph(
        id='value by type',
        figure=fig1
    ),

    dcc.Graph(
        id='number of transactions by type',
        figure=fig2
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

