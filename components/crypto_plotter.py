import plotly.graph_objs as go


class CryptoPlotter:
    def __init__(self, data):
        self.data = data

    def plot_area_chart(self, cryptos):
        fig = go.Figure()
        for crypto in cryptos:
            fig.add_trace(go.Scatter(
                x=self.data[crypto].index,
                y=self.data[crypto]['Close'],
                mode='lines',
                fill='tozeroy',
                name=crypto,
                opacity=0.5
            ))
        fig.update_layout(title="Cryptocurrency Price Over Time",
                          xaxis_title="Time", yaxis_title="Price")
        return fig

    def plot_volume_chart(self, cryptos):
        fig = go.Figure()
        for crypto in cryptos:
            fig.add_trace(go.Bar(
                x=self.data[crypto].index,
                y=self.data[crypto]['Volume'],
                name=crypto,
                opacity=0.6
            ))
        fig.update_layout(title="Cryptocurrency Volume Over Time",
                          xaxis_title="Time", yaxis_title="Volume")
        return fig
