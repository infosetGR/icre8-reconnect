import base64
import datetime
import io
import os
from urllib.parse import quote as urlquote

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from flask import Flask,send_file,send_from_directory

#server = Flask(__name__)

import pandas as pd
from utils import Header, make_dash_table,readWorldDataUrl, app

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download')

'''
@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(STATIC_PATH, path, as_attachment=True)
'''

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


layout= html.Div([
             html.Div([
                 html.Div([
                Header(app),
                html.Br(),
                html.Br(),
                html.H3('Import CSV'),
                file_download_link('SampleWD.csv'),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '80%',
                        'height': '40px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(id='output-data-upload'),

                html.H3('Import from URL'),
                dcc.Input(
                     id='input_name',
                     type='text',
                     placeholder="Indicator Name",
                ),
                dcc.Input(
                     id='input_url',
                     type='url',
                     placeholder="WorldBank data url",
                ),

                html.Button('Check URL', id='chkUrl'),
                html.Div(id='container-button-basic2', children='Enter a value and press submit'),

                 html.H3('Import DSS data Excel'),
                 file_download_link('CBASample.xls'),
                 dcc.Upload(
                     id='upload-DSS',
                     children=html.Div([
                         'Drag and Drop or ',
                         html.A('Select Excel File')
                     ]),
                     style={
                         'width': '80%',
                         'height': '40px',
                         'lineHeight': '60px',
                         'borderWidth': '1px',
                         'borderStyle': 'dashed',
                         'borderRadius': '5px',
                         'textAlign': 'center',
                         'margin': '10px'
                     },
                     # Allow multiple files to be uploaded
                     multiple=False
                 ),
                 html.Div(id='output-data-upload-DSS'),

                 ])
                 ], className='ten columns offset-by-one')
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df=pd.DataFrame()
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=';')
            print(df)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise Exception()

        df.to_csv('WorldDataBankData.csv', mode='a', index=False, sep=';', header=False)

        return html.Div([
            'The file ' + filename + ' processed successfully'
        ])

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

'''    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])'''


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(
    dash.dependencies.Output('container-button-basic2', 'children'),
    [dash.dependencies.Input('chkUrl', 'n_clicks')],
    [dash.dependencies.State('input_url', 'value'),
    dash.dependencies.State('input_name', 'value')])
def update_output(n_clicks, url,name):
    if name=='':
        return 'The Data need an Indicator name'
    try:
        dfx = readWorldDataUrl(url,name)
        return 'The data imported successfully'
    except:
       return 'The URL does not contain data from World Bank or bad format'

'''
@app.callback(
    dash.dependencies.Output('container-button-basic1', 'children'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename'),
         State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children'''

'''def update_output(n_clicks, url,name):
    try:
        data = pd.read_csv(, ';')
        data.to_csv('WorldDataBankData.csv', mode='a', index=False, sep=';', header=False)
        return 'The data imported successfully'
    except:
       return 'The CSV format does not match'
'''
if __name__ == '__main__':
    app.run_server(debug=True)