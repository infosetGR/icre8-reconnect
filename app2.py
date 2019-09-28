# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import overview
import correlationanalysis
import mapanalysis

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


dcc.Link(
    "Overview",
    href="/Reconnect/overview",
    className="tab first",
),
dcc.Link(
    "Descriptive Analysis",
    href="/Reconnect/Data-Analysis",
    className="tab",
),
dcc.Link(
    "Corelation Analysis",
    href="/Reconnect/Corelation-analysis",
    className="tab",
),
dcc.Link(
    "DSS scenarios", href="/Reconnect/DSS-scenarios", className="tab"
),

dcc.Link(
    "Overview",
    href="/Reconnect/Overview",
    className="tab first",
),
dcc.Link(
    "Descriptive Analysis",
    href="/Reconnect/Descriptive-Analysis",
    className="tab",
),
dcc.Link(
    "Correlation Analysis",
    href="/Reconnect/Correlation-analysis",
    className="tab",
),
dcc.Link(
    "Map Analysis",
    href="/Reconnect/Map-Analysis",
    className="tab",
),
dcc.Link(
    "DSS scenarios", href="/Reconnect/DSS-scenarios", className="tab"
),


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/Reconnect/Overview":
        return overview.create_layout(app)
    elif pathname == "/Reconnect/Descriptive-Analysis":
        #return overview.create_layout(app)
        pass
    elif pathname == "/Reconnect/Correlation-analysis":
        return correlationanalysis.create_layout(app)
    elif pathname == "/Reconnect/Map-Analysis":
        return mapanalysis.create_layout(app)
    elif pathname == "/Reconnect/full-view":
        return (
            mapanalysis.create_layout(app),
            correlationanalysis.create_layout(app),
            overview.create_layout(app),
        )
    else:
        return overview.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
