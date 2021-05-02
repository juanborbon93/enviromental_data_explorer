import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
from ...app import app 

def numeric_query(col_name,col_params=None):
    if col_params is None:
        col_params = {}
    min_val = col_params.get("min")
    max_val = col_params.get("max")
    if min_val and max_val:
        title = f"{col_name} {min_val} to {max_val}"
    else: 
        title = col_name
    form = dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Min", html_for="min"),
                        dbc.Input(
                            type="number",
                            id={"type":"numeric-query-min","index":col_name},
                            min=min_val,
                            max=max_val
                        ),
                    ]
                ),
                width=6,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Max", html_for="max"),
                        dbc.Input(
                            type="number",
                            id={"type":"numeric-query-max","index":col_name},
                            min=min_val,
                            max=max_val
                        ),
                    ]
                ),
                width=6,
            ),
        ],
        form=True,
    )
    return html.Div(
        [
            html.H4(title),
            form,
            dcc.Store(
                id = {"type":"numeric-query-params","index":col_name},
                data = {
                    "col":col_name,
                    "type":"numeric",
                    "query":{
                        "min":None,
                        "max":None
                    }    
                }
            )
        ]
    )


@app.callback(
    Output({"type":"numeric-query-params","index":MATCH},"data"),
    [
        Input({"type":"numeric-query-min","index":MATCH},"value"),
        Input({"type":"numeric-query-max","index":MATCH},"value")
    ],
    State({"type":"numeric-query-params","index":MATCH},"data")
)
def record_date(start_date,end_date,data):
    state =  {
        "min":start_date,
        "max":end_date
    }
    data["query"] = state
    return data