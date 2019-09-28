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

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Location of Study:'),
                        dcc.Checklist(
                                id = 'Country',
                                options=[
                                    {'label': 'Cyprus', 'value': 'CY'},
                                    {'label': 'Greece', 'value': 'GR'},
                                    {'label': 'Bulgaria', 'value': 'BU'},
                                    {'label': 'Albania', 'value': 'AL'},
                                ],
                                value=['CY', 'GR', "BU",  'AL'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),

            ],
            className='row'
        ),

    ], className='ten columns offset-by-one'))
])
