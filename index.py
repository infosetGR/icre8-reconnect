import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output




from utils import app
import mapanalysis
import correlationanalysis
import overview
import LoadData


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/DSSscenarios':
        return mapanalysis.layout
    elif pathname == '/correlationanalysis':
        return correlationanalysis.layout
    elif pathname == '/LoadData':
        return LoadData.layout
    else:
        return overview.layout

if __name__ == '__main__':
    app.run_server(debug=True)