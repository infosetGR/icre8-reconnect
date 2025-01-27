# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import shapefile as shp
import plotly.graph_objects as go
import numpy as np
import os.path
import area as ar
import plotly.express as px
import copy
import json

from utils import Header, Footer, make_dash_table, app,STATIC_PATH
from dash.dependencies import Input, Output, State

# Reads Excel with CB input to a dataframe
def ReadCBExcel():

    cb= pd.read_excel(os.path.join(STATIC_PATH,'CBASample.xls'))
    cb = cb.fillna('')
    Iscost=True
    project=''
    category=''

    CR= cb[0:0]
    for i, r in cb.iterrows():
      if i>1:
        if r['Project'] and not r['Project'] is np.nan :  # if is project keep it and do not add row
            category = ''
            area = ''
            areatype = ''
            if r['Project']=='REVENUES':
                Iscost=False
                project=''
            else:
                project=r['Project']
            continue
        r['Project']=project
        if not r['Category'] or r['Category'] is np.nan:  #not add row if has not category
            continue
        if not r['Area'] or r['Area'] is np.nan:
            r['Area']=''
        if not r['AreaType'] or r['AreaType'] is np.nan:
            r['Area'] = ''
        for i in range(1,25):
            if  r['Y'+str(i)]=='':
                r['Y'+str(i)]=0
        if Iscost:
            r["Type"]='Cost'
        else:
            r["Type"] = 'Revenue'
        CR = CR.append(r)

    return CR

cba=ReadCBExcel()


# API keys and datasets
mapbox_access_token = 'pk.eyJ1IjoiZm90aXNzcyIsImEiOiJjazB0cG5qdmcwYW85M2NvMXk1bXIxbGpoIn0.2gG7BRYboHPm-bDQohusCw'

#parses a shapefile to a dataframe for mapbox
def read_shapefile(shp_path):
 
    sf = shp.Reader(shp_path)

    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shpsX = [(s.points[0][0]+s.points[1][0]+s.points[2][0]+s.points[3][0])/4 for s in sf.shapes()]
    shpsY = [(s.points[0][1] + s.points[1][1] + s.points[2][1] + s.points[3][1]) / 4 for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(X=shpsX, Y=shpsY)

    return df

#read all shapefiles specified in ShapeFiles.csv
def read_Maps():
    Layers= pd.read_csv('ShapeFiles.csv', ';')
    maps =  pd.DataFrame()
    for i,r in Layers.iterrows():

        script_dir = os.path.dirname(__file__)
        rel_path = r['File']
        abs_file_path = os.path.join(script_dir, rel_path)
        # Selecting only required columns
        map_data = read_shapefile(abs_file_path)

        if 'X' in map_data and 'Y' in map_data:
            if 'Id' in map_data and 'Percentage' in map_data:
                map_data = map_data[["X", "Y", "Id", "Percentage"]].drop_duplicates()
            elif 'id' in map_data and 'Percentage' in map_data:
                map_data=map_data.rename({'id': 'Id'}, axis=1)
                map_data = map_data[["X", "Y", "Id", "Percentage"]].drop_duplicates()
            else:
                map_data = map_data[["X", "Y"]].drop_duplicates()
                map_data['Id']=i
                map_data['Percentage'] = 0

        map_data['Country'] = r['Country']
        map_data['Type'] = r['Type']

        maps = maps.append(map_data)
    return maps

map_data=read_Maps()






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

def layout_map(title):
    return go.Layout(
        autosize=True,
        height=500,
        font=dict(color="#191A1A"),
        titlefont=dict(color="#191A1A", size=14),
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=45
        ),
        title=title,
        hovermode="closest",
        plot_bgcolor='#000000',
        paper_bgcolor='#fffcfc',
        legend=dict(font=dict(size=10), orientation='h'),
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
scl['Mpa','0']='#000000'
scl['Mpa','1-10']='#97ccf0'
scl['Mpa','10-50']='#62acde'
scl['Mpa','50-100']= '#004d80'
scl['Posidonia','0']='#FFFFFF'
scl['Posidonia','1-10']='#97ccf0'
scl['Posidonia','10-50']='#62acde'
scl['Posidonia','50-100']= '#004d80'
scl['Rocky','0']='#FFFFFF'
scl['Rocky','1-10']='#c2c2c2'
scl['Rocky','10-50']='#8a8a8a'
scl['Rocky','50-100']= '#454545'
scl['Sandy','0']='#FFFFFF'
scl['Sandy','1-10']='#d5c3a1'
scl['Sandy','10-50']='#b99c6b'
scl['Sandy','50-100']= '#a5714e'
# functions

# returns map from dataframe
def gen_map(md):
    type=set(md['Type'])
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(md['Y']),
                "lon": list(md['X']),
                "text":list(md['Id']),
                "hoverinfo": "text",
                "hovertext":  list(md['Percentage']),
                "mode": "markers",
                "name": list(md['Id']),
                "marker": {
                    "size": 10,
                    "opacity": 0.7,
                    "color": [scl[list(type)[0],str(per)] for per in list(md['Percentage'])]

                }
        }],
        "layout": layout_map(list(type)[0]),
    }



'''  html.Div(
                    dcc.ConfirmDialogProvider(
                        children=html.Button(
                            'Click Me', 
                        ), 
                        id='danger-danger-provider',
                        message='Danger danger! Are you sure you want to continue?'
                    ),
                )'''

# Main Layout
layout= html.Div([ html.Div(
    html.Div([
        html.Div(
            [
                Header(app),
                dcc.Store(id="MapCostRevdata"),

                html.Div(children='',
                         id='display',
                         className='nine columns'
                ),
                html.Div(id='intermediate-value', style={'display': 'none'}),
                html.Div(id='intermediate-value2', style={'display': 'none'}),
                html.Table(id='table'),
            ], className="row"
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Country:'),
                        dcc.Dropdown(
                                id = 'Country',
                                options=[{'label': str(item),
                                      'value': str(item)}
                                     for item in set(map_data['Country'])],
                                value='Cyprus',
                        ),
                        html.P('Choose Layer:'),
                        dcc.Dropdown(
                            id='Layer',
                            options=[{'label': str(item),
                                      'value': str(item)}
                                     for item in set(map_data['Type'])],
                            value='Posidonia',
                        ),
                        html.P('%:'),
                        dcc.Dropdown(
                            id='Percentage',
                            options=[{'label': str(item) + '%',
                                      'value': str(item)}
                                     for item in set(map_data['Percentage'])],
                            multi=True,
                            value=list(set(map_data['Percentage']))
                        ),
                        html.P('Projects:'),
                        dcc.Dropdown(
                            id='Project',
                            options=[{'label': str(item),
                                      'value': str(item)}
                                     for item in set(cba['Project'])],
                            multi=True,
                            value=list(set(cba['Project']))
                        ),
                        html.P('Inflation rate %:'),
                        dcc.Input(id="Inflation",
                                  type="number",
                                  placeholder="Inflation",
                                  value=0, max=20, min=-20
                                  ),
                        html.P('Interest rate %:'),
                        dcc.Input(id="Interest",
                                  type="number",
                                  placeholder="Interest",
                                  value=0, max=20, min=-20
                                  ),

                        html.P('Category:'),
                        dcc.Dropdown(
                            id='Category',
                            options=[{'label': str(item),
                                      'value': str(item)}
                                     for item in set(cba['Category'])],
                            multi=True,
                            value=list(set(cba['Category']))
                        ),
                        html.P('Type:'),
                        dcc.Dropdown(
                            id='Type',
                            options=[{'label': str(item),
                                      'value': str(item)}
                                     for item in set(cba['Type'])],
                            multi=True,
                            value=list(set(cba['Type']))
                        ),
                        html.P('Years (1-20):'),
                        dcc.Slider(id='Years',
                                   min=1,
                                   max=20,
                                   step=1,
                                   value=10
                                   ),
                        html.Div(id='slider-output-container'),
                        html.Br(),
                        html.Br(),
                        html.Label('Graph Type & Values'),
                        dcc.RadioItems(
                            id="CBcharttype",
                            options=[
                                {"label": "Line", "value": "Line"},
                                {"label": "Bar", "value": "Bar"},
                            ],
                            value="Bar",
                            className="three columns",
                        ),
                        dcc.RadioItems(
                            id="Cumulative",
                            options=[
                                {"label": "per Year", "value": "No"},
                                {"label": "Cumulative", "value": "Yes"},
                            ],
                            value="No",
                            className="three columns",
                        ),
                    ],
                    className='six columns',

                ),  html.Div(
                    [
                        html.Label('Select an area on the Map:'),
                        dcc.Graph(id='map-graph',
                                  animate=False,
                                  style={'margin-bottom': '0'}),
                        html.Div(id='area1'),
                        dcc.Dropdown(
                            id='cost-rev-selection',
                            options=[
                                {"label": "Cost", "value": "Cost"},
                                {"label": "Revenue", "value": "Revenue"},
                                {"label": "NPV", "value": "NPV"},
                            ],
                            value='Cost',
                        ),
                        html.Label('Select an area on the Map (B) for comparison:'),
                        dcc.Graph(id='cost-rev-graph',
                                  animate=False,
                                  style={'margin-bottom': '0'}),
                        html.Div(id='area2'),

                    ], className = "six columns"


                ),

            ],
            className='row'
        ),

        # Map + table + Histogram
        html.Div(
            [

                html.Br(),
                html.H3('Cost-Benefit Analysis'),
                html.Div([
                    dcc.Graph(
                        id='bar-graph'
                    )
                ], className='twelve columns'
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='costpie'
                        )
                    ], className='six columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            id='revenuepie'
                        )
                    ], className='six columns'
                    )], className='twelve columns'),
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='costperareapie'
                        )
                    ], className='six columns'
                    ),
                    html.Div([
                        dcc.Graph(
                            id='costperareatypepie'
                        )
                    ], className='six columns'
                    )], className='twelve columns'),

                html.Div(
                    [
                        html.P('Selected Areas:'),
                        dt.DataTable(
                            id='selectedpointsDataTable',
                            columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in
                                     {'Percentage', 'Type', 'Count'}],
                            # data=cba.to_dict('records'),
                            # columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in cba.columns
                            #         ],
                            editable=False,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                            row_selectable=False,
                            row_deletable=False,
                            page_action="native",
                            # page_current=0,
                            # page_size=5
                        ),
                        html.Div(
                            [
                        dt.DataTable(
                            id='selectedpointsDataTable2',
                            columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in
                                     {'Percentage', 'Type', 'Count'}],
                            # data=cba.to_dict('records'),
                            # columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in cba.columns
                            #         ],
                            editable=False,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                            row_selectable=False,
                            row_deletable=False,
                            page_action="native",
                            # page_current=0,
                            # page_size=5
                        )], style={'display': 'none'})
                    ],
                    style=layout_table,
                    className="six columns"
                ),

                html.Div(
                    [   html.P('Cost-Benefit Input'),
                        dt.DataTable(
                            id='datatable',
                            data=cba.to_dict('records'),
                            columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in cba.columns
                            ],
                            editable=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                            row_selectable=False,
                            row_deletable=False,
                            page_action="native",
                            page_current=0

                            ),
                    ],
                    style = layout_table,
                    className="twelve columns"
                ),

                Footer(app)

            ], className="row"
        )
    ], className='ten columns offset-by-one'))
])


# Slider => show selected value
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('Years', 'value')])
def update_output(value):
    return 'You have selected {} years'.format(value)



@app.callback(
    Output('cost-rev-graph','figure'),
    [ Input('MapCostRevdata','data'),
      Input('cost-rev-selection','value'),
    ])
def mapcostrevplot(json_data,costorrev):

    px.set_mapbox_access_token(mapbox_access_token)

    dff = pd.read_json(json_data, orient='records')
    if len(dff)==0:
        return  {'data': []}

    mmd=map_data.merge(dff, how='left', left_on=['Type', 'Percentage'], right_on=['Area','Percentage'])

    mmdg=mmd.groupby(['X','Y']).sum().reset_index()

    fig = px.scatter_mapbox(mmdg, lat="Y", lon="X", color=costorrev, opacity= 0.7,
                            color_continuous_scale=px.colors.sequential.Peach if costorrev=='Cost' else px.colors.sequential.Greens if costorrev=='Revenue' else px.colors.sequential.Blues, zoom=12)

    return fig



# Options => Map layer
@app.callback(
    Output('map-graph', 'figure'),
    [Input('Layer', 'value'),
     Input('Country', 'value'),
     Input('Percentage','value'),
     #Input('MapCostRevdata','data'),
     ])
def map_selection(layer,country,per):

    aux = map_data[map_data['Type']==layer]
    aux=aux[aux['Country']==country]
    aux = aux[aux['Percentage'].isin(per)]
 #   temp_df = aux.ix[selected_row_ids, :]
 #   if len(selected_row_ids) == 0:
 #       return gen_map(aux)
    return gen_map(aux)


@app.callback(Output('area1', 'children'),
              [Input('map-graph', 'selectedData')
               ])
def selectData(selectData):
    coor = []
    if selectData == None:
        return ''

    for i in range(len(selectData['points'])):
        coor.append([selectData['points'][i]['lon'], selectData['points'][i]['lat']])
    obja = {'type': 'Polygon', 'coordinates': [coor]}
    x = ar.area(obja)
    return 'Selected area:'+ f"{int(x):,d}"+' m²'

@app.callback(Output('area2', 'children'),
              [Input('cost-rev-graph', 'selectedData')
               ])
def selectData(selectData):
    coor = []
    if selectData == None:
        return ''

    for i in range(len(selectData['points'])):
        coor.append([selectData['points'][i]['lon'], selectData['points'][i]['lat']])
    obja = {'type': 'Polygon', 'coordinates': [coor]}
    x = ar.area(obja)
    return 'Selected area:'+f"{int(x):,d}"+' m²'


# Map selection of area => Intermediate field for aggregate types and percentages
@app.callback(Output('intermediate-value2','children'),
    [Input('cost-rev-graph','selectedData')
    ])
def selectData(selectData):
        filtList = []
        coor=[]
        if selectData==None:
            return ''.format(filtList)
        else :
          #  selmapdata = map_data[map_data["Id"].isin(selectData['points']['text'])]
            for i in range(len(selectData['points'])):
                filtList.append(selectData['points'][i]['pointIndex'])
                coor.append([selectData['points'][i]['lon'],selectData['points'][i]['lat']])
            obja={'type':'Polygon','coordinates':[coor]}

            x= ar.area(obja)
            print(x)
            selmapdata = map_data[map_data["Id"].isin(filtList)].groupby(['Percentage','Type']).size().reset_index()
            selmapdata.columns = ['Percentage' , 'Type'  ,'Count']
            return selmapdata.to_json(date_format='iso', orient='records')
           # str('Selecting points produces a nested dictionary: {}'.format(filtList))

# Map selection of area => Intermediate field for aggregate types and percentages
@app.callback(Output('intermediate-value','children'),
    [Input('map-graph','selectedData')
    ])
def selectData(selectData):
        filtList = []
        if selectData==None:
            return ''.format(filtList)
        else :
          #  selmapdata = map_data[map_data["Id"].isin(selectData['points']['text'])]

            for i in range(len(selectData['points'])):
                filtList.append(selectData['points'][i]['text'])
            selmapdata = map_data[map_data["Id"].isin(filtList)].groupby(['Percentage','Type']).size().reset_index()
            selmapdata.columns = ['Percentage' , 'Type'  ,'Count']
            return selmapdata.to_json(date_format='iso', orient='records')
           # str('Selecting points produces a nested dictionary: {}'.format(filtList))

#Intermediate field for aggregate types and percentages => Table
@app.callback(
    Output('selectedpointsDataTable', 'data'),
    [Input('intermediate-value', 'children')])
def update_table(jsonified_cleaned_data):
    rows=[]
    if not jsonified_cleaned_data is None and len(jsonified_cleaned_data)>0:
        dff= pd.read_json(jsonified_cleaned_data, orient='records')
        rows = dff.to_dict('records')
    return rows


#Intermediate field for aggregate types and percentages => Table
@app.callback(
    Output('selectedpointsDataTable2', 'data'),
    [Input('intermediate-value2', 'children')])
def update_table(jsonified_cleaned_data):
    rows=[]
    if not jsonified_cleaned_data is None and len(jsonified_cleaned_data)>0:
        dff= pd.read_json(jsonified_cleaned_data, orient='records')
        rows = dff.to_dict('records')
    return rows


@app.callback(
    Output('costperareatypepie', 'figure'),
    [Input('datatable', 'data'),
     Input('selectedpointsDataTable', 'data'),
     Input('Years', 'value'),
     Input('Category', 'value'),
     Input('Inflation', 'value'),
     Input('Interest', 'value'),
     Input('Project', 'value'),
     Input('Country', 'value'),
     ])
def update_figure(cbdata, areasdata, years, costrevcategory, interest, inflation, projects, country):
    if len(cbdata) == 0 or areasdata == None or len(areasdata) == 0:
        return dash.no_update

    c = produce_aggregate_area(cbdata, areasdata, years, 'Cost', costrevcategory, interest, inflation,
                               projects, country)

    c['Area']=c['Area'] + ' '+ c['Percentage']
    c = c.groupby(['Area']).sum().reset_index()

    c = c.replace(to_replace=[' all','all','',' '], value='Other')

    fig = go.Figure(data=[go.Pie(labels=c['Area'], values=c['Cost'])])
    fig.update_layout(title='Cost per Area percentage', showlegend=True)
    return fig

@app.callback(
    Output('costperareapie', 'figure'),
    [Input('datatable', 'data'),
     Input('selectedpointsDataTable','data'),
     Input('Years','value'),
     Input('Category','value'),
     Input('Inflation','value'),
     Input('Interest','value'),
     Input('Project','value'),
     Input('Country','value'),
    ])
def update_figure(cbdata,areasdata,years, costrevcategory, interest,inflation,projects,country):
    if len(cbdata) == 0 or areasdata == None or len(areasdata) == 0:
        return dash.no_update


    c = produce_aggregate_area(cbdata, areasdata, years, 'Cost', costrevcategory, interest, inflation,
                                              projects, country)
    c= c.groupby(['Area']).sum().reset_index()
    c= c.replace(to_replace=[' all','all', '', ' '], value='Other')

    fig = go.Figure(data=[go.Pie(labels=c['Area'], values=c['Cost'])])
    fig.update_layout(title='Cost per Area', showlegend=True)
    return fig

# cost Pie chart
@app.callback(
    Output('costpie', 'figure'),
    [Input('datatable', 'data'),
     Input('selectedpointsDataTable','data'),
     Input('Years','value'),
     Input('Category','value'),
     Input('Inflation','value'),
     Input('Interest','value'),
     Input('Project','value'),
     Input('Country','value'),
    ])
def update_figure(cbdata,areasdata,years, costrevcategory, interest,inflation,projects,country):
    if len(cbdata) == 0 or areasdata == None or len(areasdata) == 0:
        return dash.no_update


    category, cost, rev = produce_aggregate_category(cbdata, areasdata, years, 'Cost', costrevcategory, interest, inflation,
                                              projects, country)

    fig = go.Figure(data=[go.Pie(labels=category, values=cost)])
    fig.update_layout(title='Cost per category', showlegend=True)
    return fig

# Revenue Pie chart
@app.callback(
    Output('revenuepie', 'figure'),
    [Input('datatable', 'data'),
     Input('selectedpointsDataTable','data'),
     Input('Years','value'),
     Input('Category','value'),
     Input('Inflation','value'),
     Input('Interest','value'),
     Input('Project','value'),
     Input('Country','value'),
    ])
def update_figure(cbdata,areasdata,years, costrevcategory, interest,inflation,projects,country):
    if len(cbdata) == 0 or areasdata == None or len(areasdata) == 0:
        return dash.no_update


    category, cost, rev = produce_aggregate_category(cbdata, areasdata, years, 'Revenue' , costrevcategory, interest, inflation,
                                              projects, country)

    fig = go.Figure(data=[go.Pie(labels=category, values=rev)])
    fig.update_layout(title='Revenues per category', showlegend=True, )
    return fig




#Main CBA graph
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('datatable', 'data'),
     Input('selectedpointsDataTable','data'),
     Input('selectedpointsDataTable2','data'),
     Input('Years','value'),
     Input('Type','value'),
     Input('Category','value'),
     Input('Inflation','value'),
     Input('Interest','value'),
     Input('Project','value'),
     Input('Country','value'),
     Input('CBcharttype','value'),
     Input('Cumulative','value')
    ])
def update_figure(cbdata,areasdata,areasdata2,years,costorrev, costrevcategory, interest,inflation,projects,country,charttype,cumulative ):
    if  len(cbdata)==0 or areasdata == None or len(areasdata)==0:
        return dash.no_update

    index, cost, revenue, npv = produce_aggregate(cbdata, areasdata,years,costorrev, costrevcategory, interest,inflation,projects,country,cumulative)
    index2, cost2, revenue2, npv2=index, cost, revenue, npv

    if len(areasdata2)>0:
        index2, cost2, revenue2, npv2 = produce_aggregate(cbdata, areasdata2, years, costorrev, costrevcategory, interest,
                                                      inflation, projects, country, cumulative)
    fig = go.Figure()
    if(charttype=='Line'):
        fig.add_trace(go.Scatter(
            mode="lines",
            name="Cost",
            x=index,
            y=cost,
            line=dict(shape="spline", smoothing=0.1, color="#ff9999")))
        fig.add_trace(go.Scatter(
            mode="lines",
            name="Revenue",
            x=index,
            y=revenue,
            line=dict(shape="spline", smoothing=0.1, color="#80ffbf")))

        fig.add_trace(go.Scatter(
            mode="lines",
            name="NPV",
            x=index,
            y=npv,
            line=dict(shape="spline", smoothing=0.1, color="#3385ff")))

        if len(areasdata2) > 0:
            fig.add_trace(go.Scatter(
                mode="lines",
                name="NPV-2",
                x=index2,
                y=npv2,
                line=dict(shape="spline", smoothing=0.1, color="#ff00ff")))
            fig.add_trace(go.Scatter(
                mode="lines",
                name="Cost B",
                x=index2,
                y=cost2,
                line=dict(shape="spline", smoothing=0, color="#ff6666", dash='dash')))
            fig.add_trace(go.Scatter(
                mode="lines",
                name="Revenue B",
                x=index2,
                y=revenue2,
                line=dict(shape="spline", smoothing=0, color="#006600", dash='dash')))

        fig.update_layout(
            title='Cost & Revenues',
            showlegend=True,
            dragmode="select",
            xaxis=dict(
                showgrid=False,
                nticks=years,
                fixedrange=False
            ),
            yaxis=dict(
                showticklabels=True,
                showgrid=False,
                fixedrange=False,
                zeroline=True)
        )
    else:
        c = pd.Series(cost)

        fig.add_trace(go.Bar(
            name="Cost",
            marker_color='#ff9999',
            x=index,
            y=c * -1,
            ))
        fig.add_trace(go.Bar(
            name="Revenue",
            marker_color='#80ffbf',
            x=index,
            y=revenue,
        ))

        fig.add_trace(go.Scatter(
            mode="lines",
            name="NPV",
            x=index,
            y=npv,
            line=dict(shape="spline", smoothing=0.1, color="#3385ff")))
        if len(areasdata2) > 0:
            fig.add_trace(go.Scatter(
                mode="lines",
                name="NPV B",
                x=index2,
                y=npv2,
                line=dict(shape="spline", smoothing=0.1, color="#ff00ff",dash = 'dash')))
            fig.add_trace(go.Scatter(
                mode="lines",
                name="Cost B",
                x=index2,
                y=cost2,
                line=dict(shape="spline", smoothing=0, color="#ff6666",dash = 'dash')))
            fig.add_trace(go.Scatter(
                mode="lines",
                name="Revenue B",
                x=index2,
                y=revenue2,
                line=dict(shape="spline", smoothing=0, color="#006600",dash = 'dash')))

        fig.update_layout(barmode='relative', title='Cost & Revenues', showlegend=True,)



    return fig

# calculate cost benefit graph data
def produce_aggregate(cbdata, areas, years, costorrev, costrevcategory, interest, inflation, projects, country,cumulative):
    index = list(range(1,years+1))
    cost=[]
    revenue=[]
    npvs=[]

    ar=pd.DataFrame(areas)
    r = 1 + (interest - inflation)/100
    npv=0
    i=1
    for year in index:
        sumcost = 0
        sumrev = 0
        for cb in cbdata:
            if cb['Project'] in projects:
                if cb['Category'] in costrevcategory:
                    if cb['Type']=='Cost':
                        if cb['Area']=='':
                            if cb['AreaType']=='':
                                sumcost+=cb['Y'+str(year)]
                            elif  cb['AreaType']=='all':
                                sumcost += cb['Y' + str(year)] * ar['Count'].sum()
                            else:
                                sumcost+= cb['Y' + str(year)] * ar[ar["Percentage"]==cb['AreaType']]['Count'].sum()
                        else:
                            if cb['AreaType'] == '' or cb['AreaType'] == 'all':
                                sumcost += cb['Y' + str(year)] * ar[ar["Type"] == cb['Area']]['Count'].sum()
                            else:
                                sumcost += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
                    elif cb["Type"] == 'Revenue':
                        if cb['Area'] == '':
                            if cb['AreaType'] == '':
                                sumrev += cb['Y' + str(year)]
                            elif cb['AreaType'] == 'all':
                                sumrev += cb['Y' + str(year)] * ar['Count'].sum()
                            else:
                                sumrev += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
                        else:
                            if cb['AreaType'] == '' or cb['AreaType'] == 'all':
                                sumrev += cb['Y' + str(year)] * ar[ar["Type"] == cb['Area']]['Count'].sum()
                            else:
                                sumrev += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
        if i==1 or cumulative=='No':
            cost.append(sumcost)
            revenue.append(sumrev)
            npvs.append(sumrev - sumcost)
        else:
            cost.append(float(cost[-1])+sumcost)
            revenue.append(float(revenue[-1])+sumrev)
            npvs.append(float(npvs[-1])+(sumrev - sumcost)/r**i)
        i=i+1
    return index, cost,revenue, npvs

# calculate cost benefit data per category
def produce_aggregate_category(cbdata, areas, years,costorrev,costrevcategory, interest, inflation, projects, country):
    index = list(range(1,years+1))
    cost=[]
    revenue=[]
    category=[]

    ar=pd.DataFrame(areas)
    r = 1 + (interest - inflation)/100
    npv=0
    i=1

    for cb in cbdata:
        sumcost = 0
        sumrev = 0
        for year in index:
            if cb['Project'] in projects:
                if cb['Category'] in costrevcategory:
                    if cb['Type']=='Cost' and  cb['Type'] in costorrev:
                        if not cb['Area']==None or len(cb['Area'])==0:
                            if len(cb['AreaType'])==0:
                                sumcost+=cb['Y'+str(year)]
                            elif  cb['AreaType']=='all':
                                sumcost += cb['Y' + str(year)] * ar['Count'].sum()
                            else:
                                sumcost+= cb['Y' + str(year)] * ar[ar["Percentage"]==cb['AreaType']]['Count'].sum()
                        else:
                            if cb['AreaType'] == '' or cb['AreaType'] == 'all':
                                sumcost += cb['Y' + str(year)] * ar[ar["Type"] == cb['Area']]['Count'].sum()
                            else:
                                sumcost += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
                    elif cb["Type"] == 'Revenue'  and  cb['Type'] in costorrev:
                        if not cb['Area']==None or len(cb['Area']) == 0:
                            if len(cb['AreaType']) == 0:
                                sumrev += cb['Y' + str(year)]
                            elif cb['AreaType'] == 'all':
                                sumrev += cb['Y' + str(year)] * ar['Count'].sum()
                            else:
                                sumrev += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
                        else:
                            if cb['AreaType'] == '' or cb['AreaType'] == 'all':
                                sumrev += cb['Y' + str(year)] * ar[ar["Type"] == cb['Area']]['Count'].sum()
                            else:
                                sumrev += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
        if cb['Type'] in costorrev:
            if sumcost>0 or sumrev>0:
                category.append(cb['Category'])
                cost.append(sumcost)
                revenue.append(sumrev)
        i=i+1
    return category, cost,revenue

# calculate cost benefit per area
def produce_aggregate_area(cbdata, areas, years,costorrev,costrevcategory, interest, inflation, projects, country):
    index = list(range(1,years+1))
    cost=[]
    revenue=[]
    category=[]

    ar=pd.DataFrame(areas)
    r = 1 + (interest - inflation)/100
    npv=0
    i=1

    CostRevArea=pd.DataFrame(columns=['Area','Percentage','Cost','Revenue'])

    for cb in cbdata:
        sumcost = 0
        sumrev = 0
        for year in index:
            if cb['Project'] in projects:
                if cb['Category'] in costrevcategory:
                    if cb['Type']=='Cost' and  cb['Type'] in costorrev:
                        if not cb['Area']==None or len(cb['Area'])==0:
                            if len(cb['AreaType'])==0:
                                sumcost+=cb['Y'+str(year)]
                            elif  cb['AreaType']=='all':
                                sumcost += cb['Y' + str(year)] * ar['Count'].sum()
                            else:
                                sumcost+= cb['Y' + str(year)] * ar[ar["Percentage"]==cb['AreaType']]['Count'].sum()
                        else:
                            if cb['AreaType'] == '' or cb['AreaType'] == 'all':
                                sumcost += cb['Y' + str(year)] * ar[ar["Type"] == cb['Area']]['Count'].sum()
                            else:
                                sumcost += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
                    elif cb["Type"] == 'Revenue'  and  cb['Type'] in costorrev:
                        if not cb['Area']==None or len(cb['Area']) == 0:
                            if len(cb['AreaType']) == 0:
                                sumrev += cb['Y' + str(year)]
                            elif cb['AreaType'] == 'all':
                                sumrev += cb['Y' + str(year)] * ar['Count'].sum()
                            else:
                                sumrev += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
                        else:
                            if cb['AreaType'] == '' or cb['AreaType'] == 'all':
                                sumrev += cb['Y' + str(year)] * ar[ar["Type"] == cb['Area']]['Count'].sum()
                            else:
                                sumrev += cb['Y' + str(year)] * ar[ar["Percentage"] == cb['AreaType']]['Count'].sum()
        if cb['Type'] in costorrev:
            if sumcost>0 or sumrev>0:
                CostRevArea= CostRevArea.append({'Area':cb['Area'],'Percentage':cb['AreaType'],'Cost':sumcost, 'Revenue':sumrev}, ignore_index=True)
        i=i+1
    return CostRevArea

#Draws 2nd map (cost-revenue)
@app.callback(
    Output('MapCostRevdata', 'data'),
    [Input('datatable', 'data'),
      Input('Years', 'value'),
      Input('Type', 'value'),
      Input('Category', 'value'),
      Input('Inflation', 'value'),
      Input('Interest', 'value'),
      Input('Project', 'value'),
      Input('Country', 'value'),
      Input('Layer', 'value'),
    ])
def map_selection(cbdata, years, Type, costrevcategory, interest, inflation,
                                              projects, country,layer):

    areacost= calcAreaCost(cbdata, years, Type, costrevcategory, interest, inflation,
                                              projects, country)

    return areacost.to_json(date_format='iso', orient='records')


#Calculates total cost-benefit per area point
def calcAreaCost(cbdata, years, costorrev, costrevcategory, interest, inflation, projects, country):
    index = list(range(1, years + 1))
    cost = []
    revenue = []
    category = []

    r = 1 + (interest - inflation) / 100
    cra = pd.DataFrame(columns=['Area', 'Percentage', 'Cost', 'Revenue','NPV'])


    for cb in cbdata:
        sumcost = 0
        sumrev = 0
        for year in index:
            if cb['Project'] in projects:
                if cb['Category'] in costrevcategory:
                    if cb['Type'] == 'Cost' and cb['Type'] in costorrev:
                            sumcost += cb['Y' + str(year)]
                    elif cb["Type"] == 'Revenue' and cb['Type'] in costorrev:
                            sumrev += cb['Y' + str(year)]
        if sumcost > 0 or sumrev > 0:
            cra = cra.append({'Area': cb['Area'], 'Percentage': cb['AreaType'], 'Cost': sumcost, 'Revenue': sumrev, 'NPV':sumcost-sumrev}, ignore_index=True)


    cra  = cra.groupby(['Area','Percentage']).sum().reset_index()


    for index, row in cra.iterrows():
        row['Cost'] += cra[(cra['Area'] == '') & (cra['Percentage'] == 'all')]['Cost'].sum()
        row['Cost'] += cra[(cra['Area'] == row['Area']) & (cra['Percentage'] == 'all')]['Cost'].sum()
        row['Cost'] += cra[(cra['Area'] == row['Area']) & (cra['Percentage'] == row['Percentage'])]['Cost'].sum()
        row['Revenue'] += cra[(cra['Area'] == '') & (cra['Percentage'] == 'all')]['Revenue'].sum()
        row['Revenue'] += cra[(cra['Area'] == row['Area']) & (cra['Percentage'] == 'all')]['Revenue'].sum()
        row['Revenue'] += cra[(cra['Area'] == row['Area']) & (cra['Percentage'] == row['Percentage'])]['Revenue'].sum()
        cra.loc[index, 'Cost']=row['Cost']
        cra.loc[index, 'Revenue'] = row['Revenue']

    if len(cra)>0 :
        cra.drop(cra.loc[cra['Area'] == ''].index, inplace=True)
        cra.drop(cra.loc[cra['Percentage'] == ''].index, inplace=True)
        cra.drop(cra.loc[cra['Percentage'] == 'all'].index, inplace=True)

    return cra

#if __name__ == '__main__':
#    app.run_server(debug=False)
