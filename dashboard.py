import dash
from dash import dcc
from dash import html 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

CENTER_LAT, CENTER_LON = -9.66625,  -35.7351

# =====================================================================

# Data Generation

# df = pd.read_csv("HIST_PAINEL_COVIDBR_13mai2021.csv", sep=";")
# df_states = df[~df["estado"].isna() & (df["codmun"].isna())] # uso do " ~ " --> quando não for NAN
# df_brasil = df[df["regiao"] == "Brasil"]

# df_states.to_csv("df_states.csv")
# df_brasil.to_csv("df_brasil.csv")

# =====================================================================

df_states = pd.read_csv("df_states.csv", sep =",")
df_brasil = pd.read_csv("df_brasil.csv", sep =",")

df_states_ = df_states[df_states["data"] == "2020-05-13"] # nobvo df states, data inicial
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))
df_data = df_states[df_states["estado"] == "RJ"]

select_columns = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por dia"}

# ========================================
# Instanciando o Dash

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.COSMO]) # onde vai ficar acoplado meu dashboard
server = app.server

fig = px.choropleth_mapbox(df_states_, locations="estado",
    geojson=brazil_states, center={"lat": -16.95, "lon": -47.78}, # https://www.google.com/maps/ -> right click -> get lat/lon
    zoom=4, color="casosNovos", color_continuous_scale="Redor", opacity=0.4,
    hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True}
    )
# locations --: coluna do df que vai casar com geojson
# usar states_ --> 
# hover_data o que mostrar ao passar o cursor por cima.

fig.update_layout(
                # mapbox_accesstoken=token,
                paper_bgcolor="#a8d5e5", # cor do projeto
                autosize = True, # auto ajustar seu tamanho
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                mapbox_style="open-street-map",
                showlegend=False,
              )


fig2 = go.Figure(layout={"template" : "simple_white"})
fig2.add_trace(go.Scatter(
    x= df_data["data"],
    y = df_data["casosAcumulado"]
))

#go.scatter -- gráfico de pontos

fig2.update_layout(
                paper_bgcolor="#a8d5e5",#cor do projeto
                plot_bgcolor="#a8d5e5",  # cor do fundo
                autosize = True, # auto ajustar seu tamanho
                margin=go.layout.Margin(l=10, r=10, t=10, b=10),
              )


# ========================================
# Contrução do layout do Dash
# src : localização do objeto
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
            html.Img(id="logo",src=app.get_asset_url("logo_dark.png"), height= 50),
            html.H5("Evolução Covid 19"),
            dbc.Button("BRASIL", color = "primary", id ="location-button", size="lg")
            ],style={"background-color": "#1E1E1E", "margin": "-25px", "padding": "25px"}),
            html.P("Informe a data na qual deseja obter informações:", style= {"margin-top": "40px"}),
            html.Div(
                className="div-for-dropdown",
                id = "div-test",
                children=[
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed= df_brasil["data"].min(),
                    max_date_allowed= df_brasil["data"].max(),
                    date= df_brasil["data"].max(),# data que quero selecionar
                    initial_visible_month=df_brasil["data"].min(),  # Mês inicial visível
                    display_format= "MMMM D, YYYY",
                    style={"border":"0px solid black"},
                    )
                ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos recuperados"),
                            html.H3(style={"color":"#adfc92"}, id="casos-recuperados-text"),
                            html.Span("Em acompanhamento"),
                            html.H5(id="em-acompanhamento-text"),
                        ])
                    ], color = "light", outline= True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF","background-color": "#2a2a2a", "border": "none"})
                ], md= 4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos confirmados totais"),
                            html.H3(style={"color":"#389fd6"}, id="casos-confirmados-text"),
                            html.Span("Novos casos na data"),
                            html.H5(id="novos-casos-text"),
                        ])
                    ], color = "light", outline= True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF","background-color": "#2a2a2a", "border": "none"})
                ], md= 4),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Óbitos confirmados"),
                            html.H3(style={"color":"#DF2935"}, id="obitos-text"),
                            html.Span("Óbitos na data"),
                            html.H5(id="obitos-na-data-text"),
                        ])
                    ], color = "light", outline= True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF","background-color": "#2a2a2a", "border": "none"})
                ], md= 4),
            ]),
                html.Div([
                    html.P("Selecione que tipo de dado deseja visualizar:", style= {"margin-top": "25px"}),
                    dcc.Dropdown(id="location-dropdown",
                                 options= [{"label":j, "value":i} for i,j in select_columns.items()],
                                 value="casosNovos",
                                 style={"margin-top": "10px"}
                                 ),
                    dcc.Graph(id="line-graph", figure = fig2) 
                ])
             
        ], md = 5, style={"padding": "25px","background-color": "#242424"}),
        
        dbc.Col([
            dcc.Loading(id="loading-1", type="default",
                        children=[ dcc.Graph(id="choropleth-map", figure = fig, style = {"height": "100vh", "margin-right":"10px"})])
             
        ], md = 7)  
    ])
, fluid=True)


# =====================================================================
# Interactivity

@app.callback(
    [
        Output("casos-recuperados-text", "children"),
        Output("em-acompanhamento-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children"),
    ],
    [Input("date-picker","date"), Input("location-button", "children")]
    ) 
def display_status(date, location):
    if location == "BRASIL":
        df_data_on_date = df_brasil[df_brasil["data"]==date]
    else:
        df_data_on_date = df_states[(df_states["estado"]==location) & (df_states["data"]==date)]
        
    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".")
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0]  else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".") 
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".") 
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0]  else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".") 
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".") 
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0]  else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".") 
    
    return (
            recuperados_novos, 
            acompanhamentos_novos, 
            casos_acumulados, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos,
            )


@app.callback(
    Output("line-graph", "figure"),
   [ 
    Input("location-dropdown", "value"),
    Input("location-button", "children")
    ]
)
def plot_line_graph(plot_type, location):
    
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_states[(df_states["estado"] == location)]
    
    bar_plots = ["casosNovos", "obitosNovos"]
    
    fig2  = go.Figure(layout={"template" : "simple_white"})
    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
        
    fig2.update_layout(
                paper_bgcolor="#a8d5e5",#cor do projeto
                plot_bgcolor="#a8d5e5",  # cor do fundo
                autosize = True, # auto ajustar seu tamanho
                margin=go.layout.Margin(l=10, r=10, t=10, b=10),
              )
    return fig2


@app.callback(
    Output("choropleth-map", "figure"), 
    [Input("date-picker", "date")]
)    
def update_map(date):
    df_data_on_states = df_states[df_states["data"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=brazil_states, 
        center={"lat": CENTER_LAT, "lon": CENTER_LON},  # https://www.google.com/maps/ -> right click -> get lat/lon
        zoom=4, color="casosAcumulado", color_continuous_scale="Redor", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": False}
        )

    fig.update_layout(paper_bgcolor="#a8d5e5", mapbox_style="open-street-map", autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig

@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    
    else:
        return "BRASIL"   
    
if __name__ == "__main__":
    app.run_server(debug=True)

