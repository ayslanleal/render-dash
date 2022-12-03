from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Relatório Socioterritorial'),
    dcc.Dropdown(id='names',
                 options=['Classificação da Via', 'Situação da Pavimentação', 'Sinalização Urbana', 'Calçada/Passeio',
             'Iluminação Pública', 'Arborização', 'Masculino', 'Naturalização',
             'Faixa Etária', 'Etnia/Raça', 'Estado Civil', 'Escolaridade',
             'Deficiência Permanente', 'Reside', 'Animal de Estimação', 'Moradia',
             'Atividade/Trabalho', 'Cidade em que Trabalha', 'Renda', 'Noticias da Cidade',
             'Local que Frequenta', 'Prioridades Bairro', 'Cuidados com Saúde', 'Locais de Lazer',
             'Resíduos Domésticos', 'Onde deixa o Resíduo', 'Frequência de retirada dos Resíduos',
             'Frequência de Varrição da Rua',
             'Bem da Arborização', 'Origem da Água', 'Falta de Água', 'Meio de Transportes',
             'Satisfação Vida', 'Satisfação Governo', 'Sistema de Drenagem', 'Esgotamento Sanitário'],
                 value='Classificação da Via',
                 clearable=False
                 ),
    dcc.Graph(id="graph")
])


@app.callback(
    Output("graph", "figure"),
    Input("names", "value"))
def generate_chart(value):
    df = pd.read_csv('value.csv') # replace with your own data source
    df.fillna('', inplace=True)

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

    map_func = df[flag].apply(lambda x: pd.Series(x.split('|')).value_counts()).sum()
    map_func.drop('', inplace=True)

    labels = map_func.keys()
    values = map_func.values
    fig = go.Figure(data=[go.Pie(values=values,labels=labels, hole=.3)])
    fig.update_layout(title={
        'text': f'{value}'},title_x=0.5)
    return fig


app.run_server(debug=True)