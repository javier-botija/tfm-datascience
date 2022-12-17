import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import globals as gb


def damefecha(mrow):
    mfechastr = "01/01/" + str(int(mrow.Year))
    mfecha = pd.to_datetime(mfechastr)
    return mfecha


def dameEsp(mrow):
    mEsp = ("00" + str(mrow.Indicador))[-3:] + " " + str(mrow.Ind_Esp)
    return mEsp


def recorre_ficheros_indices():
    ficheros = os.listdir(gb.pathCSVsIndex)
    for fich in ficheros:
        importa_fichero_indices(gb.pathCSVsIndex, fich)


def recorre_ficheros_econ():
    ficheros = os.listdir(gb.pathCSVsEcon)
    for fich in ficheros:
        if fich[0:7] == 'T0003_C':
            importa_fichero_econs(gb.pathCSVsEcon, fich)

def recorre_ficheros_airbnb():
    importa_fichero_airbnb(gb.pathCSVsAirbnb + gb.filebnb2018, 2018)
    importa_fichero_airbnb(gb.pathCSVsAirbnb + gb.filebnb2019, 2019)
    importa_fichero_airbnb(gb.pathCSVsAirbnb + gb.filebnb2021, 2021)
    importa_fichero_airbnb(gb.pathCSVsAirbnb + gb.filebnb2022, 2022)

def recorre_ficheros_pisos_turisticos():
    importa_fichero_pisosturisticos(gb.pathCSVsAirbnb + gb.filepisosturisticos, 4, 2018)


def recorre_ficheros_renta():
    ficheros = os.listdir(gb.pathCSVsRenta)
    for fich in ficheros:
        if fich[0:6] == 'Barris':
            importa_fichero_renta(gb.pathCSVsRenta, fich)


def importa_fichero_indices(directorio, fich):
    global df_dest
    df = pd.read_csv(directorio + fich, sep=';')
    for index, row in df.iterrows() :
        for column in [col for col in df.columns if col.find("Valor ") >= 0]:
            df_dest = df_dest.append({'DT': row['DT'],
                                      'DTBA': row['DTBA'],
                                      'Indicator': row['Indicador'],
                                      'Year': column.replace('Valor ', ''),
                                      'Value': row[column]}, ignore_index=True)


def importa_fichero_econs(directorio, fich):
    global df_dest
    df = pd.read_csv(directorio + fich, sep=';', skiprows=2, encoding="ISO-8859-1", thousands='.')
    if df.columns[3] == 'Total':
        colini = 4
    else:
        colini = 3
    Yearfich = fich.replace('.csv','').replace('T0003_C ','')
    for index, row in df.iterrows():
        if row['Barrio'].is_integer():
            DTBA = str(int(row['Distrito'])) + str(int(row['Barrio']))
            if colini == 3 :
                ValueTot = int(row[3]) + int(row[4]) + int(row[5]) + int(row[6])
            else :
                ValueTot = int(row['Total'])
            df_dest = df_dest.append({'DT': row['Distrito'],
                                      'DTBA': DTBA,
                                      'Indicator': 200,
                                      'Year': Yearfich,
                                      'Value': ValueTot}, ignore_index=True)
            for col in range(4):
                df_dest = df_dest.append({'DT': row['Distrito'],
                                          'DTBA': DTBA,
                                          'Indicator': 201+col,
                                          'Year': Yearfich,
                                          'Value': row[colini+col]}, ignore_index=True)


def importa_fichero_airbnb(fich, Yearfich):
    global df_dest
    gdf_barrios = gpd.read_file(gb.pathCSVsOther + gb.fileBarrios)
    gdf_barrios.insert(0, "DTBA", pd.to_numeric(gdf_barrios.coddistbar, downcast='integer'), True)

    gdf_puntos = gpd.read_file(fich)
    gdf_puntos = gdf_puntos[(gdf_puntos['room_type'] == 'entire_home') | (gdf_puntos['room_type'] == 'Entire home/apt')]
    gdf_puntos['longitude'] = pd.to_numeric(gdf_puntos.longitude, downcast='float')
    gdf_puntos['latitude'] = pd.to_numeric(gdf_puntos.latitude, downcast='float')
    gdf_puntos['Coordinates'] = list(zip(gdf_puntos['longitude'], gdf_puntos['latitude']))
    gdf_puntos['Coordinates'] = gdf_puntos['Coordinates'].apply(Point)
    gdf_puntos = gpd.GeoDataFrame(gdf_puntos, geometry='Coordinates')
    gdf_puntos = gdf_puntos.set_crs(epsg=4326)

    gdf_join = gpd.sjoin(gdf_puntos, gdf_barrios, how='left')

    # Agrupamos los resultados
    gdf_ag=gdf_join.groupby(
            ['coddistrit','coddistbar']
        ).count()

    for index, row in gdf_ag.iterrows():
        df_dest = df_dest.append({'DT': index[0],
                                  'DTBA': int(index[1]),
                                  'Indicator': 301,
                                  'Year': Yearfich,
                                  'Value': row[0]}, ignore_index=True)


def importa_fichero_pisosturisticos(fich, years, yearini):
    global df_dest
    df_pisos = pd.read_excel(fich, skiprows=range(4))

    for index, row in df_pisos.iterrows():
        if type(row['Districte']) == str:
            aux = row['Districte'].split('.')
            if aux[0].isdigit():
                DT = aux[0]
        if type(row['Barri']) == str:
            if row['Barri'].find('.') > 0:
                aux = row['Barri'].split('.')
                DTBA = aux[0] + aux[1]
                for col in range(years):
                    num = row[2 + col]
                    if num > 0:
                        num = int(num)
                    else:
                        num = 0
                    df_dest = df_dest.append({'DT': DT,
                                              'DTBA': DTBA,
                                              'Indicator': 302,
                                              'Year': yearini+col,
                                              'Value': int(num)}, ignore_index=True)


def importa_fichero_renta(directorio, fich):
    global df_dest
    df = pd.read_csv(directorio + fich, sep=';', encoding="ISO-8859-1")
    Indfich = 400 + int(fich[16:18])
    for index, row in df.iterrows() :
        if str(row['DT']) != 'nan':
            DT = int(row['DT'])
            DTBA = int(row['DTBA'])
            Year = int(row['Any'])
            df_dest = df_dest.append({'DT': DT,
                                      'DTBA': DTBA,
                                      'Indicator': Indfich,
                                      'Year': Year,
                                      'Value': row['Valor']}, ignore_index=True)


def crea_tabla_resumen(fichgeo, fichind):
    df_data = pd.read_csv(gb.pathData + gb.fileDataRaw, sep=';', decimal=',')
    df_data['ValueDate'] = df_data.apply(damefecha, axis=1)

    df_ind = pd.read_csv(fichind, sep=';')

    df_data = df_data.merge(df_ind, left_on='Indicator', right_on='Indicador')
    df_data['IndEsp'] = df_data.apply(dameEsp, axis=1)

    gdf_barrios = gpd.read_file(fichgeo)
    gdf_barrios.insert(0, "DTBA", pd.to_numeric(gdf_barrios.coddistbar, downcast='integer'), True)

    # Agrupamos los resultados
    df_datast=df_data.groupby(
            ['DT','DTBA','Year','ValueDate', df_data.IndEsp.values]
        ).Value.sum().unstack().reset_index()

    gdf_final = gdf_barrios.merge(df_datast, on='DTBA')

    gdf_final = gdf_final.drop(['gis_gis_barrios_area',
                                'objectid',
                                'linkid',
                                'codbarrio',
                                'coddistbar',
                                'last_edited_user',
                                'last_edited_date'], axis=1)

    gdf_final.to_csv(gb.pathData + gb.fileData, sep=';', decimal='.', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df_dest = pd.DataFrame(columns=['DT', 'DTBA', 'Indicator', 'Year', 'Value'])

    print('Cargando índices...')
    recorre_ficheros_indices()
    print('Índices finalizado')

    print('Cargando econs...')
    recorre_ficheros_econ()
    print('Econ finalizado')

    print('Cargando Airbnb...')
    recorre_ficheros_airbnb()
    print('Airbnb finalizado')

    print('Cargando Pisos Turísticos...')
    recorre_ficheros_pisos_turisticos()
    print('Pisos Turísticos finalizado')

    print('Cargando Renta...')
    recorre_ficheros_renta()
    print('Renta finalizado')

    df_dest.to_csv(gb.pathData + gb.fileDataRaw, sep=';', index=False)

    print('Creando tabla resumen')
    crea_tabla_resumen(gb.pathCSVsOther + gb.fileBarrios, gb.pathCSVsOther + gb.fileIndicadores)
    print('Proceso finalizado')

