# Prueba
# http://127.0.0.1:8050/

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ---------------------------------------------------------------------------------------------------------------
# Iniciamos la aplicacion
app = dash.Dash(__name__)

# ---------------------------------------------------------------------------------------------------------------
# Importamos la data, en este caso la tenemos en un csv
df = pd.read_csv('intro_bees.csv')

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
#print(df[:5])
print("Las columnas son:")
print(df.columns)
# ---------------------------------------------------------------------------------------------------------------
# Ahora, comenzamos con el layout del app

# Todo lo necesario va dentro del layout
app.layout = html.Div([
    html.H1('Primera aplicacion hecha con Dash', style={'text-align' : 'center'}),

    # Agregamos un componente de Dash, que en este caso sera un dropdown
    dcc.Dropdown(id='slct_year',
                 options=[
                     {'label' : '2015', 'value' : 2015},
                     {'label' : '2016', 'value' : 2016},
                     {'label' : '2017', 'value' : 2017},
                     {'label' : '2018', 'value' : 2018}],
                 multi=False,
                 value=2015,
                 style={'width' : '40%'}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(), # agregamos una linea o espacio

    dcc.Graph(id='my_bee_map', figure={})
])

# -------------------------------------------------------------------------------------------
# Ahora vamos a conectar los compnentes creados con los graficos de Plotly y la data

@app.callback(
    [Output(component_id='output_container', component_property='children'),  # Vamos a tener tantos Outputs como elementos
    Output(component_id='my_bee_map', component_property='figure')],      # necesitemos. En este caso devolveremos el contenedor
    [Input(component_id='slct_year', component_property='value')]                # y el grafico
)         # Para el input vamos a seleccionar el id del dropdown y lo que queremos variar son los valores
        # por eso la propiedad a variar del dropdown es el value

# Ahora vamos a crear una funcion. Esta funcion tendra tantos argumentos como Inputs en el callback tengamos
def update_graph(option_slctd):  # aca estamos haciendo referencia al value o a la opcion escogida
    print(option_slctd)
    #print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
   # dff = dff[dff["Year"] == option_slctd] # filtramos por la opcion seleccionada
   # dff = dff[dff["Affected by"] == "Varroa_mites"] # filtramos por la enfermedad


    # Plotly Express es la libreria que nos hace los graficos
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    return container, fig  # La cantidad de Outputs que tenga es la cantidad de elementos a retornar

# -------------------------------------------------------------------------------------------
# Correr el sistema

if __name__ == '__main__':
    app.run_server(debug=True)