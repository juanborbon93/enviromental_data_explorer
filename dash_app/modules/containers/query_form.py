import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from ..components.query.categorical_query import categorical_query
from ..components.query.numeric_query import numeric_query
from ..components.query.date_query import date_query
from ..data_tools import get_type_dict, get_parser
from dash.dependencies import Input, Output, State,MATCH,ALL
from dash_extensions import Download
import json
from ..data_tools import filter_data
import os
from ..app import app

datatype_query_map = {
    "date":date_query,
    "string":categorical_query,
    "numeric":numeric_query
}

def query_form(columns,dataset_path,dataset_info):
    parser = get_parser(dataset_path)
    df = parser(dataset_path,nrows=50)
    type_dict = dataset_info["column_types"] #get_type_dict(df)
    col_analysis = dataset_info["col_analysis"]
    col_query_map = {col:datatype_query_map.get(type_dict[col]) for col in columns}
    # form_fields = [query(col,dataset_path) for col,query in col_query_map.items()]
    form_fields = []
    for col,query in col_query_map.items():
        query_config = col_analysis.get(col)
        form_fields.append(
            query(col,query_config)
        )
    # submit_btn = dbc.Button("Submit",id="submit-query",block=True,style={"margin-top":"1rem"})
    # download = Download(id="download")
    # download_element = dcc.Loading([submit_btn,download],style={"margin-top":"1rem"})
    return form_fields#+[download_element]

    

@app.callback(
    Output("download","data"),
    Input("submit-query","n_clicks"),
    [
        State("dataset-path",'value'),
        State({"type":"date-range-query-params","index":ALL},"data"),
        State({"type":"numeric-query-params","index":ALL},"data"),
        State({"type":"categorical-query-params","index":ALL},"data"),
        State("latitude","value"),
        State("longitude","value"),
        State("radius","value"),
        State("distance-unit","value"),
    ]
)
def submit_query(n_clicks,dataset_path,date_queries,numeric_queries,categorical_queries,latitude,longitude,radius,unit):
    if n_clicks:
        queries = {}
        for query_group in [date_queries,numeric_queries,categorical_queries]:
            for q in query_group:
                col_name = q['col']
                params = q['query']
                queries[col_name] =  params
        print(queries)
        df = filter_data(dataset_path,latitude,longitude,radius,unit,queries)
        csv_str = df.to_csv()
        original_file_name = os.path.splitext(os.path.basename(dataset_path))[0]
        return {"content":csv_str,"filename":f"FILTERED_{original_file_name}.csv"}