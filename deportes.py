from data import datos
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
#from datetime import datetime import timedelta

# ---------------------------------------------------------------------------------------------------------------
# Llamada a la funcion que nos da la data

# Coloque la fecha para la cual desea conocer los pronosticos
#fecha_inicio = '2021-08-16'
#fecha_fin = '2021-08-22'
#df = datos(fecha_inicio, fecha_fin)
#print(df.tail())


# ---------------------------------------------------------------------------------------------------------------
# Iniciamos la aplicacion
app = dash.Dash(__name__)

# ---------------------------------------------------------------------------------------------------------------
# Todo lo necesario va dentro del layout

# Al existir una combinada en deportes se asigna un None, es por ello que para ver la cantidad de aciertos
# en cada uno de los deportes vamos a eliminar las filas en las que deporte es igual a None
#df_deportes = df.dropna(subset=['deporte'])
#deportes = df_deportes['deporte'].unique()  # Tomamos los deportes

deportes = ['Soccer', 'Tennis', 'Baseball', 'Basketball', 'Ice Hockey', 'Fighting', 'American Football']
print(deportes)



app.layout = html.Div([
    html.H1('Dashboard de PronosticOdds', style={'text-align' : 'center'}),
    
    html.Br(),

    html.H2('Aciertos Totales y por Plan', style={'text-align' : 'center'}),
    
    html.Div([
        html.P('Seleccione un rango de fecha', className = 'fix_label'),
        dcc.DatePickerRange(
            id='my-date-picker-range',  # ID to be used for callback
            calendar_orientation='horizontal',  # vertical or horizontal
            day_size=25,  # size of calendar image. Default is 39
            start_date_placeholder_text = "Fecha Inicio",
            end_date_placeholder_text="Fecha Fin",  # text that appears when no end date chosen
            with_portal=False,  # if True calendar will open in a full screen overlay portal
            first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
            reopen_calendar_on_clear=True,
            is_RTL=False,  # True or False for direction of calendar
            clearable=True,  # whether or not the user can clear the dropdown
            number_of_months_shown=1,  # number of months shown when calendar is open
            min_date_allowed=dt(2021, 6, 1),  # minimum date allowed on the DatePickerRange component
            max_date_allowed=dt(dt.today().year, dt.today().month, dt.today().day).date(),  #datetime.today()+timedelta(days=-1) # maximum date allowed on the DatePickerRange component
            initial_visible_month=dt(dt.today().year, dt.today().month, 1).date(),  # the month initially presented when the user opens the calendar
            start_date=dt(dt.today().year, dt.today().month, 1).date(),
            end_date=dt(dt.today().year, dt.today().month, dt.today().day).date(),
            display_format='D MMM, YY',  # how selected dates are displayed in the DatePickerRange component.
            month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
            minimum_nights=0,  # minimum number of days between start and end date

            # Estas tres lineas indican que guardar y cuanto tiempo la fecha introducida por el usuario
            persistence=True,  
            persisted_props=['start_date'],
            persistence_type='session',  # session, local, or memory. Default is 'local'

            updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
        )
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id='df_trial', figure={})
        ], style={'display' : 'inline-block', 'float' : 'left', 'width': '25%'}),

        html.Div([
            dcc.Graph(id='df_silver', figure={}),
        ], style={'display' : 'inline-block', 'float' : 'rigth', 'width': '25%'}),

        html.Div([
            dcc.Graph(id='df_total', figure={}),
        ], style={'display' : 'inline-block', 'float' : 'left', 'width': '50%'}),

    ]),


    html.Br(),
    html.H2('Aciertos por deporte y fecha', style={'text-align' : 'center'}),

    html.Br(),

    html.Div([
        html.Div([
            html.P('Seleccione un Deporte', className = 'fix_label'),
            # Agregamos un componente de Dash, que en este caso sera un dropdown
            dcc.Dropdown(id='slc_deporte',
                        options=[{'label' : i , 'value' : i} for i in deportes],
                        multi=False,
                        value='Soccer',   # Valor que se ve por defecto
                        clearable=False,
                        style={'width' : '40%'}
            )
        ], style={'width': '62%', 'display': 'inline-block'})
    ]),

    html.Br(), # agregamos una linea o espacio
    dcc.Graph(id='acierto_deportes', figure={}),
    dcc.Graph(id='acierto_fechas', figure={}),
    html.Br(),

# Dropdown para aciertos por competiciones

   # html.Div([
   #     html.P('Seleccione una Competicion', className = 'fix_label'),
        # Agregamos un componente de Dash, que en este caso sera un dropdown
   #     dcc.Dropdown(id='slc_competiciones',
   #             options=[{'label' : i , 'value' : i} for i in competiciones],
   #             multi=False,
   #             value='ATP World Tour',   # Valor que se ve por defecto
   #             clearable=False,
   #             style={'width' : '40%'}
   #     )
   # ], style={'width': '62%', 'display': 'inline-block'})

])


# -------------------------------------------------------------------------------------------
# Ahora vamos a conectar los compnentes creados con los graficos de Plotly y la data

@app.callback(
    [Output(component_id='acierto_deportes', component_property='figure'),
     Output(component_id='acierto_fechas', component_property='figure'),
     Output(component_id='df_silver', component_property='figure'),
     Output(component_id='df_trial', component_property='figure'),
     Output(component_id='df_total', component_property='figure')],
    [Input(component_id='slc_deporte', component_property='value'),
     Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date')]
)
 
# ----------------------------------------------------------------------------------------------------------------
# Ahora vamos a crear una funcion. Esta funcion tendra tantos argumentos como Inputs en el callback tengamos
def update_graph(value, start_date, end_date):  # aca estamos haciendo referencia al value o a la opcion escogida
    #print(option_slctd)

    df = datos(str(start_date), str(end_date))
    print(df.head())

    df_deportes = df.dropna(subset=['deporte'])

    df_temp = df_deportes[df_deportes['deporte'] == value]  # Filtramos por deporte
    df_temp.head()

    repeticiones_fecha = df_temp.groupby(['fecha']).size()  # con esto obtenemos el total de veces que aparece una misma fecha

    aciertos_fecha = df_temp.groupby(['fecha', 'acierto'], as_index=False).size() # Vemos los aciertos, fallos y nulos por fecha
    aciertos_fecha = aciertos_fecha.pivot(index="fecha", columns="acierto", values="size")  # Transformamos los aciertos a columna y le  
                                                                                          # asignamos como valor el size
    aciertos_fecha = aciertos_fecha.fillna(0)  # Reemplazamos los NaN por un cero
    aciertos_fecha['total'] = repeticiones_fecha   # Agregamos el total por fecha

    # Cambiamos el nombre de las columnas
    if -1 in aciertos_fecha.columns and 0 in aciertos_fecha.columns and 1 in aciertos_fecha.columns:
        aciertos_fecha.columns = ['nulos', 'fallados', 'acertados', 'total']

        # Construimos el data frame final
        df_final = pd.DataFrame(index=['acertados', 'fallados', 'nulos'], columns = ['total'])
        df_final.loc['acertados'] = aciertos_fecha['acertados'].sum()
        df_final.loc['fallados'] = aciertos_fecha['fallados'].sum()
        df_final.loc['nulos'] = aciertos_fecha['nulos'].sum()
        
    elif -1 in aciertos_fecha.columns and 0 in aciertos_fecha.columns and 1 not in aciertos_fecha.columns:
        aciertos_fecha.columns = ['nulos', 'fallados', 'total']

        # Construimos el data frame final
        df_final = pd.DataFrame(index=['fallados', 'nulos'], columns = ['total'])
        df_final.loc['fallados'] = aciertos_fecha['fallados'].sum()
        df_final.loc['nulos'] = aciertos_fecha['nulos'].sum()

    elif -1 in aciertos_fecha.columns and 0 not in aciertos_fecha.columns and 1 not in aciertos_fecha.columns:
        aciertos_fecha.columns = ['nulos', 'total']

        # Construimos el data frame final
        df_final = pd.DataFrame(index=['nulos'], columns = ['total'])
        df_final.loc['nulos'] = aciertos_fecha['nulos'].sum() 

    elif -1 not in aciertos_fecha.columns and 0 in aciertos_fecha.columns and 1 not in aciertos_fecha.columns:
        aciertos_fecha.columns = ['fallados', 'total']

        # Construimos el data frame final
        df_final = pd.DataFrame(index=['fallados'], columns = ['total'])
        df_final.loc['fallados'] = aciertos_fecha['fallados'].sum() 

    elif -1 not in aciertos_fecha.columns and 0 not in aciertos_fecha.columns and 1 in aciertos_fecha.columns:
        aciertos_fecha.columns = ['acertados', 'total']

        # Construimos el data frame final
        df_final = pd.DataFrame(index=['acertados'], columns = ['total'])
        df_final.loc['acertados'] = aciertos_fecha['acertados'].sum()

    elif -1 in aciertos_fecha.columns and 0 not in aciertos_fecha.columns and 1 not in aciertos_fecha.columns:
        aciertos_fecha.columns = ['nulos', 'acertados', 'total']

        # Construimos el data frame final
        df_final = pd.DataFrame(index=['acertados', 'nulos'], columns = ['total'])
        df_final.loc['acertados'] = aciertos_fecha['acertados'].sum()
        df_final.loc['nulos'] = aciertos_fecha['nulos'].sum()

    elif -1 not in aciertos_fecha.columns and 0 in aciertos_fecha.columns and 1 in aciertos_fecha.columns:
        aciertos_fecha.columns = ['fallados', 'acertados', 'total']

        # Construimos el data frame final
        df_final = pd.DataFrame(index=['acertados', 'fallados'], columns = ['total'])
        df_final.loc['acertados'] = aciertos_fecha['acertados'].sum()
        df_final.loc['fallados'] = aciertos_fecha['fallados'].sum()   

    print(df_final)

    # Plotly Express es la libreria que nos hace los graficos
    fig1 = px.pie(
        df_final, 
        values='total'
        #title='Acierto por Deporte'
    )
    #fig.update_traces(labels = df_acierto.index, textposition='inside', textinfo='percent+label')
    fig1.update_traces(labels = df_final.index, textinfo='label+percent', hoverinfo='skip')


    #---------------------------------------------------------------------------------------------------
    # Grafico de barra para los aciertos por dia
    fig2 = px.bar(aciertos_fecha, x=aciertos_fecha.index, y=aciertos_fecha.columns, barmode="group")
    fig2.update_xaxes(type='category')

    #----------------------------------------------------------------------------------------------------
    # Vamos a hacer el group_by para sacar los graficos para los aciertos totales y por plan
    #temp = datos(str(inicio), str(fin))

    # Hacemos las transformaciones necesarias
    temp = df.groupby(['plan', 'acierto'], as_index=False).size()   # agrupamos
    temp = temp.pivot(index="plan", columns="acierto", values="size")  # pivoteamos
    temp = temp.fillna(0)  # llenamos los NaN con 0
    temp['total'] = temp.sum(axis=1)  # Sacamos la suma total por fila, es decir, por plan

    if -1 in temp.columns:
        temp.columns = ['nulos', 'fallados', 'acertados', 'total']
        
        df_silver = pd.DataFrame(index=['acertados', 'fallados', 'nulos'], columns = ['total'])
        df_silver.loc['acertados'] = temp['acertados']['Silver']
        df_silver.loc['fallados'] = temp['fallados']['Silver']
        df_silver.loc['nulos'] = temp['nulos']['Silver']
        
        df_trial = pd.DataFrame(index=['acertados', 'fallados', 'nulos'], columns = ['total'])
        df_trial.loc['acertados'] = temp['acertados']['Trial']
        df_trial.loc['fallados'] = temp['fallados']['Trial']
        df_trial.loc['nulos'] = temp['nulos']['Trial']

        df_total = pd.DataFrame(index=['acertados', 'fallados', 'nulos'], columns = ['total'])
        df_total.loc['acertados'] = temp['acertados']['Silver'] + temp['acertados']['Trial']
        df_total.loc['fallados'] = temp['fallados']['Silver'] + temp['fallados']['Trial'] 
        df_total.loc['nulos'] = temp['nulos']['Silver'] + temp['nulos']['Trial']



    elif 1 not in temp.columns or 0 not in temp.columns: 
        temp.columns = ['total']
        
        df_silver = pd.DataFrame(index=['acertados', 'fallados'], columns = ['total'])
        df_silver.loc['acertados'] = 0.0
        df_silver.loc['fallados'] = 0.0
        
        df_trial = pd.DataFrame(index=['acertados', 'fallados'], columns = ['total'])
        df_trial.loc['acertados'] = 0.0
        df_trial.loc['fallados'] = 0.0

        df_total = pd.DataFrame(index=['acertados', 'fallados'], columns = ['total'])
        df_total.loc['acertados'] = 0.0
        df_total.loc['fallados'] = 0.0

    else:    # quiere decir que dentro de esa fecha no hubo ninguna jugada nula 
        temp.columns = ['fallados', 'acertados', 'total']
        
        df_silver = pd.DataFrame(index=['acertados', 'fallados'], columns = ['total'])
        df_silver.loc['acertados'] = temp['acertados']['Silver']
        df_silver.loc['fallados'] = temp['fallados']['Silver']
        
        df_trial = pd.DataFrame(index=['acertados', 'fallados'], columns = ['total'])
        df_trial.loc['acertados'] = temp['acertados']['Trial']
        df_trial.loc['fallados'] = temp['fallados']['Trial']

        df_total = pd.DataFrame(index=['acertados', 'fallados'], columns = ['total'])
        df_total.loc['acertados'] = temp['acertados']['Silver'] + temp['acertados']['Trial']
        df_total.loc['fallados'] = temp['fallados']['Silver'] + temp['fallados']['Trial'] 

    #print(df_silver)
    #print(df_trial)
    #print(df_total)

    # Hacemos los graficos
    fig3 = px.pie(
        df_total, 
        values='total',
        title='Aciertos Totales'
    )
    fig3.update_traces(labels = df_total.index, textinfo='label+percent', hoverinfo='skip', textposition='inside')
    
    fig4 = px.pie(
        df_silver, 
        values='total',
        title='Aciertos Plan Sport'
    )
    fig4.update_traces(labels = df_silver.index, textinfo='label+percent', hoverinfo='skip', textposition='inside')
    
    fig5 = px.pie(
        df_trial, 
        values='total',
        title='Aciertos Jugada del dia'
    )
    fig5.update_traces(labels = df_trial.index, textinfo='label+percent', hoverinfo='skip', textposition='inside')


    return fig1, fig2, fig3, fig4, fig5  # La cantidad de Outputs que tenga es la cantidad de elementos a retornar


# -------------------------------------------------------------------------------------------
# Correr el sistema

if __name__ == '__main__':
    app.run_server(debug=True)




