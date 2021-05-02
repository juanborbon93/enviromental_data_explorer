import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from .query_form import query_form
from ..components.file_selector import file_selector
from ..components.column_selector import column_selector
from ..components.query.location_query import location_query
from dash.dependencies import Input, Output, State
from ..app import app
from ..data_tools import get_cols,analyze_cols
from dash_extensions import Download
import os
import re

logo  = "https://l2enviro.com/wp-content/uploads/2019/03/L2ENVIROSOLUTIONS_logo_final_individual-blue-06-252x300.png"
print(logo)
def home():
    navbar = dbc.Navbar(
        dbc.Row(
            [
                dbc.Col(html.Img(src=logo,height="90px",style={"filter":"invert(100%) contrast(100)","margin-bottom":"10px"})),
                dbc.Col(dbc.NavbarBrand("L2 Enviro Dataset Navigator",className="ml-2"),align="center")
            ]
        ),
        color="dark",
        dark=True
    )

    return html.Div([
        navbar,
        html.Div(
            dbc.Row(
                dbc.Col(
                    [
                        file_selector,
                        dcc.Store(id='dataset-info',data = {}),
                        html.Div(id="location-query-div"),
                        dcc.Loading(id='column-selection-div',style={"margin-top":"200px"}),
                        html.Div(id="query-form-div")
                    ],
                    width=10
                ),
                justify="center"
            )
        ),
        html.Div(id="modal")
    ])
    

@app.callback(
    [
        Output("column-selection-div","children"),
        Output("location-query-div","children"),
        Output("dataset-info","data")
    ],
    Input("dataset-path",'value'),
    State('dataset-info','data')
)
def file_actions(dataset_path,dataset_data):
    if dataset_path:
        if os.path.isfile(dataset_path) and len(re.findall(".(csv|xlsx)$",dataset_path))==1:
            if dataset_path not in dataset_data:
                print(f"analyzing {dataset_path}")
                cols = get_cols(dataset_path)
                col_analysis,type_dict = analyze_cols(dataset_path)
                dataset_data[dataset_path] = {
                    "column_types":type_dict,
                    "col_analysis":col_analysis
                }
                cols = [c for c in cols if c in list(col_analysis.keys())]
            return column_selector(cols),location_query(),dataset_data
    else:
        return None,None,dataset_data


@app.callback(
    Output("query-form-div","children"),
    Input("column-selection",'value'),
    [
        State("dataset-path",'value'),
        State("dataset-info","data")    
    ]
)
def show_query_form(columns,dataset_path,dataset_data):
    if dataset_path:
        submit_btn = dbc.Button("Submit",id="submit-query",block=True,style={"margin-top":"1rem"})
        download = Download(id="download")
        download_element = dcc.Loading([submit_btn,download],style={"margin-top":"1rem"})
        form = []
        if columns and (dataset_path in dataset_data):
            form =  query_form(columns,dataset_path,dataset_data[dataset_path])
        form.append(download_element)
        return form

