import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import webbrowser
import dash_table as dt



Data=pd.read_pickle('Full_Dataset.pkl')
location_data=pd.read_pickle('Location_Data.plk')
test_matrix=pd.read_pickle('Test_Matrix.plk')
location_data = location_data.T.reset_index(drop=True).T

print(test_matrix)
elevation=location_data.iloc[:,8]
elevation=elevation.drop_duplicates()
elevation.sort_values(inplace = True,ascending=False)
elevation.reset_index(drop=True, inplace=True)
elevation=elevation.drop_duplicates()
#elevation=elevation.astype(str)
index_values=elevation.index.astype(int)
elevation=elevation.to_list()

marks={}
for i in index_values:
    marks_mid={i  : str(elevation[i])}
    marks.update(marks_mid)
a = []
Value = Data.columns
Value = pd.Series(Value[:])

for i in Value:
    dict_mid = dict({'label': i, 'value': i})
    a.append(dict_mid)

Value_1=Value.str.split("-", n = 4, expand = True)
Value_1=Value_1.iloc[1:-1,:]

series=Value_1.iloc[:,0]
series=series.drop_duplicates()
series.sort_values(inplace = True)
test=Value_1.iloc[:,1]
test=test.drop_duplicates()
test.sort_values(inplace = True)
sensor=Value_1.iloc[:,2]
sensor=sensor.drop_duplicates()
sensor.sort_values(inplace = True)
location=Value_1.iloc[:,3]
location=location.drop_duplicates()
location.sort_values(inplace = True)
type=Value_1.iloc[:,4]
type=type.drop_duplicates()
type.sort_values(inplace = True)
def dictionary(data_in):
    b=[]
    for i in data_in:
        i=str(i)
        dict_mid = dict({'label': i, 'value': i})
        b.append(dict_mid)
    return b

series=dictionary(series)
test=dictionary(test)
sensor=dictionary(sensor)
location=dictionary(location)
type=dictionary(type)

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h")
    )


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Fire & Risk Alliance",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Natural Gas Dispersion", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="two column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    "Filter By Series:",
                                    className="control_label",
                                ),
                                dcc.Dropdown(
                                    id='series-dropdown',
                                    options=series,
                                    placeholder="Series",
                                    className = "dcc_control"
                                ),
                                html.P("Select Test:", className="control_label"),
                                dcc.Dropdown(
                                    id='test-dropdown',
                                    placeholder="Test",
                                    className = "dcc_control"
                                ),
                               dcc.Slider(
                                   id='slider',
                                   min=0,
                                   step=None,
                                   value=5,
                                   vertical='True',
                                   className="dcc_control"

                               ),
                            dcc.Graph(id='layout_first-graph'
                                ),
                                        dt.DataTable(
                                            id='table',
                                            columns=[
                                                {'name': 'Name', 'id': 'Name'},
                                                {'name': 'Date', 'id': 'Date'},
                                                {'name': 'Duration (min)', 'id': 'Duration (min)'},
                                                {'name': 'Source Type', 'id': 'Source Type'},
                                                {'name': 'Flowrate (SCFH)', 'id': 'Flowrate (SCFH)'},
                                                {'name': 'Temperature (C)', 'id': 'Temperature (C)'},
                                                {'name': 'Relative Humidity (%RH)', 'id': 'Relative Humidity (%RH)'}],
                                            style_cell={'textAlign': 'center'}
                                        ),
                            ],
                            className="one columns",
                            id="cross-filter-options"),
                        ],
                        className="row flex-display",
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id='my-graph')],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="two columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


webbrowser.open('http://127.0.0.1:8050/')



@app.callback(Output('test-dropdown', 'options'), [Input('series-dropdown', 'value')])
def update_drop(value):
    b = []
    value=str(value)
    data = location_data.loc[location_data[0] == value]
    data=data.iloc[:,1]
    data.drop_duplicates(inplace=True)
    for i in data:
        i = str(i)
        dict_mid = dict({'label': i, 'value': i})
        b.append(dict_mid)
    return b



@app.callback([Output('slider', 'marks'),Output('slider', 'max')], [Input('test-dropdown', 'value')],[State('series-dropdown', 'value')])
def update_slider(value_test,value_series):
    data = location_data.loc[location_data[0] == value_series]
    data = data.loc[data[1] == value_test]
    data = data.loc[data[4] == 'MB']
    data=data.iloc[:,8]
    data = data.drop_duplicates()
    data=data.sort_values(ascending=False)

    marks={}
    for i in data:
        marks_mid = {float(i): str(i)}
        marks.update(marks_mid)

    return marks, max(marks)


@app.callback(Output('my-dropdown', 'value'),
              [Input('layout_first-graph', 'clickData')],[State('my-dropdown', 'value')]
              )
def string_gen(sensor,previous):
    sensor_data=sensor['points']
    for dict in sensor_data:
        mid=dict['hovertext']
        previous.append(mid)
    return previous





@app.callback(Output('layout_first-graph', 'figure'),[Input('slider', 'value'),Input('test-dropdown', 'value')],[State('series-dropdown', 'value')])
def update_graph(slider_value,value_test, value_series):
    data = location_data.loc[location_data[0] == value_series]
    data_1 = data.loc[data[1] == value_test]
    data = data_1.loc[data_1[8] == slider_value]
    data = data.iloc[:,4:]
    data.columns=['Type','Sensor','Y','X','Z','Level']
    print(data_1)
    fig = px.scatter(data, x='X', y='Y',hover_name="Sensor",range_y=[-20,500.75],range_x=[ 254.75,-20] )
    data_1 = data_1.loc[data_1[4] == 'FL']
    data_1 = data_1.iloc[:,5:]
    data_1.columns = [ 'Sensor', 'Y', 'X', 'Z', 'Level']
    fig2=px.scatter(data_1, x='X', y='Y',color_discrete_sequence=["red"])
    fig2.update_traces(dict(hoverinfo='skip',hovertemplate=None))
    fig.add_trace(fig2.data[0])
    fig.add_shape(
        dict(
            type="line",
            x0=88,
            y0=0,
            x1=88,
            y1=330,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=88,
            y0=330,
            x1=240,
            y1=330,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=88,
            y0=215,
            x1=240,
            y1=215,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=88,
            y0=150,
            x1=240,
            y1=150,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=240,
            y0=0,
            x1=240,
            y1=0,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=240,
            y0=0,
            x1=240,
            y1=482.75,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=-5,
            y0=0,
            x1=-5,
            y1=482.75,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=0,
            y0=482.75,
            x1=240,
            y1=482.75,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=0,
            y0=0,
            x1=240,
            y1=0,
            line=dict(
                color="Black",
                width=2
            )
        ))

    fig.update_traces(marker=dict(size=8))


    return fig
B=[]
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    Alpha = Data[selected_dropdown_value]
    Alpha = Alpha.dropna()
    Size = len(Alpha)
    df = Data.iloc[:Size, :]

    fig = px.scatter(df, x='Time', y=selected_dropdown_value)
    return fig


@app.callback(Output('table', 'data'), [Input('my-dropdown', 'value')])
def update_table(selected_dropdown_value):
    a=[]
    data=selected_dropdown_value
    print(data)
    for i in data:
        ID=i[: 5]
        a.append(ID)

    live_matrix=test_matrix[test_matrix['Name'].isin(a)]
    live_matrix=live_matrix.iloc[:,[0,3,5,6,7,8,9]]
    live_matrix=live_matrix.round(2)
    return live_matrix.to_dict('records')


if __name__ == '__main__':
    app.run_server()