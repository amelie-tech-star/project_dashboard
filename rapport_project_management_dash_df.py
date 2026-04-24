from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import re
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display
import math
import plotly.graph_objects as go
from model import management_files
import numpy as np


date = '2026-04-30'
project_list = ['25-0030 - FLYCERA']
project_dir = '\\\\dfs\\AIX\\KNS\\Doc_KN\\XXX affaires\\2025\\'

col_list = ['Actual Cost', 'Earned Value', 'Reste à Faire', 'Planned Value']
col_list_short = ['AC', 'EV', 'RAF', 'PV']
color_list = { 'AC' : 'orchid', 'RAF': 'gray', 'EV':'gold', 'PV' : 'lime', 'CAT' : 'blue', 'Objectif CAT' : 'cyan' }
cat_titles = ['MANAGEMENT', 'SYSTEM', 'HARDWARE', 'FIRMWARE', 'SOFTWARE', 'MECHANICAL', 'CAO', 'Manufacturing', 'Procurement', 'Warranty/Risk', 'TOTAL']
#cat_titles = ['MANAGEMENT', 'SYSTEM', 'MECHANICAL', 'HARDWARE', 'SOFTWARE', 'Manufacturing', 'Procurement', 'TOTAL']
nb_cat_title = len(cat_titles)-1
print(nb_cat_title)
actuality = ['meeting', 'Main issues', 'Past activities', 'Future activities']
baseline_chiffres = ['CA', 'CAT', 'PM', 'CAT NEW', 'PM NEW']
template="plotly_dark"

PERF_collection = {}
cat_list = {}
TBD_avancement = pd.DataFrame()
BASELINE_dataframe = pd.DataFrame()
FILE_dataframe = pd.DataFrame()

FILE_dataframe= management_files.get_FILE_dataframe(project_list, date, project_dir)

for project in project_list:

    ########################
    # PERF SHEET PARSING   #
    ########################
    PERF = pd.read_excel (FILE_dataframe.loc[project, 'Cost'], 'PERF.')
    # Select main rows only with "x" in 'Nom du poste' column
    PERF = PERF[PERF['Nom du poste'] == 'x']
    # Get "Categories" column and use it as index (Projet, Système, HW, FW...)
    cat_list[project] = PERF['Catégorie'].values
    
    PERF.index=cat_list[project]
    # Transpose the dataframe
    PERF = PERF.transpose()

    # For each "catégorie de poste" (Projet, Système, HW, FW...), select
    # requested columns (PV, EV, AC, RAF)
    for cat in cat_list[project]:
        result = pd.DataFrame()
        data = {}
        for col in col_list:
            data[col]= PERF[PERF.index.str.contains(col)][cat]
            # Replace long columns names with acronyms
            s1=pd.DataFrame(data[col].values, columns=[(col).replace("Planned Value", "PV")
                            .replace("Earned Value", "EV")
                            .replace("Actual Cost", "AC")
                            .replace("Reste à Faire", "RAF")])
            result=pd.concat([result, s1], axis=1)
        PERF_collection[project,cat]=pd.DataFrame(result, columns = col_list_short)



    ########################
    # BASELINE PARSING     #
    ########################
    BASELINE = pd.read_excel (FILE_dataframe.loc[project, 'Cost'], 'BASELINE', header=None)
    synth_chif_found= False
    
    # For each colomn
    for col_name, col_data in BASELINE.items():
        # For each value in the column
        for idx, value in col_data.items():
            for baseline_name in baseline_chiffres:
                # if baseline_name is found
                if baseline_name == str(value):
                    synth_chif_found= True
                    synth_chif_found_value = str(value)
                    synth_chif_found_j = idx
                    break

            if synth_chif_found == True and synth_chif_found_j !=  idx:
                synth_chif_found= False
                print (f"{synth_chif_found_value} = {value}")
                BASELINE_dataframe.loc[project,synth_chif_found_value] = value

    ########################
    # TBD SHEET PARSING    #
    ########################
    TbD = pd.read_excel (FILE_dataframe.loc[project, 'TBD'], 'Actuality', header=None)
    synth_chif_found= False
    for i, row in TbD.iterrows():
        for j, value in row.items():
            for synth_avcmt in actuality:
                if synth_avcmt in str(value):
                    TBD_avancement.loc[project, synth_avcmt]=value

#######################
# PERF AND EVM FIGURE #
#######################
perf_fig = go.Figure()
evm_fig  = go.Figure()


nb_cols = 5
nb_row = 2

#nb_cols = 3
#nb_row = 3

perf_fig = make_subplots(rows=nb_row, cols=nb_cols, shared_yaxes=True, subplot_titles=cat_titles[:nb_cat_title])
evm_fig  = make_subplots(rows=1, cols=1, shared_yaxes=True, subplot_titles=cat_titles[nb_cat_title-1])

# For each title category 
for j in range (0, nb_cat_title+1):
    perf_df=PERF_collection[project_list[0],cat_list[project_list[0]][j]]
    # Subplot organization
    if j < nb_cols:
        j_row=1
        j_col=j+1
    elif j < nb_cols*2:
        j_row=2
        j_col=j+1 - nb_cols
    elif j < nb_cols*3:
        j_row=3
        j_col=j+1 - 2*nb_cols

    # if j < nb_cols:
        # j_row=1
        # j_col=j+1
        
    print(f"j {j} j_row {j_row} j_col{j_col}")
        
    # elif j < nb_cols*2:
        # j_row=2
        # j_col=j- nb_cols - 1
    # elif j < nb_cols*3:
        # j_row=3
        # j_col=j- nb_cols - 1




    # Select EVM figure for TOTAL
    if j < nb_cat_title:
        fig = perf_fig
    elif j == nb_cat_title:
        fig = evm_fig
        j_row=1
        j_col=1

    # Diplay first project with categories
    for i in range(0, len(perf_df.columns)):
        perf_x = perf_df[perf_df.columns[i]].index
        perf_y = perf_df[perf_df.columns[i]]

        if perf_df.columns[i] == 'AC' or perf_df.columns[i]=='RAF':
            print(f"FOR AC RAF i {i} j {j} j_row {j_row} j_col{j_col}")
            fig.add_trace(
                go.Bar(
                    x=perf_x,
                    y=perf_y,
                    marker=dict(color = color_list[perf_df.columns[i]]),
                    name=cat_list[project_list[0]][j] + ' ' + perf_df.columns[i]),
                    row=j_row,
                    col=j_col)
        else:
            print(f"ELSE i {i} j {j} j_row {j_row} j_col{j_col}")
            fig.add_trace(
                go.Scatter(
                    x=perf_x,
                    y=perf_y,
                    mode='lines+markers',
                    line_color= color_list[perf_df.columns[i]],
                    name=cat_list[project_list[0]][j] + ' ' + perf_df.columns[i]),
                    row=j_row,
                    col=j_col)

    # Add CAT curve for EVM graph
    if j == nb_cat_title:
        perf_x = perf_df[perf_df.columns[0]].index
        perf_y = np.empty(len(perf_x))
        perf_y.fill(BASELINE_dataframe.loc[project_list[0],'CAT'])
        fig.add_trace(
           go.Scatter(
               x=perf_x,
               y=perf_y,
               mode='lines+markers',
               line_color= color_list['CAT'],
               name=cat_list[project_list[0]][j] + ' CAT'),
               row=j_row,
               col=j_col)

perf_fig.update_layout(template=template, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', barmode='stack', hovermode="x unified", showlegend=False,hoverlabel_namelength=20)
perf_fig.update_yaxes()
perf_fig.update_xaxes()

evm_fig.update_layout(template=template, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',  barmode='stack', hovermode="x unified", showlegend=False,hoverlabel_namelength=20)
evm_fig.update_yaxes()
evm_fig.update_xaxes()


####################
# BASELINE FIGURE #
####################
tbd_fig = go.Figure()
tbd_fig.add_trace(
    go.Indicator(
        mode = "gauge+number+delta",
        value = BASELINE_dataframe.loc[project_list[0],'CAT'],
        title = {'text': "CAT & DELTA CAT<br><span style='font-size:0.8em;color:gray'> CA : " +str(BASELINE_dataframe.loc[project_list[0],'CA']/1000) + "kEUR</span>"},
        delta = {'reference': BASELINE_dataframe.loc[project_list[0],'CAT NEW'], },
        gauge = {
            'bar': {'color': color_list['RAF']},
            'steps': [
                {'range': [0, BASELINE_dataframe.loc[project_list[0],'CAT']], 'color': color_list['Objectif CAT']},
                {'range': [BASELINE_dataframe.loc[project_list[0],'CAT'], BASELINE_dataframe.loc[project_list[0],'CAT NEW']],'color': color_list['CAT']},
                {'range': [BASELINE_dataframe.loc[project_list[0],'CAT NEW'], BASELINE_dataframe.loc[project_list[0],'CA']],'color': color_list['AC']}],
            }
        )
    )
tbd_fig.update_layout(template=template, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

tbd_ind_fig = go.Figure()
tbd_ind_fig.add_trace(
    go.Indicator(
        mode = "number+delta",
        value = BASELINE_dataframe.loc[project_list[0],'PM NEW'],
        number = {'valueformat':'.2%'},
        title = {'text': u'PM & ΔPM %'},
        delta = {'reference': BASELINE_dataframe.loc[project_list[0],'PM'],
        'valueformat':'.2%',},
        domain = {'row': 0, 'column': 0},
        name = 'pm_percent',
        )
    )

tbd_ind_fig.add_trace(
    go.Indicator(
        mode = "number+delta",
        value = BASELINE_dataframe.loc[project_list[0],'CA']-BASELINE_dataframe.loc[project_list[0],'CAT NEW'],
        title = {'text': u'PM & ΔPM'},
        delta = {'reference': BASELINE_dataframe.loc[project_list[0],'CA']-BASELINE_dataframe.loc[project_list[0],'CAT'],},
        domain = {'row': 1, 'column': 0},
        name = 'pm_value',
        )
    )
tbd_ind_fig.update_layout(template=template, grid = {'rows': 2, 'columns': 1, 'pattern': 'independent'})

#################
# TBD CALLBACK  #
#################
@callback([
    Output(component_id=actuality[0], component_property='children'),
    Output(component_id=actuality[1], component_property='children'),
    Output(component_id=actuality[2], component_property='children'),
    Output(component_id=actuality[3], component_property='children'),
    ],
    Input(component_id='project-item', component_property='value')
)
def update_synthesis(project_chosen):
    children_0 = TBD_avancement.loc[project_chosen, actuality[0]]
    children_1 = TBD_avancement.loc[project_chosen, actuality[1]]
    children_2 = TBD_avancement.loc[project_chosen, actuality[2]]
    children_3 = TBD_avancement.loc[project_chosen, actuality[3]]
    return children_0,children_1,children_2, children_3

@callback(
    Output(component_id='TBD_GAUGE', component_property='figure'),
    Input(component_id='project-item', component_property='value')
)
def update_tbd_gauge(project_chosen):
    tbd_fig.update_traces(
        value = BASELINE_dataframe.loc[project_chosen,'CAT'],
        title = {'text': "CAT & DELTA CAT<br><span style='font-size:0.8em;color:gray'> CA : " +str(BASELINE_dataframe.loc[project_chosen,'CA']/1000) + "kEUR</span>"},
        delta = {'reference': BASELINE_dataframe.loc[project_chosen,'CAT NEW']},
        gauge = {
             'steps': [
                {'range': [0, BASELINE_dataframe.loc[project_chosen,'CAT']]},
                {'range': [BASELINE_dataframe.loc[project_chosen,'CAT'], BASELINE_dataframe.loc[project_chosen,'CAT NEW']]},
                {'range': [BASELINE_dataframe.loc[project_chosen,'CAT NEW'], BASELINE_dataframe.loc[project_chosen,'CA']] }
                ],
         }
        )
    return tbd_fig

@callback(
    Output(component_id='TBD_INDICATOR', component_property='figure'),
    Input(component_id='project-item', component_property='value')
)
def update_ind_tbd(project_chosen):
    tbd_ind_fig.update_traces(
        value = BASELINE_dataframe.loc[project_chosen,'PM NEW'],
        delta = {'reference': BASELINE_dataframe.loc[project_chosen,'PM']},
        selector=dict(name='pm_percent'),
        )
    tbd_ind_fig.update_traces(
        value = BASELINE_dataframe.loc[project_chosen,'CA']-BASELINE_dataframe.loc[project_chosen,'CAT NEW'],
        delta = {'reference': BASELINE_dataframe.loc[project_chosen,'CA']-BASELINE_dataframe.loc[project_chosen,'CAT']},
        selector=dict(name='pm_value'),
        )
    return tbd_ind_fig


@callback(
    [Output(component_id='Link_TBD', component_property='value'),
     Output(component_id='Link_Cost', component_property='value'),
     Output(component_id='Link_Forecast', component_property='value'),
     Output(component_id='Link_Schedule', component_property='value')],
    Input(component_id='project-item', component_property='value')
)
def update_href(project_chosen):
    return FILE_dataframe.loc[project_chosen].get('TBD',''), FILE_dataframe.loc[project_chosen].get('Cost',''), FILE_dataframe.loc[project_chosen].get('Forecast',''), FILE_dataframe.loc[project_chosen].get('Schedule')

#################
# BTN CALLBACK  #
#################
@callback(
    Output(component_id='Open_TBD', component_property='children'),
    [Input(component_id='Link_TBD', component_property='n_clicks'),
    State(component_id='Link_TBD', component_property='value')])
def open_file_tbd(n_clicks, value):
    if n_clicks:
        print(value)
        print(n_clicks)
        os.startfile(value)
    return ""

@callback(
    Output(component_id='Open_Cost', component_property='children'),
    [Input(component_id='Link_Cost', component_property='n_clicks'),
    State(component_id='Link_Cost', component_property='value')])
def open_file_cost(n_clicks, value):
    if n_clicks:
        print(value)
        print(n_clicks)
        os.startfile(value)
    return ""

@callback(
    Output(component_id='Open_Schedule', component_property='children'),
    [Input(component_id='Link_Schedule', component_property='n_clicks'),
    State(component_id='Link_Schedule', component_property='value')])
def open_file_schedule(n_clicks, value):
    if n_clicks:
        print(value)
        print(n_clicks)
        os.startfile(value)
    return ""

@callback(
    Output(component_id='Open_Forecast', component_property='children'),
    [Input(component_id='Link_Forecast', component_property='n_clicks'),
    State(component_id='Link_Forecast', component_property='value')])
def open_file_forecast(n_clicks, value):
    if n_clicks:
        print(value)
        print(n_clicks)
        os.startfile(value)
    return ""

#################
# EVM CALLBACK  #
#################
@callback(
    Output(component_id='EVM', component_property='figure'),
    Input(component_id='project-item', component_property='value')
)
def update_evm(project_chosen):
    # Update every trace (EV, RAF, AC...)
    perf_proj_collection= {}
    perf_proj_collection = PERF_collection[project_chosen,cat_list[project_chosen][nb_cat_title]]
    for col in perf_df.columns:
        evm_fig.update_traces(
            x=perf_proj_collection.index,
            y=perf_proj_collection[col],
            selector=dict(name=cat_titles[nb_cat_title] + ' ' + col))

    # Update separatly CAT that is coming from BASELINE
    perf_y = np.empty(len(perf_x))
    perf_y.fill(BASELINE_dataframe.loc[project_chosen,'CAT'])
    evm_fig.update_traces(
        x=perf_proj_collection.index,
        y=perf_y,
        selector=dict(name=cat_titles[nb_cat_title] + ' CAT'))

    return evm_fig

#################
# PERF CALLBACK #
#################
@callback(
    Output(component_id='PERF', component_property='figure'),
    Input(component_id='project-item', component_property='value')
)
def update_perf(project_chosen):
    perf_y=[]
    perf_name = []
    perf_proj_collection= {}
    for k in range (0, nb_cat_title):
        perf_proj_collection[cat_list[project_chosen][k]] = PERF_collection[project_chosen,cat_list[project_chosen][k]]
        for col in perf_df.columns:
            perf_fig.update_traces(
                x=perf_proj_collection[cat_list[project_chosen][k]].index,
                y=perf_proj_collection[cat_list[project_chosen][k]][col],
                selector=dict(name=(cat_list[project_chosen][k] + " " + col)))

    return perf_fig

######################
# DASH LAYOUT        #
######################

app = Dash(external_stylesheets=[dbc.themes.SLATE])

FILE_dataframe.loc[project, 'TBD']

# App layout

app.layout = dbc.Container([dbc.Row([
    # MENU
    dbc.Col([
        # DROPDOWN
        dbc.Row(dcc.Dropdown(options=project_list, value=project_list[0], id='project-item')),
        # LINKS
        dbc.Row(dbc.Button("Dashboard", value=FILE_dataframe.loc[project].get('TBD',''), id = 'Link_TBD')),
        dbc.Row(dbc.Button("Costs", value=FILE_dataframe.loc[project].get('Cost',''), id = 'Link_Cost')),
        dbc.Row(dbc.Button("Forecast", value=FILE_dataframe.loc[project].get('Forecast',''), id = 'Link_Forecast')),
        dbc.Row(dbc.Button("Schedule", value=FILE_dataframe.loc[project].get('Schedule',''), id = 'Link_Schedule')),
        html.Div(id='Open_TBD', style={'display':'none'}),
        html.Div(id='Open_Cost', style={'display':'none'}),
        html.Div(id='Open_Forecast', style={'display':'none'}),
        html.Div(id='Open_Schedule', style={'display':'none'}),
        ],width=1),
    # PANEL GRAPH
    dbc.Col([
        dbc.Row([
            dbc.Col([
                # INDICATOR
                dbc.Row( dcc.Graph(figure=tbd_ind_fig, id='TBD_INDICATOR', style={'height':'25vh','border': '1px solid'}), ),
                # REUNION
                dbc.Row(dbc.Card(html.P(TBD_avancement.loc[project,actuality[0]], id=actuality[0]), className='custom-card'),),
                ],width=2),
            # EVM GRAPH
            dbc.Col(dbc.Row(dcc.Graph(figure=evm_fig, id='EVM',style={ 'height':'50vh'})),
                width=6, style={'border': '1px solid'} ),

            dbc.Col( [
                 # MAIN ISSUES
                 dbc.Row(dbc.Card(html.P(TBD_avancement.loc[project,actuality[1]], id=actuality[1]), style={'color': 'red'}, className='custom-card')),
                 # GAUGE
                 dbc.Row(dcc.Graph(figure=tbd_fig, id='TBD_GAUGE',style={'border': '1px solid', 'height':'25vh'})),
                 ], width=4 ),
            ],),
        dbc.Row([
            #PERF GRAPH
            dbc.Col(dbc.Row( dcc.Graph(figure=perf_fig, id='PERF',style={'height':'50vh'})),
                width=8, style={'border': '1px solid'} ),
            #AVANCEMENT
            dbc.Col(dbc.Row([
                dbc.Card(html.P(children=TBD_avancement.loc[project,actuality[2]], id=actuality[2]), style={'color': color_list['EV']}, className='custom-card'),
                dbc.Card(html.P(children=TBD_avancement.loc[project,actuality[3]], id=actuality[3]), style={'color': color_list['PV']}, className='custom-card'),
                ]), width=4),
        ],), ]),],style={'margin-top': '5px', 'margin-left': '5px','margin-right': '5px', 'margin-bottom': '5px'})]
        , fluid=True)


if __name__ == '__main__':
    app.run(debug=False)
