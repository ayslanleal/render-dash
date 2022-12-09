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
    options = ['map_Cat_via', 'map_Sit_pav', 'map_Sit_urb', 'map_Cal_Pass',
               'map_Ilu_Pub', 'map_Arb', 'ident_Sex_ide', 'ident_Natura',
               'ident_Fax_Eta', 'ident_Et_Raça', 'ident_Est_Civ', 'ident_Est_Esc',
               'ident_Def_Perm', 'ident_Res', 'ident_Ani_Est', 'ident_Pos_Imo',
               'ident_Atv_trab', 'ident_Cid_Trab', 'ident_Rend_Ind', 'inf_Not_Cid',
               'inf_Loc_Trav', 'inf_Pri_Bair', 'inf_Cuid_Saud', 'inf_Loc_Laz',
               'inf_Res_Dom', 'inf_Dei_Res', 'inf_Fre_Res', 'inf_Fre_Var',
               'inf_Ben_Arb', 'inf_Ori_Agu', 'inf_Falt_Agu', 'inf_Mei_Tran',
               'inf_Sat_Vid', 'inf_Sat_Gov', 'map_Sis_Dre', 'map_Esgo_Sani']

    names = ['Classificação da Via', 'Situação da Pavimentação', 'Sinalização Urbana', 'Calçada/Passeio',
             'Iluminação Pública', 'Arborização', 'Masculino', 'Naturalização',
             'Faixa Etária', 'Etnia/Raça', 'Estado Civil', 'Escolaridade',
             'Deficiência Permanente', 'Reside', 'Animal de Estimação', 'Moradia',
             'Atividade/Trabalho', 'Cidade em que Trabalha', 'Renda', 'Noticias da Cidade',
             'Local que Frequenta', 'Prioridades Bairro', 'Cuidados com Saúde', 'Locais de Lazer',
             'Resíduos Domésticos', 'Onde deixa o Resíduo', 'Frequência de retirada dos Resíduos',
             'Frequência de Varrição da Rua',
             'Bem da Arborização', 'Origem da Água', 'Falta de Água', 'Meio de Transportes',
             'Satisfação Vida', 'Satisfação Governo', 'Sistema de Drenagem', 'Esgotamento Sanitário']

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
                        options=['Classificação da Via', 'Situação da Pavimentação', 'Sinalização Urbana', 'Calçada/Passeio',
                            'Iluminação Pública', 'Arborização', 'Sexo', 'Naturalização',
                            'Faixa Etária', 'Etnia/Raça', 'Estado Civil', 'Escolaridade',
                            'Deficiência Permanente', 'Reside', 'Animal de Estimação', 'Moradia',
                            'Atividade/Trabalho', 'Cidade em que Trabalha', 'Renda', 'Noticias da Cidade',
                            'Local que Frequenta', 'Prioridades Bairro', 'Cuidados com Saúde', 'Locais de Lazer',
                            'Resíduos Domésticos', 'Onde deixa o Resíduo', 'Frequência de retirada dos Resíduos',
                            'Frequência de Varrição da Rua',
                            'Bem da Arborização', 'Origem da Água', 'Falta de Água', 'Meio de Transportes',
                            'Satisfação Vida', 'Satisfação Governo', 'Sistema de Drenagem', 'Esgotamento Sanitário'],
                         value='Etnia/Raça',
                         ),
        ]),
    ]),

    html.Div(className="row", children=[
    html.Div(className="seven columns pretty_container", children=[
            dcc.Graph(id='geomap_figure'),
        ]),
        html.Div(className="five columns pretty_container", children=[
            dcc.Graph(id='graph'),
        ])
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
    fig = go.Figure(data=[go.Pie(values=values,labels=labels, hole=.3)])
    fig.update_layout(title={
        'text': f'{value}'},title_x=0.5)

    fig.layout = go.Layout(**fig_layout_defaults)
    return fig

@app.callback(
    Output("geomap_figure", "figure"),
    Input("names", "value"))
def generate_chart_map(value):

    df = pd.read_csv('tabela_atualizada_geolococ.csv')
    df.fillna('', inplace=True)
    flag = rename_titles(value)

    columns = df[flag].apply(lambda x: pd.Series(x.split('|')).fillna(''))
    geo = df[['posLat', 'posLon']].join(columns)
    list_dataframes = []
    for index in range(len(geo.iloc[:, 2:].columns)):
        select = geo[['posLat', 'posLon', index]].dropna()
        select.columns = ['posLat', 'posLon', 'value']
        list_dataframes.append(select)

    table_consolida = pd.concat(list_dataframes)
    df_map = table_consolida.value_counts().reset_index()
    df_map.columns = ['posLat', 'posLon', 'value','cnt']


    fig = px.scatter_mapbox(df_map, lat="posLat", lon="posLon",color='value',size='cnt',zoom=12)
    #fig.update_traces(cluster=dict(enabled=True))
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(legend=dict(bgcolor='rgba(0,0,0,0)'))
    #fig.update_layout(legend_title="")
    #fig.layout = go.Layout()


    return fig


app.run_server(debug=True)