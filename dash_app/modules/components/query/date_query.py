import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State,MATCH
from ...app import app

def date_query(col_name,col_params=None):
    if col_params is None:
        col_params = {}
    start_date = col_params.get("min")
    end_date = col_params.get("max")
    form = dcc.DatePickerRange(
        id={"type":"date-range-query","index":col_name},
        # min_date_allowed = start_date,
        # max_date_allowed = end_date
        )
    if start_date and end_date:
        title = f"{col_name} {start_date} to {end_date}"
    else: 
        title = col_name
    return html.Div(
        [
            html.H4(title),
            form,
            dcc.Store(
                id={"type":"date-range-query-params","index":col_name},
                data = {
                    "col":col_name,
                    "type":"date",
                    "query":{
                        "min":None,
                        "max":None
                    }
                }  
            )
        ]
    )

@app.callback(
    Output({"type":"date-range-query-params","index":MATCH},"data"),
    [
        Input({"type":"date-range-query","index":MATCH},"start_date"),
        Input({"type":"date-range-query","index":MATCH},"end_date")
    ],
    State({"type":"date-range-query-params","index":MATCH},"data")
)
def record_date(start_date,end_date,data):
    data["query"] =  {
        "min":start_date,
        "max":end_date
    }
    return data




