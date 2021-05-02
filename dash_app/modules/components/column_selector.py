import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from typing import List
from ..app import app

def column_selector(options:List[str]):
    children = []
    if len(options)>0:
        dropdown =  dcc.Dropdown(
            options = [{"label":option,"value":option} for option in options],
            multi=True,
            id = "column-selection"
        )
        children = [
            html.H3("Choose columns to filter by:"),
            dropdown
        ]
    return html.Div(children)

    
