import mysql.connector
import pandas as pd
import numpy as np

def datos(fecha_inicio, fecha_fin):
    mydb = mysql.connector.connect(
    host="pronosticodds-rds.cluster-c3lv3tcn13lr.us-west-2.rds.amazonaws.com",
    port=3306,
    user="datamanager",
    password="8J=LGCTHuQx,M4UZ",
    database='pronosticodds'
    )

    # Coloque la fecha para la cual desea conocer los pronosticos
   # fecha_inicio = '2021-08-16'
   # fecha_fin = '2021-08-25'

    mycursor = mydb.cursor()

    sql = "SELECT \
                f.date, d.name, c.name, g.title, ft.name, f.logro, t.name, ca.name, f.cuota, f.stake, f.parent_id, f.plan, f.acierto \
            FROM forecasts f \
            LEFT JOIN games g ON (f.game_id = g.id) \
            LEFT JOIN competitions c ON (g.competition_id = c.id) \
            LEFT JOIN disciplines d ON (c.discipline_id = d.id) \
            LEFT JOIN forecast_types ft ON (ft.id = f.forecast_type_id) \
            LEFT JOIN casa_apuestas ca ON (ca.id = f.casa_apuesta_id) \
            LEFT JOIN teams t ON (t.id = f.team_id) \
            WHERE f.`date` BETWEEN %s AND %s"

    fecha = (fecha_inicio, fecha_fin)

    mycursor.execute(sql, fecha)  # aca ejecutamos el codigo MySQL

    myresult = mycursor.fetchall()

    df = pd.DataFrame(myresult, columns = ['fecha', 'deporte', 'competicion','equipos', 'apuesta_a', 'logro', 'equipo', 'casa_apuesta',
                                        'cuota', 'stake', 'parent_id', 'plan', 'acierto'])

    df['plan'].replace({'price_1Ie1g8H07k7IB2uwHUBnheIK' : 'Gold', 
                        'price_1J9sF4H07k7IB2uwK4Cv0ZBm' : 'Silver',
                        'price_1Ie1f0H07k7IB2uwsyf4m7GI' : 'Bronze', 
                        'price_1JCSHlH07k7IB2uw1u0aAMYk' : 'Trial', 
                        'plan_H6PDCQbTsjQhIy' : 'Special'}, 
                        inplace = True)

    #La Jugada del dia: price_1JCSHlH07k7IB2uw1u0aAMYk
    #Deportes Generales:  price_1J9sF4H07k7IB2uwK4Cv0ZBm
    # Hipismo: price_1J9sF4H07k7IB2uw8vlb4BZC

    df['cuota'] = pd.to_numeric(df['cuota'])

    df.loc[df['cuota'] > 0, 'cuota'] =  round(1 + (df.loc[df['cuota'] > 0, 'cuota']/100), 2)
    df.loc[df['cuota'] < 0, 'cuota'] =  round((abs(100/df.loc[df['cuota'] < 0, 'cuota'])) + 1, 2)

    df[['home_team', 'away_team']] = df['equipos'].str.split("vs", expand=True)
    df.drop(['equipos'], axis = 1, inplace = True)

    df['home_team'] = df['home_team'].str.strip()
    df['away_team'] = df['away_team'].str.strip()

    df['tipo'] = np.where(df['cuota']>= 1.98, 'Hembra', 'Macho')

    df['apuesta'] = 100

    df = df[['fecha', 'deporte', 'competicion', 'home_team', 'away_team', 'apuesta_a', 'logro', 'equipo',
            'tipo', 'cuota', 'casa_apuesta', 'stake', 'plan', 'parent_id', 'apuesta', 'acierto']]

    # tomamos los id unicos en parent id
    unique_parent = df['parent_id'].unique()

    # vamos a eliminar el nan, si existe. Si no existe, no elimina nada
    nan_o_no = np.isnan(df['parent_id'].unique())
    unique_parent = np.delete(unique_parent, np.where(nan_o_no))

    # vamos a eliminar el 0.0 que esta en la lista de unique_parent
    unique_parent = np.delete(unique_parent, np.where(unique_parent == 0.0))

    for idx in unique_parent:
        df.loc[df['parent_id'] == idx, ['apuesta']] = 0
        #df.loc[df['parent_id'] == idx, ['cuota']] = ''
        df.loc[df['parent_id'] == idx, ['plan']] = ''


    return df