import dash_html_components as html
import dash_core_components as dcc
import dash
import pandas as pd
import csv


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
    return html.Div([get_header(app), html.Br([]), get_menu(),  html.Br([])])

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
                    html.Img(
                        src='http://www.icre8.eu/images/icre8-logo.png',
                        # src=app.get_asset_url("icre8-logo.png"),
                        className="logo",
                        style={
                            'height': '70px',
                            'float': 'right',
                            'position': 'relative',
                            'padding-top': 0,
                            'padding-right': 0
                        },
                    ),



                ],
            ),
            html.Div(
                [
                    html.Div(
                        [html.H2("RECONNECT DSS Tool ")], className='nine columns'

                    ),
                    html.A(
                        html.Button("Learn More", id="learn-more-button"),
                        href="http://www.icre8.eu/reconnect-interreg", target='_blank'

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
                html.Button("Load Data")
                , href="/LoadData"
            ),

           html.A(
               html.Button("Correlation Analysis"),
                href="/correlationanalysis"


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

def readWorldDataUrl(url,IndicName='-'):
    Indicators = pd.read_csv("WorldDataBankIndicators.csv", ';').to_dict(orient='records')
    name=IndicName
    for row in Indicators:
        if(row['DataURL']==url):
            name=row['Name']
    print('name:'+name)
    data=pd.DataFrame()
    data['Indicator Name']=''
    try:
        data = pd.read_csv('WorldDataBankData.csv', ';')

    except :
        with open('WorldDataBankData.csv', 'w') as csvfile:
           writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=['Year','Country Name',  'Value', 'Indicator Name'])
           writer.writeheader()

    tab_unpivoted = None

    if  not any(data['Indicator Name']== name):
        dfs = pd.read_html(url)
        df = dfs[5].transpose()
        x = df.set_axis(['Year'], axis=1, inplace=False)
        y = dfs[19].transpose()
        y.columns = y.iloc[0]
        y = y.drop(y.index[0])
        tab = pd.concat([x, y], axis=1)
        tab_unpivoted = tab.melt(id_vars=['Year'], var_name='Country Name', value_name='Value')
        tab_unpivoted = tab_unpivoted.dropna(subset=['Year', 'Value'])
        tab_unpivoted = tab_unpivoted[tab_unpivoted.Value != '..']
        tab_unpivoted['Indicator Name'] = name
        print(tab_unpivoted)

        tab_unpivoted.to_csv('WorldDataBankData.csv', mode='a', index=False, sep=';', header=False)
        '''with open('WorldDataBankData.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=['Indicator Name', 'Country Name', 'Year', 'Value'])
            for row in tab_unpivoted.iterrows():

                writer.writerow({'Indicator Name':row['Indicator Name'],'Country Name':row['Country Name'],'Year':row['Year'],'Value':row['Value']})'''

    else:
        tab_unpivoted = data[(data['Indicator Name']==name)]

    return tab_unpivoted


