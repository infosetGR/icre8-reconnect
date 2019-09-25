import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import matplotlib.pyplot as plt

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    dcc.Slider(
        id='n_points',
        min=10,
        max=100,
        step=1,
        value=50,
    ),

    dcc.Graph(id='example')  # or something other than Graph?...
])


@app.callback(
    dash.dependencies.Output('example', 'figure'),
    [dash.dependencies.Input('n_points', 'value')]
)
def update_figure(n_points):
    # create some matplotlib graph
    x = np.random.rand(n_points)
    y = np.random.rand(n_points)
    plt.scatter(x, y)
    # plt.show()
    return None  # return what, I don't know exactly, `plt`?


if __name__ == '__main__':
    app.run_server(debug=True)