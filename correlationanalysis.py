import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import html5lib
from utils import Header, make_dash_table,readWorldDataUrl, app


dfx=None
dfy=None
#df = pd.read_csv(
    #'https://gist.githubusercontent.com/chriddyp/'
    #'cb5392c35661370d95f300086accea51/raw/'
    #'8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
 #   'indicators.csv')

Indicators = pd.read_csv("WorldDataBankIndicators.csv",';').to_dict(orient='records')

scl={}
scl['Greece']='#0000ff'
scl['Albania']='#ff0000'
scl['Bulgaria']='#00ff00'
scl['Cyprus']= '#00ffff'

layout= html.Div([
             html.Div([
                 html.Div([

                Header(app),

                     # Selectors
                html.Div(
                     [
                         html.Div(
                             [
                                 html.Br(),
                                 dcc.Dropdown(
                                     id='Country',
                                     options=[{'label': str(item),
                                               'value': str(item)}
                                              for item in set(scl)],
                                     multi=True,
                                     value=list(set(scl))
                                 ),
                             ],

                         ),

                     ],
                     className='ten columns offset-by-one'
                ),

                html.Div([
                html.Label('1st series'),
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i['Name'], 'value': i['DataURL']} for i in Indicators],
             #       value='Marine protected areas (% of territorial waters)',

                ),
                dcc.RadioItems(
                    id='crossfilter-xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'},

                )
                ],className='six columns' ),


                html.Div([
                html.Label('2nd series'),
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i['Name'], 'value': i['DataURL']} for i in Indicators],
            #        value='GDP per capita growth (annual %)',
                ),
                dcc.RadioItems(
                    id='crossfilter-yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
                ], className='six columns')
                 ], className='row')
            ],   className='ten columns offset-by-one',
             ),
        html.Div([
            html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'Greece'}]}
            )
            ], className='six columns'),
            html.Div([
            dcc.Graph(id='x-time-series'),
            dcc.Graph(id='y-time-series'),
            ], className='six columns'),

            html.Div([
                dcc.Slider(
            id='crossfilter-year--slider',
            #min=df['Year'].min(),
            #max=df['Year'].max(),
            min=1950,
            max=2020,
            #value=df['Year'].max(),
            value=2020,
            step=None,
          #  marks={str(year): str(year) for year in df['Year'].unique()}
             )], className='row')
    ], className='ten columns offset-by-one')
])




@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value'),
     dash.dependencies.Input('Country', 'value')
     ])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, year_value,c):
    if (xaxis_column_name == '-' or yaxis_column_name == '-' or xaxis_column_name == None or yaxis_column_name == None):
      return dash.no_update

    dfx=readWorldDataUrl(xaxis_column_name)
    dfy=readWorldDataUrl(yaxis_column_name)
    dfx=dfx[dfx['Country Name'].isin(c)]
    dfy = dfy[dfy['Country Name'].isin(c)]
    for row in Indicators:
        if (row['DataURL'] == yaxis_column_name):
            yname = row['Name']
        if (row['DataURL'] == xaxis_column_name):
            xname = row['Name']

    return {
    'data': [go.Scatter(
        #x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
        x=dfx['Value'],
        y=dfy['Value'],
        text=dfy['Country Name'],
        customdata=dfy['Country Name'],
        mode='markers',
        marker={
            'size': 15,
            'opacity': 0.5,
            'color': [scl[c] for c in list(dfy['Country Name'])],
            'line': {'width': 0.5, 'color': 'black'}
        }
    )],
    'layout': go.Layout(
    xaxis={
        'title': xname,
        'type': 'linear' if xaxis_type == 'Linear' else 'log'
    },
    yaxis={
        'title': yname,
        'type': 'linear' if yaxis_type == 'Linear' else 'log'
    },
    margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
    height=450,
    hovermode='closest'
    )
}

def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     ])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    if (xaxis_column_name == '-' or xaxis_column_name == None):
        return dash.no_update

    for row in Indicators:
        if (row['DataURL'] == xaxis_column_name):
            name = row['Name']
    country_name= hoverData['points'][0]['customdata']
    dfx = readWorldDataUrl(xaxis_column_name)
    dfx = dfx[dfx['Country Name'] == country_name]
    title = '<b>{}</b><br>{}'.format(country_name,   name)
    return create_time_series(dfx, axis_type, title)

@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     ])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    if (yaxis_column_name == '-'  or yaxis_column_name == None):
        return dash.no_update
    dfy = readWorldDataUrl(yaxis_column_name)
    for row in Indicators:
        if (row['DataURL'] == yaxis_column_name):
            name = row['Name']
    country_name= hoverData['points'][0]['customdata']
    dfy = dfy[dfy['Country Name'] == country_name]
    title = '<b>{}</b><br>{}'.format(country_name, name)
    return create_time_series(dfy, axis_type, title)


if __name__ == '__main__':
    app.run_server(debug=True)