from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

external_stylesheets = []
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

zone_initial = 89  # JFK
trip_start_initial = -73.79413852703125, 40.65619859765626  # JFK
trip_end_initial = -73.99194061898439, 40.75039170609375  # Manhatten


fig_layout_defaults = dict(
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
)
df_head = pd.read_csv('tabela_atualizada_geolococ.csv')
df_head.fillna('', inplace=True)

select_filtered_md_template = '{:,} entrevistas selecionadas'
select_interviews = select_filtered_md_template.format(len(df_head))

def rename_titles(value):
    if value == []:
        return ''

    options =['ident_Ani_Est', 'map_Arb', 'ident_Atv_trab', 'inf_Ben_Arb',
            'map_Cal_Pass','ident_Cid_Trab', 'map_Cat_via', 'inf_Cuid_Saud',
            'ident_Def_Perm', 'ident_Est_Esc', 'map_Esgo_Sani', 'ident_Est_Civ',
            'ident_Et_Raça', 'ident_Fax_Eta', 'inf_Falt_Agu', 'inf_Fre_Res',
             'inf_Fre_Var', 'map_Ilu_Pub', 'inf_Loc_Laz', 'inf_Loc_Trav',
            'inf_Mei_Tran', 'ident_Pos_Imo', 'ident_Natura', 'inf_Not_Cid',
             'inf_Dei_Res',
            'inf_Ori_Agu', 'inf_Pri_Bair', 'ident_Rend_Ind', 'ident_Res',
             'inf_Res_Dom', 'inf_Sat_Gov', 'inf_Sat_Vid', 'ident_Sex_ide',
            'map_Sit_urb', 'map_Sis_Dre', 'map_Sit_pav']

    names = ['Animal de Estimação', 'Arborização', 'Atividade/Trabalho', 'Bem da Arborização',
     'Calçada/Passeio', 'Cidade em que Trabalha', 'Classificação da Via', 'Cuidados com Saúde',
     'Deficiência Permanente', 'Escolaridade', 'Esgotamento Sanitário', 'Estado Civil',
     'Etnia/Raça', 'Faixa Etária', 'Falta de Água', 'Frequência de Retirada dos Resíduos',
     'Frequência de Varrição da Rua', 'Iluminação Pública', 'Locais de Lazer', 'Locais que Frequenta',
     'Meio de Transporte', 'Moradia', 'Naturalização', 'Notícias da Cidade',
     'Onde Deixa o Resíduo', 'Origem da Água', 'Prioridades Para o Bairro', 'Renda', 'Reside',
     'Resíduos Domésticos', 'Satisfacão com Governo', 'Satisfação Vida', 'Sexo',
     'Sinalização Urbana', 'Sistema de Drenagem', 'Situação da Pavimentação']

    dictionary = dict(zip(names, options))
    flag = dictionary[value]
    return flag



app.layout = html.Div(className='app-body', children=[
    # Stores
    dcc.Store(id='map_clicks', data=0),
    dcc.Store(id='zone', data=zone_initial),
    dcc.Store(id='trip_start', data=trip_start_initial),
    dcc.Store(id='trip_end', data=trip_end_initial),

    # About the app + logos
    html.Div(className="row", children=[
        html.Div(className='twelve columns', children=[
            html.Div(style={'float': 'left'}, children=[
                    html.H1('Relatório Socioterritorial'),
                    html.H4(f'Dados de {len(df_head):} entrevistas realizadas em Santo Antônio da Barra - GO')
                ]
            ),
        ]),
    ]),
    # Control panel
    html.Div(className="row", id='control-panel', children=[
        html.Div(className="seven columns pretty_container", children=[
            dcc.Loading(
                className="loader",
                id="loading",
                type="default",
                children=[
                    html.Div(id='loader-trigger-1', style={"display": "none"}),
                    html.Div(id='loader-trigger-2', style={"display": "none"}),
                    html.Div(id='loader-trigger-3', style={"display": "none"}),
                    html.Div(id='loader-trigger-4', style={"display": "none"}),
                    dcc.Markdown(id='data_summary_filtered', children=select_interviews),
                    html.Progress(id="selected_progress", max=f"{307}", value=f"{len(df_head)}"),
                ]),
        ]),

        html.Div(className="five columns pretty_container", children=[
            html.Label('Selecione um tema'),
            dcc.Dropdown(id='names',
                         placeholder='Select a day of week',
                        options=['Animal de Estimação', 'Arborização', 'Atividade/Trabalho', 'Bem da Arborização',
                                    'Calçada/Passeio','Cidade em que Trabalha', 'Classificação da Via', 'Cuidados com Saúde',
                                    'Deficiência Permanente', 'Escolaridade', 'Esgotamento Sanitário', 'Estado Civil',
                                    'Etnia/Raça', 'Faixa Etária', 'Falta de Água', 'Frequência de Retirada dos Resíduos',
                                     'Frequência de Varrição da Rua', 'Iluminação Pública', 'Locais de Lazer', 'Locais que Frequenta',
                                    'Meio de Transporte', 'Moradia', 'Naturalização', 'Notícias da Cidade',
                                     'Onde Deixa o Resíduo','Origem da Água', 'Prioridades Para o Bairro', 'Renda', 'Reside',
                                     'Resíduos Domésticos', 'Satisfacão com Governo', 'Satisfação Vida', 'Sexo',
                                    'Sinalização Urbana', 'Sistema de Drenagem', 'Situação da Pavimentação'],
                         value=[],
                         ),
        ]),
    ]),

    html.Div(className="row", children=[
    html.Div(className="twelve columns pretty_container", children=[
            dcc.Graph(id='graph'),
        ])
    ]),
    
    html.Div(className="row", children=[
    html.Div(className="twelve columns pretty_container", children=[
            #dcc.Graph(id='geomap_figure'),
            dcc.Loading(id = "loading-icon", children=[html.Div(dcc.Graph(id='geomap_figure'))], type="default")
        ]),

    ]),

    html.Hr()

])

@app.callback(
    Output("graph", "figure"),
    Input("names", "value"))
def generate_chart(value):
    df = pd.read_csv('tabela_atualizada_geolococ.csv')
    df.fillna('', inplace=True)
    flag = rename_titles(value)

    map_func = df[flag].apply(lambda x: pd.Series(x.split('|')).value_counts()).sum()
    map_func.drop('', inplace=True)

    labels = map_func.keys()
    values = map_func.values
    fig = go.Figure(data=[go.Pie(values=values,labels=labels, hole=.3,legendwidth=1)])
    fig.layout = go.Layout(**fig_layout_defaults)
    fig.update_layout(title={
        'text': f'{value}'},title_x=0.5)
    
    fig.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(size= 13), x=0.8))
    #fig.update_layout(margin={"r": 120, "t": 0, "l": 0, "b": 0})

    return fig

@app.callback(
    Output("geomap_figure", "figure"),
    Input("names", "value"))
def generate_chart_map(value):

    df = pd.read_csv('tabela_atualizada_geolococ.csv')
    df.fillna('', inplace=True)
    flag = rename_titles(value)

    columns = df[flag].apply(lambda x: pd.  Series(x.split('|')))
    geo = df[['posLat', 'posLon']].join(columns)
    list_dataframes = []
    for index in range(len(geo.iloc[:, 2:].columns)):
        select = geo[['posLat', 'posLon', index]].dropna()
        select.columns = ['posLat', 'posLon', 'value']
        list_dataframes.append(select)
    table_consolida = pd.concat(list_dataframes)

    df_map = table_consolida.drop(table_consolida[table_consolida['value'] == ''].index)
    df_map = table_consolida.value_counts().reset_index()
    df_map.columns = ['posLat', 'posLon', 'value','cnt']


    fig = px.scatter_mapbox(df_map, lat="posLat", lon="posLon",color='value',size='cnt',zoom=12)
    #fig.update_traces(cluster=dict(enabled=True))
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)', xanchor='center', y=1,x= 0.1))
    fig.update_layout(legend_title="")
    #fig.layout = go.Layout()


    return fig

#app.run_server(debug=True)