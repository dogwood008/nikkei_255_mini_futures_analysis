import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly_candle_stick import PlotlyCandleStick


class Combined(PlotlyCandleStick):
    @staticmethod
    def graph_method(df, title=None, save_fig=False, filename=None, output_base_dir=None):
        '''
        https://stackoverflow.com/a/65997291/15983717
        '''
        # plotly = go.Figure(data=go.Candlestick(x=df.index, open=df.open, high=df.high, low=df.low, close=df.close))
        # Plot OHLC on 1st row
        plotly = make_subplots(shared_xaxes=True,  # rows=2, cols=1,
                               vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), specs=[[{"secondary_y": True}]])
        # row_width=[1.0, 1.0])
        plotly.add_trace(
            go.Candlestick(
                x=df.index, open=df.open, high=df.high, low=df.low, close=df.close, name='OHLC'
            ),  # , row=1, col=1)
            secondary_y=True
        )
        # Bar trace for volumes on 2nd row without legend
        plotly.add_trace(
            go.Bar(x=df.index, y=df.volume, showlegend=False),
            secondary_y=False
        )  # , row=2, col=1)
        # plotly.update(layout_xaxis_rangeslider_visible=True)
        if save_fig:
            plotly.update_layout(
                xaxis=dict(
                    rangeslider=dict(
                        visible=False
                    ),
                )
            )
            plotly.update_yaxes(type='log')
            plotly.layout.yaxis2.showgrid = False
            plotly.write_image(
                f'{output_base_dir}/figure_{filename}.pdf', engine="kaleido", scale=10)
            #plotly.write_image(f'./figure_{filename}.png', engine="kaleido", scale = 20)
            plotly.update_layout(  # https://qiita.com/Ringa_hyj/items/b13e3e721519c2842cc9
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1,
                                 label="1m",
                                 step="month",
                                 stepmode="backward"),
                            dict(count=6,
                                 label="6m",
                                 step="month",
                                 stepmode="backward"),
                            dict(count=1,
                                 label="YTD",
                                 step="year",
                                 stepmode="todate"),
                            dict(count=1,
                                 label="1y",
                                 step="year",
                                 stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(
                        visible=True
                    ),
                    type="date"
                )
            )
            save_html = False
            if save_html:
                plotly.write_html(f'{output_base_dir}/figure_{filename}.html')
            # https://zenn.dev/ganariya/articles/plotly-high-resolution
        else:
            plotly.show()
    # plotly_candlestick(convert_into_ohlcv(df.sort_index().loc['2022-08-01':'2022-08-07', :], '1min'))
