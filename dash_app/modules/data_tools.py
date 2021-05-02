import pandas as pd
from haversine import haversine, Unit
from time import time
from datetime import datetime
from dateutil import parser as dateparser
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

parser_dict = {
    "csv":pd.read_csv,
    "xlsx":pd.read_excel
}
def get_cats(series,prev):
    if prev is None:
        prev = []
    new =  list(series.dropna().unique())
    return list(set(new+prev))

def get_num_range(series,prev):
    if prev is None:
        prev = {"min":series.min(),"max":series.max()}
    return {
        "min":min(series.min(),prev["min"]),
        "max":max(series.max(),prev["max"])
    }
def get_date_range(series,prev):
    dates = pd.to_datetime(series)
    if prev is None:
        prev = {"min":dates.min(),"max":dates.max()}
    return{
        "min":min(dates.min(),prev["min"]),
        "max":max(dates.max(),prev["max"])
    }
col_analyzer_map = {
    "date":get_date_range,
    "string":get_cats,
    "numeric":get_num_range
}

def analyze_cols(file_path):
    parser,parse_args = get_parser(file_path)
    df = parser(file_path,nrows=1000,**parse_args)
    type_dict = get_type_dict(df)
    col_analyzers = {col:col_analyzer_map.get(col_type) for col,col_type in type_dict.items()}
    col_analysis = {col:None for col in df.columns}
    unparsed = {col:[] for col in df.columns}
    for index,df_chunk in enumerate(parser(file_path,chunksize=20000,low_memory=False),start=0):
        for col,prev in col_analysis.items():
            analyzer = col_analyzers[col]
            col_series = df_chunk[col]
            try:
                new = analyzer(col_series,prev)
                col_analysis[col]=new
            except:
                new_type_dict = get_type_dict(df_chunk)
                new_col_type = new_type_dict[col]
                if new_col_type != type_dict[col]:
                    new_analyzer = col_analyzer_map.get(new_col_type)
                    try: 
                        new = new_analyzer(col_series,None)
                        col_analysis[col]=new
                        col_analyzers[col] = new_analyzer
                        type_dict[col]=new_col_type
                    except:
                        col_series = df_chunk[col]
                        unparsed[col].append(col_series)
    return col_analysis,type_dict

def get_parser(file_path):
    parser = None
    args = {}
    if file_path.endswith("xlsx"):
        args['engine']="openpyxl"
    for extension in parser_dict:
        if file_path.endswith(extension):
            parser = parser_dict[extension]
    return parser,args

def get_categories(file_path,col_name):
    parser,parse_args = get_parser(file_path)
    df = parser(file_path,usecols=[col_name],**parse_args)
    return list(df[col_name].unique())

def get_cols(file_path):
    parser,parse_args = get_parser(file_path)
    df = parser(file_path,nrows=5,**parse_args)
    return [i for i in df.columns if "latitude"!=i.lower() and "longitude"!=i.lower()]

distance_units = ['m','km','nmi','ft','in','mi']
def numeric_filter(df,col_name,min_val,max_val):
    return df[(df[col_name]<=max_val) & (df[col_name]>=min_val)]
def categorical_filter(df,col_name,filter_options):
    return df[df[col_name].isin(filter_options)]
def date_filter(df,date_col,start_date,end_date):
    if not isinstance(start_date,datetime):
        try:
            start_date = dateparser.parse(start_date)
        except:
            raise Exception(f"Could not parse start date {start_date}")
    if not isinstance(end_date,datetime):
        try:
            end_date = dateparser.parse(end_date)
        except:
            raise Exception(f"Could not parse end date {end_date}")
    matches = []
    failed_parse_count = 0
    dates = pd.to_datetime(df[date_col],infer_datetime_format=True)
    print("query: ",start_date,end_date)
    print("date range: ",dates.min(),dates.max())
    print("all dates: ",set(df[date_col].values))
    return df[(dates>=start_date) & (dates<=end_date) ] 
def get_type_dict(df):
    type_dict = {}
    for t in df.columns:
        col_type = None
        if "date" in t.lower():
            col_type= "date"
        elif is_string_dtype(df[t]):
            col_type= "string"
        elif is_numeric_dtype(df[t]):
            col_type= "numeric"
        type_dict[t]=col_type
    return type_dict

def filter_data(file_path,latitude,longitude,radius,distance_unit,queries,save_as=None):
    t0 = time()
    if distance_unit not in distance_units:
        raise Exception(f"unit: {distance_unit} is not an accepted unit. must be one of: {distance_units}")
    query_coords = (latitude,longitude)
    chunk_size = 10000
    parser,parse_args = get_parser(file_path)
    if parser:
        df = parser(file_path,nrows=chunk_size,**parse_args)
    else:
        raise Exception("file must have a .csv or .xlsx extension")
    result_df = None
    result_df_list = []
    row_count = 0
    for index,df_chunk in enumerate(parser(file_path,chunksize=chunk_size,low_memory=False),start=0):
        if index==0:
            latitude_col = [i for i in df_chunk.columns if "latitude" in i.lower()]
            if len(latitude_col)==1:
                latitude_col = latitude_col[0]
            else:
                raise Exception(f"found {len(latitude_col)} latitude columns")

            longitude_col = [i for i in df_chunk.columns if "longitude" in i.lower()]
            if len(longitude_col)==1:
                longitude_col = longitude_col[0]
            else:
                raise Exception(f"found {len(longitude_col)} longitude columns")
        row_count += len(df_chunk)
        data_coords = list(zip(df_chunk[latitude_col],df_chunk[longitude_col]))
        distance = [haversine(d,query_coords,unit=distance_unit) for d in data_coords]
        df = df_chunk.copy(deep=True)
        df.insert(0,f"Haversine Distance ({distance_unit})",distance)
        df = df[df[f"Haversine Distance ({distance_unit})"]<=radius]
        result_df_list.append(df.copy(deep=True))
    result_df = pd.concat(result_df_list)

    df_type_dict = get_type_dict(result_df)
    for query_col,query_params in queries.items():
        if query_col not in result_df.columns:
            raise Exception(f"{query_col} is not a column")
        col_type = df_type_dict[query_col]
        if col_type == "date":
            result_df = date_filter(result_df,query_col,query_params.get('min'),query_params.get('max'))
        elif col_type == "numeric":
            result_df = numeric_filter(result_df,query_col,query_params.get('min'),query_params.get('max'))
        elif col_type == "string":
            result_df = categorical_filter(result_df,query_col,query_params)
    tf = time()
    print("rows processed: ",row_count)
    print(f"processing time: {tf-t0} seconds")
    if save_as:
        result_df.to_csv(save_as)
        print(f"saved to {save_as}")
    return result_df
