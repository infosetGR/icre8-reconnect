# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns


from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State #, Event

app = dash.Dash(__name__)
server = app.server
app.title = 'Reconnect DSS'

# API keys and datasets
mapbox_access_token = 'pk.eyJ1IjoiZm90aXNzcyIsImEiOiJjazB0cG5qdmcwYW85M2NvMXk1bXIxbGpoIn0.2gG7BRYboHPm-bDQohusCw'
#map_data = pd.read_csv("CY_Posidonia_100m.csv")

sf = shp.Reader('./spatial-vector-lidar/Cyprus_Posidonia/CY_Posidonia_100m.shp')

def read_shapefile(shp_path):
 
    sf = shp.Reader(shp_path)

    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shpsX = [(s.points[0][0]+s.points[1][0]+s.points[2][0]+s.points[3][0])/4 for s in sf.shapes()]
    shpsY = [(s.points[0][1] + s.points[1][1] + s.points[2][1] + s.points[3][1]) / 4 for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(X=shpsX, Y=shpsY)

    return df


map_data = read_shapefile( './spatial-vector-lidar/Cyprus_Posidonia/CY_Posidonia_100m.shp')
# Selecting only required columns
#map_data = map_data[["Borough", "Type", "Provider", "Name", "Location", "Latitude", "Longitude"]].drop_duplicates()

map_data = map_data[["X","Y","Id","Percentage"]].drop_duplicates()

# Boostrap CSS.
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


#  Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#000000',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='CY posidonia',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=34.07,
            lat=34.97
        ),
        zoom=12,
    )
)

scl={}
scl['0']='#FFFFFF'
scl['1-10']='#CCE8FF'
scl['10-50']='#3379B2'
scl['50-100']= '#002A4C'

# functions

def gen_map(map_data):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(map_data['Y']),
                "lon": list(map_data['X']),
                "text":list(map_data['Percentage']),
                "hoverinfo": "text",
                "hovertext":  list(map_data['Percentage']),
                #[["Name: {} <br>Type: {} <br>Provider: {}".format(i,j,k)]
                #               for i,j,k in zip(map_data['Name'], map_data['Type'],map_data['Provider'])],
                "mode": "markers",
            #    "name": list(map_data['Name']),
                "name": list(map_data['Percentage']),
                "marker": {
                    "size": 10,
                    "opacity": 0.7,
                    "color": [scl[per] for per in list(map_data['Percentage'])]

                }
        }],
        "layout": layout_map
    }

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Reconnect',
                        className='nine columns'),
                html.Img( id='ddd',
                    src=app.get_asset_url('icre8-logo.png'),
                    className='three columns',
                    style={
                        'height': '16%',
                        'width': '16%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 12,
                        'padding-right': 0
                    },
                ),
                html.Div(children='''
                        Message
                        ''',
                         id='display',
                        className='nine columns'
                ),
                html.Div(
                    dcc.ConfirmDialogProvider(
                        children=html.Button(
                            'Click Me',
                        ),
                        id='danger-danger-provider',
                        message='Danger danger! Are you sure you want to continue?'
                    ),
                )
            ], className="row"
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Borroughs:'),
                        dcc.Checklist(
                                id = 'boroughs',
                                options=[
                                    {'label': 'Manhattan', 'value': 'MN'},
                                    {'label': 'Bronx', 'value': 'BX'},
                                    {'label': 'Queens', 'value': 'QU'},
                                    {'label': 'Brooklyn', 'value': 'BK'},
                                    {'label': 'Staten Island', 'value': 'SI'}
                                ],
                                value=['MN', 'BX', "QU",  'BK', 'SI'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Type:'),
                        dcc.Dropdown(
                            id='type',
                            options= [{'label': str(item),
                                                  'value': str(item)}
                                                 for item in set(map_data['Percentage'])],
                            multi=True,
                            value=list(set(map_data['Percentage']))
                        )
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
            ],
            className='row'
        ),

        # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True,
                                  style={'margin-top': '20'})
                    ], className = "six columns"
                ),
                html.Div(
                    [
                        dt.DataTable(
                            id='datatable',
                            data=map_data.to_dict('records'),
                            columns=[ {"name": i, "id": i, "deletable": True, "selectable": True} for i in map_data.columns
                            ],
                            editable=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                            row_selectable="multi",
                            row_deletable=True,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10
                            ),
                    ],
                    style = layout_table,
                    className="six columns"
                ),
                html.Div([
                        dcc.Graph(
                            id='bar-graph'
                        )
                    ], className= 'twelve columns'
                    ),
                html.Div(
                    [
                        html.P('Developed by Fotis Stathopoulos - Infoset ', style = {'display': 'inline'}),
                        html.A('fotis@infoset.co', href = 'mailto:fotis@infoset.co')
                    ], className = "twelve columns",
                       style = {'fontSize': 12, 'padding-top': 20}
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one'))

"""
@app.callback(
    Output('confirm', 'displayed')
    [Input('datatable', 'derived_virtual_selected_rows')])
def display_confirm(value):
    if value == 'Danger!!':
        return True
    return False
"""

@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'data'),
     Input('datatable', 'selected_row_ids')])
def map_selection(rows, selected_row_ids):
    aux = pd.DataFrame(rows)
 #   temp_df = aux.ix[selected_row_ids, :]
 #   if len(selected_row_ids) == 0:
 #       return gen_map(aux)
    return gen_map(aux)


@app.callback(Output('display','children'),[Input('map-graph','selectedData')])
def selectData(selectData):
        filtList = []
        if selectData==None:
            return ''
        else :
            for i in range(len(selectData['points'])):
                filtList.append(selectData['points'][i]['text'])
        return str('Selecting points produces a nested dictionary: {}'.format(filtList))


"""
@app.callback(
    Output('datatable', 'data'),
    [Input('type', 'value'),
     Input('boroughs', 'value')])
def update_selected_row_indices(type, borough):
    map_aux = map_data.copy()

    # Type filter
    map_aux = map_aux[map_aux['Type'].isin(type)]
    # Boroughs filter
    map_aux = map_aux[map_aux["Borough"].isin(borough)]

    rows = map_aux.to_dict('records')
    return rows
"""
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('datatable', 'data'),
     Input('datatable', 'selected_rows')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)

    layout = go.Layout(
        bargap=0.05,
        bargroupgap=0,
        barmode='group',
        showlegend=False,
        dragmode="select",
        xaxis=dict(
            showgrid=False,
            nticks=50,
            fixedrange=False
        ),
        yaxis=dict(
            showticklabels=True,
            showgrid=False,
            fixedrange=False,
            rangemode='nonnegative',
            zeroline=False        )
    )

    data = Data([
         go.Bar(x=dff
      #       x=dff.groupby('Borough', as_index = False).count()['Borough'],
      #       y=dff.groupby('Borough', as_index = False).count()['Type']
         )
     ])

    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
