import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import Header, make_dash_table,app

from IPython import display
import os



layout= html.Div([ html.Div(
    html.Div([
        html.Div(
            [
                Header(app),

            ], className="row"
        ),



    ], className='ten columns offset-by-one'))
])
