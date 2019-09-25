import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from IPython import display
import os


def show_app(app, port=9999,
             width=700,
             height=350,
             offline=False,
             in_binder=None):
    in_binder = 'JUPYTERHUB_SERVICE_PREFIX' in os.environ if in_binder is None else in_binder
    if in_binder:
        base_prefix = '{}proxy/{}/'.format(os.environ['JUPYTERHUB_SERVICE_PREFIX'], port)
        url = 'https://hub.mybinder.org{}'.format(base_prefix)
        app.config.requests_pathname_prefix = base_prefix
    else:
        url = 'http://localhost:%d' % port

    iframe = '<a href="{url}" target="_new">Open in new window</a><hr><iframe src="{url}" width={width} height={height}></iframe>'.format(
        url=url,
        width=width,
        height=height)

    display.display_html(iframe, raw=True)
    if offline:
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
    return app.run_server(debug=False)

app_simple = dash.Dash()

app_simple.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

show_app(app_simple)