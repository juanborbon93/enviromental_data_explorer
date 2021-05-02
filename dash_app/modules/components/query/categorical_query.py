import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, MATCH
from ...data_tools import get_categories
from ...app import app

# categorical_query = html.Div("categorical query")

def categorical_query(col_name,col_params=None):
    if col_params:
        options = col_params
    else:
        options = get_categories(dataset_path,col_name)
    form = dcc.Dropdown(
            options = [{"label":option,"value":option} for option in options],
            multi=True,
            id = {"type":"categorical-query","index":col_name}
        )
    return html.Div(
        [
            html.H4(col_name),
            form,
            dcc.Store(
                id = {"type":"categorical-query-params","index":col_name},
                data = {
                    "col":col_name,
                    "type":"string",
                    "query":[] 
                }
            )
        ]
    )


@app.callback(
    Output({"type":"categorical-query-params","index":MATCH},"data"),
    [
        Input({"type":"categorical-query","index":MATCH},"value")
    ],
    State({"type":"categorical-query-params","index":MATCH},"data")
)
def record_date(selections,data):
    if selections: 
        data["query"] = selections
    return data