import io
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from .crypto_data_fetcher import CryptoDataFetcher
from .crypto_plotter import CryptoPlotter


class CryptoDashboard:
    def __init__(self, cryptos):
        self.app = Dash(__name__)
        self.cryptos = cryptos
        self.data_fetcher = CryptoDataFetcher(cryptos)
        self.layout()

    def layout(self):
        self.app.layout = html.Div([
            html.H1("Cryptocurrency Dashboard"),
            html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}, children=[
                dcc.Dropdown(
                    id='crypto-dropdown',
                    options=[{'label': crypto, 'value': crypto}
                             for crypto in self.cryptos],
                    value=[self.cryptos[0]],
                    multi=True,
                    style={'width': '90%', 'min-width': '300px',
                           'whiteSpace': 'normal'}
                ),
                dcc.Dropdown(
                    id='time-dropdown',
                    options=[
                        {'label': 'Last 6 months', 'value': '6mo'},
                        {'label': 'Last 3 months', 'value': '3mo'},
                        {'label': 'Last 1 month', 'value': '1mo'},
                        {'label': 'Last 5 days', 'value': '5d'},
                        {'label': 'Today', 'value': '24h'},
                    ],
                    value='6mo',
                    style={'width': '48%'}
                )
            ]),
            html.Div(style={'display': 'flex'}, children=[
                dcc.Graph(id='area-chart',
                          style={'width': '90%', 'min-width': '300px'}),
                dcc.Graph(id='volume-chart')  # Volume chart
            ]),
            html.H2("Latest Prices"),
            html.Div(id='price-table'),
            html.Button("Download Chart Data", id="btn-download"),
            dcc.Download(id="download-dataframe-xlsx")  # Download component
        ])

    def update_callbacks(self):
        @self.app.callback(
            [Output('area-chart', 'figure'),
             Output('volume-chart', 'figure'),  # New volume chart output
             Output('price-table', 'children')],
            [Input('crypto-dropdown', 'value'),
             Input('time-dropdown', 'value')]
        )
        def update_graph(selected_cryptos, selected_time):
            # Define period and interval based on selected time
            period_map = {
                '6mo': '6mo',
                '3mo': '3mo',
                '1mo': '1mo',
                '5d': '5d',
                '24h': '1d',
            }

            interval_map = {
                '6mo': '1d',
                '3mo': '1d',
                '1mo': '1d',
                '5d': '1d',
                '24h': '5m',
            }
            period = period_map[selected_time]
            interval = interval_map[selected_time]

            # update data
            self.data = self.data_fetcher.fetch_prices(
                period=period, interval=interval)

            # update plotter
            self.plotter = CryptoPlotter(self.data)
            area_chart = self.plotter.plot_area_chart(selected_cryptos)
            volume_chart = self.plotter.plot_volume_chart(selected_cryptos)

            # layout for latest prices
            price_rows = []
            for i, crypto in enumerate(selected_cryptos):
                last_row = self.data[crypto].iloc[-1]
                price = last_row['Close']
                change = price - self.data[crypto]['Close'].iloc[-2]
                timestamp = last_row.name.strftime("%m/%d/%Y - %H:%M:%S")

                if i % 2 == 0:
                    row = html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '10px'}, children=[
                        html.Div(children=[
                            html.P(f"{crypto}", style={'margin': '0'}),
                            html.P(f"${price:.2f}", style={'margin': '0'}),
                            html.P(f"{change:.2f}", style={'margin': '0'}),
                            html.P(f"{timestamp}", style={'margin': '0'}),
                        ], style={'padding': '10px'})
                    ])
                    price_rows.append(row)
                else:
                    price_rows[-1].children.append(
                        html.Div(children=[
                            html.P(f"{crypto}", style={'margin': '0'}),
                            html.P(f"${price:.2f}", style={'margin': '0'}),
                            html.P(f"{change:.2f}", style={'margin': '0'}),
                            html.P(f"{timestamp}", style={'margin': '0'}),
                        ], style={'padding': '10px'})
                    )

            prices_display = html.Div(
                style={'display': 'flex', 'flex-wrap': 'wrap'}, children=price_rows)

            return area_chart, volume_chart, prices_display

        @self.app.callback(
            Output("download-dataframe-xlsx", "data"),
            [Input("btn-download", "n_clicks")],
            prevent_initial_call=True,
        )
        def export_to_excel(n_clicks):
            if not hasattr(self, 'data'):
                return None

            # Create a BytesIO buffer for the Excel file
            output = io.BytesIO()

            # Write each crypto DataFrame to separate sheets
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for crypto, df in self.data.items():
                    # Remove timezone information for Excel compatibility
                    df.index = df.index.tz_convert(None)
                    df.to_excel(writer, sheet_name=crypto)

            # Set the position back to the beginning of the buffer
            output.seek(0)

            # Return the downloadable file
            return dcc.send_bytes(output.getvalue(), f"crypto_data {pd.Timestamp.now().strftime('%m-%d-%Y')}.xlsx")

    def run(self):
        self.update_callbacks()
        self.app.run_server(debug=True)
