import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import sqlite3
import plotly.graph_objs as go
# Directory where your database files are located
DATA_DIR = r'./'

# Function to get the list of tool numbers from the directory
def get_tool_numbers(data_dir):
    tool_numbers = []
    for filename in os.listdir(data_dir):
        if filename.startswith('Tool_') and filename.endswith('.db'):
            tool_number = filename.split('_')[1].split('.')[0]
            tool_numbers.append(tool_number)
    return tool_numbers

def load_coarse_data(tool_number):
    file_path = os.path.join(DATA_DIR, f'Tool_{tool_number}.db')
    if os.path.exists(file_path):
        # Load data from the database file
        conn = sqlite3.connect(file_path)
        query = """
        SELECT
            *
        FROM Coarse_Data
        ORDER BY "Time" DESC
        LIMIT 60000
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if the DB does not exist


# Function to load data from a specific tool's database file
def load_tad_data(tool_number):
    file_path = os.path.join(DATA_DIR, f'Tool_{tool_number}.db')
    if os.path.exists(file_path):
        # Load data from the database file
        conn = sqlite3.connect(file_path)
        query = "SELECT * FROM Tad_Data"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if the DB does not exist

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get the list of tool numbers
tool_numbers = get_tool_numbers(DATA_DIR)

# Define the layout of the app
app.layout = dbc.Tabs([
    dbc.Tab(
        label='Home Page',
        children=[
            dbc.Container([
                html.Div([
                    html.H1("Created By:", 
                            style={
                                'textAlign': 'center', 
                                'fontSize': '24px', 
                                'fontFamily': 'serif'
                            }),
                    html.H2("X", 
                            style={
                                'textAlign': 'center', 
                                'fontSize': '48px', 
                                'fontWeight': 'bold',
                                'fontFamily': 'serif',
                                'textShadow': '2px 1px 4px #888888'
                            }),
                    html.Br(),  # Adds a line break
                    html.H3("Special Thanks to:", 
                            style={
                                'textAlign': 'center', 
                                'fontSize': '24px', 
                                'fontFamily': 'serif'
                            }),
                    html.H4("Y, Z, T", 
                            style={
                                'textAlign': 'center', 
                                'fontSize': '24px', 
                                'fontWeight': 'bold',
                                'fontFamily': 'serif',
                                'textShadow': '2px 1px 4px #888888'
                            }),
                ], style={'height': '100vh', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})
            ], fluid=True)
        ]
    ),
    dbc.Tab(
        label='Coarse-Pixel',
        children=[
            dbc.Container([
                html.H1("Coarse Pixel Viewer"),

                html.Div([
                    html.Label("Select Tool Number:"),
                    dcc.Dropdown(
                        id='tool-number-dropdown',
                        options=[{'label': str(tool), 'value': tool} for tool in tool_numbers],
                        value=tool_numbers[0] if tool_numbers else None,
                        style={'width': '150px'}
                    ),
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-x-pass-fail',
                        placeholder="Select X Pass/Fail",
                        multi=True
                    )
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-y-pass-fail',
                        placeholder="Select Y Pass/Fail",
                        multi=True
                    )
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-time',
                        placeholder="Select Time",
                        multi=True
                    )
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-lot',
                        placeholder="Select Lot Name",
                        multi=True
                    )
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-xdie',
                        placeholder="Select X Die",
                        multi=True
                    )
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-ydie',
                        placeholder="Select Y Die",
                        multi=True
                    )
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-static-iteration',
                        placeholder="Select Static Iteration",
                        multi=True
                    )
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-orientation',
                        placeholder="Select Orientation",
                        multi=True
                    )
                ], style={'marginBottom': 0}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-site-serial-number',
                        placeholder="Select Site Serial Number",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Hr(style={'border':'5px solid #000'}),

                dcc.Graph(id='scatter-plot'),

                html.Hr(style={'border':'5px solid #000'}),

                dcc.Graph(id='x-vs-time-plot'),

                html.Hr(style={'border':'5px solid #000'}),

                dcc.Graph(id='y-vs-time-plot'),

                html.Hr(style={'border':'5px solid #000'}),

                html.Div(id='table-container')
            ], fluid=True)
        ]
    ),
    dbc.Tab(
        label='Tad-Converge',
        children=[
            dbc.Container([
                html.H1("Tad Converge Viewer"),

                html.Div([
                    html.Label("Select Tool Number:"),
                    dcc.Dropdown(
                        id='tool-number-dropdown_tad',
                        options=[{'label': str(tool), 'value': tool} for tool in tool_numbers],
                        value=tool_numbers[0] if tool_numbers else None,
                        style={'width': '150px'}
                    ),
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-time_tad',
                        placeholder="Select Time",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-recipe',
                        placeholder="Select Recipe",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-lot_tad',
                        placeholder="Select Lot",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-phase',
                        placeholder="Select Phase",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-site-serial-number_tad',
                        placeholder="Select Site Serial Number",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-die-x',
                        placeholder="Select Die X",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-die-y',
                        placeholder="Select Die Y",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-misreg-x',
                        placeholder="Select Misreg X",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-misreg-y',
                        placeholder="Select Misreg Y",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-tis-x',
                        placeholder="Select TIS X",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-tis-y',
                        placeholder="Select TIS Y",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-dad-pos-x',
                        placeholder="Select DAD Pos X",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-dad-pos-y',
                        placeholder="Select DAD Pos Y",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-slope-x',
                        placeholder="Select Slope X",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-slope-y',
                        placeholder="Select Slope Y",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-b-x',
                        placeholder="Select B X",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-b-y',
                        placeholder="Select B Y",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-exit-reason',
                        placeholder="Select Exit Reason",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Div([
                    dcc.Dropdown(
                        id='filter-stats',
                        placeholder="Select Stats",
                        multi=True
                    )
                ], style={'marginBottom': 10}),

                html.Hr(style={'border': '5px solid #000'}),

                dcc.Graph(id='tis-x-vs-dad-x-plot'),

                html.Hr(style={'border': '5px solid #000'}),

                dcc.Graph(id='tis-y-vs-dad-y-plot'),

                html.Hr(style={'border': '5px solid #000'}),

                html.Div(id='table-container_tad')
            ], fluid=True)
        ]
    )
])



@app.callback(
    [Output('filter-x-pass-fail', 'options'),
     Output('filter-y-pass-fail', 'options'),
     Output('filter-time', 'options'),
     Output('filter-lot', 'options'),
     Output('filter-xdie', 'options'),
     Output('filter-ydie', 'options'),
     Output('filter-static-iteration', 'options'),
     Output('filter-orientation', 'options'),
     Output('filter-site-serial-number', 'options')],
    [Input('tool-number-dropdown', 'value'),
     Input('filter-x-pass-fail', 'value'),
     Input('filter-y-pass-fail', 'value'),
     Input('filter-time', 'value'),
     Input('filter-lot', 'value'),
     Input('filter-xdie', 'value'),
     Input('filter-ydie', 'value'),
     Input('filter-static-iteration', 'value'),
     Input('filter-orientation', 'value'),
     Input('filter-site-serial-number', 'value')]
)
def set_coarse_filters(tool_number, x_pass_fail_filters, y_pass_fail_filters, time_filters, lot_filters, xdie_filters, ydie_filters, iteration_filters, orientation_filters, serial_filters):
    df = load_coarse_data(tool_number)
    if df.empty:
        return [{}]*9  # Return empty options if no data

    filtered_df = df.copy()

    if time_filters:
        filtered_df = filtered_df[filtered_df['Time'].isin(time_filters)]
    if x_pass_fail_filters:
        filtered_df = filtered_df[filtered_df['X Pass/Fail'].isin(x_pass_fail_filters)]
    if y_pass_fail_filters:
        filtered_df = filtered_df[filtered_df['Y Pass/Fail'].isin(y_pass_fail_filters)]   
    if lot_filters:
        filtered_df = filtered_df[filtered_df['Lot Name'].isin(lot_filters)]
    if xdie_filters:
        filtered_df = filtered_df[filtered_df['X_Die'].isin(xdie_filters)]
    if ydie_filters:
        filtered_df = filtered_df[filtered_df['Y_Die'].isin(ydie_filters)]
    if iteration_filters:
        filtered_df = filtered_df[filtered_df['Static Iteration'].isin(iteration_filters)]
    if orientation_filters:
        filtered_df = filtered_df[filtered_df['Orientation'].isin(orientation_filters)]
    if serial_filters:
        filtered_df = filtered_df[filtered_df['Site Serial Number'].isin(serial_filters)]

    return [
        [{'label': str(i), 'value': i} for i in filtered_df['X Pass/Fail'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Y Pass/Fail'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Time'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Lot Name'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['X_Die'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Y_Die'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Static Iteration'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Orientation'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Site Serial Number'].unique()]
    ]

@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('x-vs-time-plot', 'figure'),
     Output('y-vs-time-plot', 'figure'),
     Output('table-container', 'children')],
    [Input('tool-number-dropdown', 'value'),
     Input('filter-x-pass-fail', 'value'),
     Input('filter-y-pass-fail', 'value'),
     Input('filter-time', 'value'),
     Input('filter-lot', 'value'),
     Input('filter-xdie', 'value'),
     Input('filter-ydie', 'value'),
     Input('filter-static-iteration', 'value'),
     Input('filter-orientation', 'value'),
     Input('filter-site-serial-number', 'value')]
)
def update_coarse_output(selected_tool, x_pass_fail_filters, y_pass_fail_filters, time_filters, lot_filters, xdie_filters, ydie_filters, iteration_filters, orientation_filters, serial_filters):
    df = load_coarse_data(selected_tool)
    if df.empty:
        return {}, {}, {}, dash_table.DataTable(data=[], columns=[{"name": i, "id": i} for i in []])

    filtered_df = df.copy()

    if x_pass_fail_filters:
        filtered_df = filtered_df[filtered_df['X Pass/Fail'].isin(x_pass_fail_filters)]
    if y_pass_fail_filters:
        filtered_df = filtered_df[filtered_df['Y Pass/Fail'].isin(y_pass_fail_filters)]
    if time_filters:
        filtered_df = filtered_df[filtered_df['Time'].isin(time_filters)]
    if lot_filters:
        filtered_df = filtered_df[filtered_df['Lot Name'].isin(lot_filters)]
    if xdie_filters:
        filtered_df = filtered_df[filtered_df['X_Die'].isin(xdie_filters)]
    if ydie_filters:
        filtered_df = filtered_df[filtered_df['Y_Die'].isin(ydie_filters)]
    if iteration_filters:
        filtered_df = filtered_df[filtered_df['Static Iteration'].isin(iteration_filters)]
    if orientation_filters:
        filtered_df = filtered_df[filtered_df['Orientation'].isin(orientation_filters)]
    if serial_filters:
        filtered_df = filtered_df[filtered_df['Site Serial Number'].isin(serial_filters)]

    # Scatter plot
    scatter_plot = {
        'data': [
            {
                'x': filtered_df['X'],
                'y': filtered_df['Y'],
                'mode': 'markers',
                'type': 'scatter',
                'marker': {
                    'color': ['red' if (x > 481.5 or x < 478.5 or y > 406.5 or y < 403.5) else 'blue' for x, y in zip(filtered_df['X'], filtered_df['Y'])]
                }
            }
        ],
        'layout': {
            'title': 'Coarse X vs. Coarse Y',
            'xaxis': {'title': 'Coarse X'},
            'yaxis': {'title': 'Coarse Y'}
        }
    }

    # X vs Time Plot
    x_vs_time_figure = {
        'data': [
            {
                'x': filtered_df['Time'],
                'y': filtered_df['X'],
                'type': 'scatter',
                'mode': 'markers',
                'name': 'X vs Time',
                'marker': {
                    'color': ['red' if (x > 481.5 or x < 478.5) else 'blue' for x in filtered_df['X']]
                }
            }
        ],
        'layout': {
            'title': 'Coarse X vs Time',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Coarse X'}
        }
    }

    # Y vs Time Plot
    y_vs_time_figure = {
        'data': [
            {
                'x': filtered_df['Time'],
                'y': filtered_df['Y'],
                'type': 'scatter',
                'mode': 'markers',
                'name': 'Y vs Time',
                'marker': {
                    'color': ['red' if (y > 406.5 or y < 403.5) else 'blue' for y in filtered_df['Y']]
                }
            }
        ],
        'layout': {
            'title': 'Coarse Y vs Time',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Coarse Y'}
        }
    }

    # Update table with tool number and highlight cells
    filtered_df.insert(0, 'Tool Number', selected_tool)  # Add tool number column at the beginning
    table_data = filtered_df.to_dict('records')

    table = dash_table.DataTable(
        data=table_data,
        columns=[{"name": "Tool Number", "id": "Tool Number"}] + [{"name": i, "id": i} for i in filtered_df.columns if i != 'Tool Number'],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{X} > 481.5 || {X} < 478.5',
                    'column_id': 'X'
                },
                'color': 'red',
                'fontWeight': 'bold'
            },
            {
                'if': {
                    'filter_query': '{Y} > 406.5 || {Y} < 403.5',
                    'column_id': 'Y'
                },
                'color': 'red',
                'fontWeight': 'bold'
            }
        ]
    )

    return scatter_plot, x_vs_time_figure, y_vs_time_figure, table

def set_tad_filters(tool_number, time_filters, recipe_filters, lot_filters, phase_filters, site_serial_number_filters, die_x_filters, die_y_filters, misreg_x_filters, misreg_y_filters, tis_x_filters, tis_y_filters, dad_pos_x_filters, dad_pos_y_filters, slope_x_filters, slope_y_filters, b_x_filters, b_y_filters, exit_reason_filters, stats_filters):
    df = load_tad_data(tool_number)
    if df.empty:
        return [{}]*20  # Return empty options if no data

    filtered_df = df.copy()

    if time_filters:
        filtered_df = filtered_df[filtered_df['Time'].isin(time_filters)]
    if recipe_filters:
        filtered_df = filtered_df[filtered_df['Recipe'].isin(recipe_filters)]
    if lot_filters:
        filtered_df = filtered_df[filtered_df['Lot'].isin(lot_filters)]
    if phase_filters:
        filtered_df = filtered_df[filtered_df['Phase'].isin(phase_filters)]
    if site_serial_number_filters:
        filtered_df = filtered_df[filtered_df['Site_Serial_Number'].isin(site_serial_number_filters)]
    if die_x_filters:
        filtered_df = filtered_df[filtered_df['Die_X'].isin(die_x_filters)]
    if die_y_filters:
        filtered_df = filtered_df[filtered_df['Die_Y'].isin(die_y_filters)]
    if misreg_x_filters:
        filtered_df = filtered_df[filtered_df['Misreg_X'].isin(misreg_x_filters)]
    if misreg_y_filters:
        filtered_df = filtered_df[filtered_df['Misreg_Y'].isin(misreg_y_filters)]
    if tis_x_filters:
        filtered_df = filtered_df[filtered_df['TIS_X'].isin(tis_x_filters)]
    if tis_y_filters:
        filtered_df = filtered_df[filtered_df['TIS_Y'].isin(tis_y_filters)]
    if dad_pos_x_filters:
        filtered_df = filtered_df[filtered_df['DAD_Pos_X'].isin(dad_pos_x_filters)]
    if dad_pos_y_filters:
        filtered_df = filtered_df[filtered_df['DAD_Pos_Y'].isin(dad_pos_y_filters)]
    if slope_x_filters:
        filtered_df = filtered_df[filtered_df['Slope_X'].isin(slope_x_filters)]
    if slope_y_filters:
        filtered_df = filtered_df[filtered_df['Slope_Y'].isin(slope_y_filters)]
    if b_x_filters:
        filtered_df = filtered_df[filtered_df['B_X'].isin(b_x_filters)]
    if b_y_filters:
        filtered_df = filtered_df[filtered_df['B_Y'].isin(b_y_filters)]
    if exit_reason_filters:
        filtered_df = filtered_df[filtered_df['Exit_Reason'].isin(exit_reason_filters)]
    if stats_filters:
        filtered_df = filtered_df[filtered_df['Stats'].isin(stats_filters)]

    return [
        [{'label': str(i), 'value': i} for i in filtered_df['Time'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Recipe'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Lot'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Phase'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Site_Serial_Number'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Die_X'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Die_Y'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Misreg_X'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Misreg_Y'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['TIS_X'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['TIS_Y'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['DAD_Pos_X'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['DAD_Pos_Y'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Slope_X'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Slope_Y'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['B_X'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['B_Y'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Exit_Reason'].unique()],
        [{'label': str(i), 'value': i} for i in filtered_df['Stats'].unique()],
    ]

@app.callback(
    [Output('filter-time_tad', 'options'),
     Output('filter-recipe', 'options'),
     Output('filter-lot_tad', 'options'),
     Output('filter-phase', 'options'),
     Output('filter-site-serial-number_tad', 'options'),
     Output('filter-die-x', 'options'),
     Output('filter-die-y', 'options'),
     Output('filter-misreg-x', 'options'),
     Output('filter-misreg-y', 'options'),
     Output('filter-tis-x', 'options'),
     Output('filter-tis-y', 'options'),
     Output('filter-dad-pos-x', 'options'),
     Output('filter-dad-pos-y', 'options'),
     Output('filter-slope-x', 'options'),
     Output('filter-slope-y', 'options'),
     Output('filter-b-x', 'options'),
     Output('filter-b-y', 'options'),
     Output('filter-exit-reason', 'options'),
     Output('filter-stats', 'options')],
    [Input('tool-number-dropdown_tad', 'value'),
     Input('filter-time_tad', 'value'),
     Input('filter-recipe', 'value'),
     Input('filter-lot_tad', 'value'),
     Input('filter-phase', 'value'),
     Input('filter-site-serial-number_tad', 'value'),
     Input('filter-die-x', 'value'),
     Input('filter-die-y', 'value'),
     Input('filter-misreg-x', 'value'),
     Input('filter-misreg-y', 'value'),
     Input('filter-tis-x', 'value'),
     Input('filter-tis-y', 'value'),
     Input('filter-dad-pos-x', 'value'),
     Input('filter-dad-pos-y', 'value'),
     Input('filter-slope-x', 'value'),
     Input('filter-slope-y', 'value'),
     Input('filter-b-x', 'value'),
     Input('filter-b-y', 'value'),
     Input('filter-exit-reason', 'value'),
     Input('filter-stats', 'value')]
)
def update_tad_filter_options(tool_number, time_filters, recipe_filters, lot_filters, phase_filters, site_serial_number_filters, die_x_filters, die_y_filters, misreg_x_filters, misreg_y_filters, tis_x_filters, tis_y_filters, dad_pos_x_filters, dad_pos_y_filters, slope_x_filters, slope_y_filters, b_x_filters, b_y_filters, exit_reason_filters, stats_filters):
    return set_tad_filters(tool_number, time_filters, recipe_filters, lot_filters, phase_filters, site_serial_number_filters, die_x_filters, die_y_filters, misreg_x_filters, misreg_y_filters, tis_x_filters, tis_y_filters, dad_pos_x_filters, dad_pos_y_filters, slope_x_filters, slope_y_filters, b_x_filters, b_y_filters, exit_reason_filters, stats_filters)



@app.callback(
    [Output('tis-x-vs-dad-x-plot', 'figure'),
     Output('tis-y-vs-dad-y-plot', 'figure'),
     Output('table-container_tad', 'children')],
    [Input('tool-number-dropdown_tad', 'value'),
     Input('filter-time_tad', 'value'),
     Input('filter-recipe', 'value'),
     Input('filter-lot_tad', 'value'),
     Input('filter-phase', 'value'),
     Input('filter-site-serial-number_tad', 'value'),
     Input('filter-die-x', 'value'),
     Input('filter-die-y', 'value'),
     Input('filter-misreg-x', 'value'),
     Input('filter-misreg-y', 'value'),
     Input('filter-tis-x', 'value'),
     Input('filter-tis-y', 'value'),
     Input('filter-dad-pos-x', 'value'),
     Input('filter-dad-pos-y', 'value'),
     Input('filter-slope-x', 'value'),
     Input('filter-slope-y', 'value'),
     Input('filter-b-x', 'value'),
     Input('filter-b-y', 'value'),
     Input('filter-exit-reason', 'value'),
     Input('filter-stats', 'value')]
)
def update_output(selected_tool, time_filters, recipe_filters, lot_filters, phase_filters, site_serial_number_filters, die_x_filters, die_y_filters, misreg_x_filters, misreg_y_filters, tis_x_filters, tis_y_filters, dad_pos_x_filters, dad_pos_y_filters, slope_x_filters, slope_y_filters, b_x_filters, b_y_filters, exit_reason_filters, stats_filters):
    df = load_tad_data(selected_tool)
    if df.empty:
        return {}, {}, dash_table.DataTable(columns=[], data=[])

    filtered_df = df.copy()

    # Apply filters
    if time_filters:
        filtered_df = filtered_df[filtered_df['Time'].isin(time_filters)]
    if recipe_filters:
        filtered_df = filtered_df[filtered_df['Recipe'].isin(recipe_filters)]
    if lot_filters:
        filtered_df = filtered_df[filtered_df['Lot'].isin(lot_filters)]
    if phase_filters:
        filtered_df = filtered_df[filtered_df['Phase'].isin(phase_filters)]
    if site_serial_number_filters:
        filtered_df = filtered_df[filtered_df['Site_Serial_Number'].isin(site_serial_number_filters)]
    if die_x_filters:
        filtered_df = filtered_df[filtered_df['Die_X'].isin(die_x_filters)]
    if die_y_filters:
        filtered_df = filtered_df[filtered_df['Die_Y'].isin(die_y_filters)]
    if misreg_x_filters:
        filtered_df = filtered_df[filtered_df['Misreg_X'].isin(misreg_x_filters)]
    if misreg_y_filters:
        filtered_df = filtered_df[filtered_df['Misreg_Y'].isin(misreg_y_filters)]
    if tis_x_filters:
        filtered_df = filtered_df[filtered_df['TIS_X'].isin(tis_x_filters)]
    if tis_y_filters:
        filtered_df = filtered_df[filtered_df['TIS_Y'].isin(tis_y_filters)]
    if dad_pos_x_filters:
        filtered_df = filtered_df[filtered_df['DAD_Pos_X'].isin(dad_pos_x_filters)]
    if dad_pos_y_filters:
        filtered_df = filtered_df[filtered_df['DAD_Pos_Y'].isin(dad_pos_y_filters)]
    if slope_x_filters:
        filtered_df = filtered_df[filtered_df['Slope_X'].isin(slope_x_filters)]
    if slope_y_filters:
        filtered_df = filtered_df[filtered_df['Slope_Y'].isin(slope_y_filters)]
    if b_x_filters:
        filtered_df = filtered_df[filtered_df['B_X'].isin(b_x_filters)]
    if b_y_filters:
        filtered_df = filtered_df[filtered_df['B_Y'].isin(b_y_filters)]
    if exit_reason_filters:
        filtered_df = filtered_df[filtered_df['Exit_Reason'].isin(exit_reason_filters)]
    if stats_filters:
        filtered_df = filtered_df[filtered_df['Stats'].isin(stats_filters)]

    # Calculate the custom fit line for TIS_X vs DAD_Pos_X
    if not filtered_df['TIS_X'].empty and not filtered_df['DAD_Pos_X'].empty:
        x = filtered_df['TIS_X'].astype(float)
        y = filtered_df['DAD_Pos_X'].astype(float)
        slope_x = filtered_df['Slope_X'].mean() if 'Slope_X' in filtered_df else 0
        intercept_x = filtered_df['B_X'].mean() if 'B_X' in filtered_df else 0
        
        # Custom line with slope of -1000.0 * Slope_X
        custom_slope_x = -1000.0 * slope_x
        fit_line_x = custom_slope_x * x + intercept_x
        
    else:
        fit_line_x = []

    # Create TIS X vs DAD Position X figure
    tis_x_vs_dad_x_figure = {
        'data': [
            go.Scatter(
                x=filtered_df['TIS_X'].astype(float),
                y=filtered_df['DAD_Pos_X'].astype(float),
                mode='markers',
                name='Data',
                marker=dict(
                    color=['red' if (y > 15 and y < 20) else 'blue' for y in filtered_df['DAD_Pos_X']] # Change these values according to your need Contols red color in graph 
                )
            ),
            go.Scatter(
                x=filtered_df['TIS_X'].astype(float),
                y=fit_line_x,
                mode='lines',
                name='Custom Fit Line',
                line=dict(color='red')
            )
        ],
        'layout': {
            'title': 'TIS X vs DAD Position X',
            'xaxis': {'title': 'TIS X'},
            'yaxis': {'title': 'DAD Position X'}
        }
    }

    # Calculate the custom fit line for TIS_Y vs DAD_Pos_Y
    if not filtered_df['TIS_Y'].empty and not filtered_df['DAD_Pos_Y'].empty:
        y = filtered_df['TIS_Y'].astype(float)
        x = filtered_df['DAD_Pos_Y'].astype(float)
        slope_y = filtered_df['Slope_Y'].mean() if 'Slope_Y' in filtered_df else 0
        intercept_y = filtered_df['B_Y'].mean() if 'B_Y' in filtered_df else 0
        
        # Custom line with slope of -1000.0 * Slope_Y
        custom_slope_y = -1000.0 * slope_y
        fit_line_y = custom_slope_y * y + intercept_y
        
    else:
        fit_line_y = []

    # Create TIS Y vs DAD Position Y figure
    tis_y_vs_dad_y_figure = {
        'data': [
            go.Scatter(
                x=filtered_df['TIS_Y'].astype(float),
                y=filtered_df['DAD_Pos_Y'].astype(float),
                mode='markers',
                name='Data',
                marker=dict(
                    color=['red' if (y > 15 and y < 20) else 'blue' for y in filtered_df['DAD_Pos_Y']]  # Change these values according to your need Contols red color in graph
                )
            ),
            go.Scatter(
                x=filtered_df['TIS_Y'].astype(float),
                y=fit_line_y,
                mode='lines',
                name='Custom Fit Line',
                line=dict(color='red')
            )
        ],
        'layout': {
            'title': 'TIS Y vs DAD Position Y',
            'xaxis': {'title': 'TIS Y'},
            'yaxis': {'title': 'DAD Position Y'}
        }
    }

    # Update table with tool number and highlight cells
    filtered_df.insert(0, 'Tool Number', selected_tool)  # Add tool number column at the beginning
    table_data = filtered_df.to_dict('records')

    table = dash_table.DataTable(
        data=table_data,
        columns=[{"name": "Tool Number", "id": "Tool Number"}] + [{"name": i, "id": i} for i in filtered_df.columns if i != 'Tool Number'],
        style_data_conditional=[
            {
                'if': { 
                    'filter_query': '{Slope_X} > 8 || {Slope_X} < -8',  # Change these values according to your need  Contols red color in table 
                    'column_id': 'Slope_X'
                },
                'color': 'red',
                'fontWeight': 'bold'
            },
            {
                'if': {
                    'filter_query': '{Slope_Y} > 8 || {Slope_Y} < -8',  # Change these values according to your need Contols red color in table 
                    'column_id': 'Slope_Y'
                },
                'color': 'red',
                'fontWeight': 'bold'
            },
           
        ]
    )

    return tis_x_vs_dad_x_figure, tis_y_vs_dad_y_figure, table
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
