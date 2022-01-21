import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly_express as px
import webbrowser
import dash_table as dt
import base64

Data = pd.read_pickle('1_2_Full_Dataset.plk')
location_data=pd.read_pickle('Location_Data_1_2.plk')
test_matrix = pd.read_pickle('Test_Matrix.plk')
test_matrix['Flowrate (SCFH)']=round(test_matrix['Flowrate (SCFH)'])
test_matrix['Temperature (C)']=round(test_matrix['Temperature (C)'])

test_matrix.loc[test_matrix['Temperature (C)'] < -10, 'Temperature (C)'] = 'N/A'

location_data = location_data.T.reset_index(drop=True).T


first_floor = location_data.where(location_data[9] == 1)
second_floor = location_data.where(location_data[9] == 2)
first_floor[7]=first_floor[7]-250


location_data=pd.concat([first_floor,second_floor])




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

Value_1 = Value.str.split("-", n = 4, expand = True)
Value_1 = Value_1.iloc[1:-1,:]

series = Value_1.iloc[:,0]
series = series.drop_duplicates()
series.sort_values(inplace = True)
test = Value_1.iloc[:,1]
test = test.drop_duplicates()
test.sort_values(inplace = True)
sensor = Value_1.iloc[:,2]
sensor = sensor.drop_duplicates()
sensor.sort_values(inplace = True)
location = Value_1.iloc[:,3]
location = location.drop_duplicates()
location.sort_values(inplace = True)
type = Value_1.iloc[:,4]
type = type.drop_duplicates()
type.sort_values(inplace = True)
def dictionary(data_in):
    b=[]
    for i in data_in:
        i = str(i)
        dict_mid = dict({'label': i, 'value': i})
        b.append(dict_mid)
    return b

def series_dictionary(data_in):
    b=[]
    print(data_in)
    data_in=data_in.iloc[:-1]
    for i in data_in:
        k=int(i)
        if k>=6:
            j='Phase II - '+str(i)
        else:
            j='Phase I - '+str(i)
        i = str(i)
        dict_mid = dict({'label': j, 'value': i})
        b.append(dict_mid)
    return b

series=series_dictionary(series)
test=dictionary(test)
sensor=dictionary(sensor)
location=dictionary(location)
type=dictionary(type)


app = dash.Dash(__name__)


encoded_image = base64.b64encode(open('logo2.png', 'rb').read())
encoded_image_2 = base64.b64encode(open('logo@2x.png', 'rb').read())

app.layout = html.Div([
    html.Div([

        html.Div([

            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'height':'50%', 'width':'50%','display':'inline-block','align':'center'}),
                html.Img(src='data:image/png;base64,{}'.format(encoded_image_2.decode()),style={'height':'50%', 'width':'50%','display':'inline-block','margin-right': '-4px'}),
                html.P(
                    "Select Test Series:",
                    className="control_label",
                ),
                dcc.Dropdown(
                    id='series-dropdown',
                    options=series,
                    placeholder="Series"
                ),
                html.P(
                    "Select Flowrate:",
                    className="control_label",
                ),
                dcc.Dropdown(
                    id='flowrate-dropdown',
                    placeholder="Flowrate"
                ),
                html.P(
                    "Select Source Type:",
                    className="control_label",
                ),
                dcc.Dropdown(
                    id='diffuser-dropdown',
                    placeholder="Source Type"
                ),
                html.P(
                    "Select Test:",
                    className="control_label",
                ),
                dcc.Dropdown(
                    id='test-dropdown',
                    placeholder="Test"
                ),
                html.P(
                    "Select Elevation:",
                    className="elevation_label",
                ),
                dcc.Dropdown(
                    id='elevation-dropdown',
                    placeholder="Elevation"
                ),
            ],),
            html.Div([
                html.Div([

                    dcc.Graph(
                        id='layout_first-graph',
                                            ),
                ],style = {'display': 'inline-block','width': '90%'}),

                html.Div([
                ],style = {'display': 'inline-block','width': '30%','float':'right'}
                ),
            ],
            ),

            html.Div([
            dcc.Dropdown(
                id='my-dropdown',
                options=a,
                value=[],
                placeholder="Selected Sensors",
                multi=True
            ),
            ],
            ),
        ],style = {'overflow': 'hidden','float':'left','width': '27%','box-shadow': '5px 5px 7px 2px #888888','display': 'inline-block','padding': '10px','border-radius': '10px'},),

        html.Div(

            style = {'overflow': 'hidden','float':'right','width': '70%','box-shadow': '5px 5px 7px 2px #888888','display': 'inline-block','padding': '10px','border-radius': '10px'},
                children=[
            html.Div([

                dcc.Graph(id='my-graph'),
            ],
            ),
        ],
        ),
        html.Div(

        style = {'overflow': 'hidden','float':'right','width': '70%','box-shadow': '5px 5px 7px 2px #888888','display': 'inline-block','padding': '10px','border-radius': '10px'},
            children=[
            dcc.Graph(id='my-histogram'),
            html.P(
                "Select Threshold:",
                className="control_label",
            ),
                dcc.Slider(
                    id='threshold-slider',
                    min=0,
                    max=50,
                    step=5,
                    value=5,
                    marks={
                        5: '5',
                        10: '10',
                        15: '15',
                        20: '20',
                        25: '25',
                        30: '30',
                        35: '35',
                        40: '40',
                        45: '45',
                        50: '50'}

                ),
            html.P(
                "Select Bin Size:",
                className="control_label",
            ),
            dcc.Slider(
                id='histo-slider',
                min=1,
                max=10,
                step=1,
                value=5,
                marks={
                    1: '1',
                    2: '2',
                    3: '3',
                    4: '4',
                    5: '5',
                    6: '6',
                    7: '7',
                    8: '8',
                    9: '9',
                    10: '10'}

            ),
            html.P(
                "Test Information:",
                className="control_label",
            ),
                html.Div(style = {'width': '80%','margin-left': 'auto','margin-right': 'auto'},
                    children=[
                    dt.DataTable(
                        id='table',
                        columns=[
                        {'name': 'Series-Test', 'id': 'Name'},
                        {'name': 'Date', 'id': 'Date'},
                        {'name': 'Duration (min)', 'id': 'Duration (min)'},
                        {'name': 'Source Type', 'id': 'Source Type'},
                        {'name': 'Flowrate (SCFH)', 'id': 'Flowrate (SCFH)'},
                        {'name': 'Temperature (C)', 'id': 'Temperature (C)'},
                        {'name': 'Relative Humidity (%RH)', 'id': 'Relative Humidity (%RH)'},
                        {'name': 'HVAC', 'id': 'HVAC'}],
                        style_cell={'textAlign': 'center'}
                    ),
                ],
                ),
        ],
            ),




    ],className="row")
],)


webbrowser.open('http://127.0.0.1:8050/')





@app.callback(Output('flowrate-dropdown', 'options'), [Input('series-dropdown', 'value')])
def update_drop_flow(value):
    b = []
    value = str(value)
    data = test_matrix.loc[test_matrix['Series'] == int(value)]
    data=data.iloc[:,7]
    data=round(data)
    data=data.sort_values()
    data.drop_duplicates(inplace=True)
    for i in data:
        i = str(i)
        dict_mid = dict({'label': i, 'value': i})
        b.append(dict_mid)
    return b

@app.callback(Output('diffuser-dropdown', 'options'), [Input('series-dropdown', 'value'),Input('flowrate-dropdown','value')])
def update_drop_diffuser(value,flow):
    b = []
    value = str(value)
    data = test_matrix.loc[test_matrix['Series'] == int(value)]
    data = data.loc[data['Flowrate (SCFH)'] == float(flow)]
    data=data.iloc[:,6]

    data.drop_duplicates(inplace=True)
    for i in data:
        i = str(i)
        dict_mid = dict({'label': i, 'value': i})
        b.append(dict_mid)

    return b

@app.callback(Output('test-dropdown', 'options'), [Input('series-dropdown', 'value'),Input('flowrate-dropdown', 'value'),Input('diffuser-dropdown', 'value')])
def update_drop_test(value,flow,diffuse):
    b = []
    value = str(value)
    data = test_matrix.loc[test_matrix['Series'] == int(value)]
    print(data)
    data = data.loc[data['Flowrate (SCFH)'] == float(flow)]
    data = data.loc[data['Source Type'] == diffuse]
    data=data.iloc[:,2]
    data.drop_duplicates(inplace=True)
    data = data.sort_values()
    data = '0' + data.astype(str)
    data = data.str.slice(start=-2)

    for i in data:

        i = str(i)
        dict_mid = dict({'label': i, 'value': i})
        b.append(dict_mid)

    return b





@app.callback(Output('elevation-dropdown', 'options'), [Input('test-dropdown', 'value'),Input('series-dropdown', 'value')])
def update_elevation(value_test,value_series):
    b = []
    data = location_data.loc[location_data[0] == value_series]
    data[1] = '0' + data[1].astype(str)
    data[1] = data[1].str[1:]
    data = data.loc[data[1] == value_test]
    data = data.loc[data[4] == 'MB']
    data=data.iloc[:,8]
    data = data.drop_duplicates()
    data=data.sort_values(ascending=False)

    for i in data:
        i = str(i)
        dict_mid = dict({'label': i, 'value': i})
        b.append(dict_mid)
    print(b)
    return b


@app.callback(Output('my-dropdown', 'value'),
              [Input('layout_first-graph', 'clickData')],[State('my-dropdown', 'value')]
              )
def string_gen(sensor,previous):
    sensor_data=sensor['points']
    for dict in sensor_data:
        mid=dict['hovertext']
        previous.append(mid)
    return previous





@app.callback(Output('layout_first-graph', 'figure'),[Input('elevation-dropdown', 'value'),Input('test-dropdown', 'value'),Input('series-dropdown', 'value')])
def update_selection_graph(elevation_value,value_test, value_series):
    data = location_data.loc[location_data[0] == value_series]
    data_1 = data.loc[data[1] == value_test]
    data = data_1.loc[data_1[8] == float(elevation_value)]
    data = data.iloc[:,4:]
    data.columns=['Type','Sensor','Y','X','Z','Level']
    fig = px.scatter(data, x='X', y='Y',hover_name="Sensor",range_y=[-20,500.75],range_x=[ 254.75,-20] )
    fig.update_layout(xaxis=dict(range=[275, -275]))
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
            x0=-5,
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
            x0=-5,
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
            x0=-250,
            y0=0,
            x1=-250,
            y1=482.75,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=-15,
            y0=0,
            x1=-15,
            y1=482.75,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=-15,
            y0=482.75,
            x1=-250,
            y1=482.75,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=-15,
            y0=0,
            x1=-250,
            y1=0,
            line=dict(
                color="Black",
                width=2
            )
        )),
    fig.add_shape(
        dict(
            type="line",
            x0=-5,
            y0=96.25,
            x1=88,
            y1=96.25,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=-250,
            y0=96.25,
            x1=-170,
            y1=96.25,
            line=dict(
                color="Black",
                width=2
            )
        ))
    fig.add_shape(
        dict(
            type="line",
            x0=-170,
            y0=0,
            x1=-170,
            y1=96.25,
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
    Alpha = Alpha.dropna(how='all')
    Size = len(Alpha)
    df = Data.iloc[:Size, :]

    fig = px.scatter(df, x='Time', y=selected_dropdown_value,title="Sensor Measurement")
    fig.update_traces(marker=dict(size=3))
    fig.update_layout(legend_title_text='Sensor')
    fig.update_layout(xaxis_title_text='Time (min)')
    fig.update_layout(yaxis_title_text='Concentration (% LEL)')

    return fig






@app.callback(Output('table', 'data'), [Input('my-dropdown', 'value')])
def update_table(selected_dropdown_value):
    a=[]
    data=selected_dropdown_value
    for i in data:
        ID=i[: 5]
        a.append(ID)

    live_matrix=test_matrix[test_matrix['Name'].isin(a)]
    print(live_matrix)
    live_matrix=live_matrix.iloc[:,[0,3,5,6,7,8,9,10]]
    live_matrix=live_matrix.round(2)
    return live_matrix.to_dict('records')

@app.callback(Output('my-histogram','figure' ), [Input('my-dropdown', 'value'),Input('threshold-slider','value'),Input('histo-slider','value')])
def update_histogram(selected_dropdown_value,thresh,bin_size):
    beta = [w[:5] for w in selected_dropdown_value]
    beta = pd.Series(beta)
    beta = beta.drop_duplicates()
    beta = beta.tolist()
    data = Data
    time = data['Time']
    data = data.filter(like='MB')

    column_slice = []
    for column in data.columns:
        column_mid = column[:5]
        column_slice.append(column_mid)

    data.columns = column_slice
    data_bin = pd.DataFrame()
    for test_series in beta:
        data_mid = data[test_series]
        data_mid = data_mid.T
        data_mid.reset_index(inplace=True, drop=True)
        data_mid = data_mid.T
        Alpha = data_mid.dropna(how='all')
        Size = len(Alpha)

        data_mid = data_mid.where(data_mid > thresh, 0)
        data_mid = data_mid.where(data_mid <= thresh, 1)

        middle_test = data_mid
        summation = data_mid.cumsum()
        summation = summation.astype(bool).astype(int)
        data_mid['sum'] = summation.sum(axis=1)
        data_mid['Time'] = time
        data_mid = data_mid.iloc[:Size, :]
        print(data_mid)
        data_mid['Test'] = test_series
        data_out = data_mid.loc[:, ['Time', 'sum', 'Test']]

        data_bin = pd.concat([data_bin, data_out])

    data_time = data_bin['Time']



    timeframe = [x / 1.0 for x in range(0, round(max(data_time)), bin_size)]

    data_bin = data_bin[data_bin['Time'].isin(timeframe)]

    fig = px.bar(data_bin, x='Time', y='sum',color='Test',barmode='group',title="Cumulative Sensor Alarms")
    fig.update_layout(legend_title_text='Series-Test')
    fig.update_layout(xaxis_title_text='Time (min)')
    fig.update_layout(yaxis_title_text='Sensor Alarm Count')
    return fig




if __name__ == '__main__':
    app.run_server()
