import dash_html_components as html
from utils import Header, make_dash_table,app


layout= html.Div([ html.Div(
    html.Div([
        html.Div(
            [
                Header(app),
                html.P('Reconnect DSS tool is a system developed from Infoset Ltd for the decision support of RECONNECT (Interreg project). The overall objective of the project is to improve the capacity of local management authorities by promoting efficient '
                       'management of natural resources through the regional approach. The specific objectives include the following: 1. Enrich the current management toolbox with instruments based on the genetic and functional biodiversity; '
                       '2. Identify and map the key marine habitats and evaluate the services they provide by socio-economic, cultural and legal approaches; 3. Engage citizens in environmental monitoring and conservation activities and involve stakeholders '
                       'to boost potential for blue growth; 4. Develop a platform for the data storage and analysis of results based on cutting edge information technologies; 5. Establishment of a Decision Supporting System to enhance the MPAs management on a scientific basis.'),
                html.P('The Decision Supporting System specifically support the user by analyzing data from various sources and presenting them in the appropriate graphical representation in order to show useful insights and assist the decision of the MPAs management. '),
                html.Li('LOAD DATA: This page is used to load data to the application. You can import data from a CSV file or a World Bank data series URL. Both contain various country indicators across time but you can also input any data in the same format. Also here you can upload the configuration file for the DSS tool. This is required in order the calcuations of DSS to be performed and present meaningful results '),
                html.Li('CORRELATION ANALYSIS: Here you can preview a series of timed data for the countries you are interested and also select 2 of different types to examine if there is any correlation between them.'),
                html.Li('DSS TOOL: Is an analysis system for making cost benefit calculations and predictions of given projects on the areas of interest. It requires to input the basic info of costs and revenues per project, category, area and area type and will provide the Cost-Benefit estimates for all project lifecycle'),

            ], className="row"
        ),



    ], className='ten columns offset-by-one'))
])
