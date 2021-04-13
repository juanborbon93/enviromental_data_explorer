import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
from ...app import app 

def location_query():
    form = dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Latitude", html_for="Latitude"),
                        dbc.Input(
                            type="number",
                            id="latitude",
                            value=30.0
                        ),
                    ]
                ),
                width=6,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Longitude", html_for="Longitude"),
                        dbc.Input(
                            type="number",
                            id="longitude",
                            value=-90.0
                        ),
                    ]
                ),
                width=6,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Radius", html_for="Radius"),
                        dbc.Input(
                            type="number",
                            id="radius",
                            value = 300
                        ),
                    ]
                ),
                width=6,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Unit", html_for="Unit"),
                        dcc.Dropdown(
                            options = [{"label":option,"value":option} for option in ['m','km','nmi','ft','in','mi']],
                            id = "distance-unit",
                            value="mi"
                        )
                    ]
                ),
                width=6,
            ),

        ],
        form=True,
    )
    return html.Div(
        [
            html.H4("Search Location:"),
            form,
            dcc.Store(
                id = 'location-query'
            )
        ]
    )


# @app.callback(
#     Output('location-query',"data"),
#     [
#         Input("latitude","value"),
#         Input("longitude","value"),
#         Input("radius","value"),
#         Input("distance-unit","value"),
#     ],
# )
# def record_date(latitude,longitude,radius,unit):
#     state =  {
#         "latitude":latitude,
#         "longitude":longitude,
#         "radius":radius,
#         "unit":unit
#     }
#     return state