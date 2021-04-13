import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from ..app import app
from dash.dependencies import Input, Output, State


file_selector = html.Div(
    [
        html.H3("Input dataset:"),
        dbc.Input(id="dataset-path", placeholder="Dataset file path...", type="text")
    ],
    style={"margin-top":"1rem"}
)
