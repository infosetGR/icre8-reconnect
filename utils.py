import dash_html_components as html
import dash_core_components as dcc
import dash


external_stylesheets = [
    #'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://codepen.io/amyoshino/pen/jzXypZ.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

def Footer(app):
    return html.Div(
                    [
                        html.P('Developed by Fotis Stathopoulos - Infoset ', style = {'display': 'inline'}),
                        html.A('fotis@infoset.co', href = 'mailto:fotis@infoset.co')
                    ], className = "twelve columns",
                       style = {'fontSize': 12, 'padding-top': 20}
                )


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Button("Learn More", id="learn-more-button"),
                        href="http://www.icre8.eu/reconnect-interreg",

                    ),
                    html.Img(
                        src=app.get_asset_url("icre8-logo.png"),
                        className="logo",
                        style={
                            'height': '16%',
                            'width': '16%',
                            'float': 'right',
                            'position': 'relative',
                            'padding-top': 12,
                            'padding-right': 0
                        },
                    ),

                ],
            ),
            html.Div(
                [
                    html.Div(
                        [html.H2("RECONNECT (Interreg) ")], className='nine columns'

                    ),
                ],
                className="twelve columns",
                style={"padding-left": "100"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            html.A(
                html.Button("Overview"),
                href="/Overview"


            ),
           html.A(
               html.Button("Correlation Analysis"),
                href="/correlationanalysis"


            ),
           html.A(
               html.Button("Map Analysis"),
                href="/mapanalysis"

            ),
            html.A(
                html.Button("DSS scenarios")
                , href="/DSSscenarios"
            ),

        ],

    )
    return menu

def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
