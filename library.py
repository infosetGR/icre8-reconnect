import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")


fig = go.Figure()
print(df.Date)


fig.add_trace(go.Scatter(x=df.Date, y=df['AAPL.High'], name="AAPL High",
                         line_color='deepskyblue'))


fig.add_trace(go.Scatter(x=df.Date, y=df['AAPL.Low'], name="AAPL Low",
                         line_color='dimgray'))

fig.update_layout(title_text='Time Series with Rangeslider',
                  xaxis_rangeslider_visible=True)
#fig.show()