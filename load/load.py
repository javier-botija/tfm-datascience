import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import globals as gb


def dame_fecha(mrow):
    mfechastr = "01/01/" + str(int(mrow.Year))
    mfecha = pd.to_datetime(mfechastr)
    return mfecha


def dame_esp(mrow):
    mesp = ("00" + str(mrow.Indicador))[-3:] + " " + str(mrow.Ind_Esp)
    return mesp


def dame_barrio(mrow):
    barrio = str(mrow.DTBA) + ' ' + mrow.nombre
    return barrio


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


def recorre_ficheros_alquileres():
    ficheros = os.listdir(gb.pathCSVsAlquileres)
    for fich in ficheros:
        if fich[0:6] == 'Barris':
            importa_fichero_alquileres(gb.pathCSVsAlquileres, fich)


def importa_fichero_indices(directorio, fich):
    print('   ' + fich)
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
    print('   ' + fich)
    global df_dest
    df = pd.read_csv(directorio + fich, sep=';', skiprows=2, encoding="ISO-8859-1", thousands='.')
    if df.columns[3] == 'Total':
        colini = 4
    else:
        colini = 3
    yearfich = fich.replace('.csv','').replace('T0003_C ','')
    for index, row in df.iterrows():
        if row['Barrio'].is_integer():
            dtba = str(int(row['Distrito'])) + str(int(row['Barrio']))
            if colini == 3 :
                value_tot = int(row[3]) + int(row[4]) + int(row[5]) + int(row[6])
            else :
                value_tot = int(row['Total'])
            df_dest = df_dest.append({'DT': row['Distrito'],
                                      'DTBA': dtba,
                                      'Indicator': 200,
                                      'Year': yearfich,
                                      'Value': value_tot}, ignore_index=True)
            for col in range(4):
                value = int(row[colini+col])
                df_dest = df_dest.append({'DT': row['Distrito'],
                                          'DTBA': dtba,
                                          'Indicator': 201+col,
                                          'Year': yearfich,
                                          'Value': value}, ignore_index=True)


def importa_fichero_airbnb(fich, year_fich):
    print('   ' + fich)
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
    gdf_ag = gdf_join.groupby(['coddistrit','coddistbar'])\
                                .agg({'id': 'count'})
    for index, row in gdf_ag.iterrows():
        dt = int(index[0])
        dtba = int(index[1])
        if str(row[0]) != 'nan':
            value = int(row[0])
            df_dest = df_dest.append({'DT': dt,
                                      'DTBA': dtba,
                                      'Indicator': 301,
                                      'Year': year_fich,
                                      'Value': value}, ignore_index=True)

    gdf_ag = gdf_join.apply(pd.to_numeric, errors='ignore') \
            .groupby(['coddistrit', 'coddistbar']) \
            .agg({'price' : 'mean'})
    for index, row in gdf_ag.iterrows() :
        dt = int(index[0])
        dtba = int(index[1])
        if str(row[0]) != 'nan' :
            value = str(round(row[0], 2)).replace('.',',')
            df_dest = df_dest.append({'DT': dt,
                                      'DTBA': dtba,
                                      'Indicator': 302,
                                      'Year': year_fich,
                                      'Value': value}, ignore_index=True)


def importa_fichero_pisosturisticos(fich, years, yearini):
    print('   ' + fich)
    global df_dest
    df_pisos = pd.read_excel(fich, skiprows=range(4))

    dt=''
    for index, row in df_pisos.iterrows():
        if type(row['Districte']) == str:
            aux = row['Districte'].split('.')
            if aux[0].isdigit():
                dt = aux[0]
        if type(row['Barri']) == str:
            if row['Barri'].find('.') > 0:
                aux = row['Barri'].split('.')
                dtba = aux[0] + aux[1]
                for col in range(years):
                    num = row[2 + col]
                    if num > 0:
                        num = int(num)
                    else:
                        num = int(0)
                    df_dest = df_dest.append({'DT': dt,
                                              'DTBA': dtba,
                                              'Indicator': 311,
                                              'Year': yearini+col,
                                              'Value': num}, ignore_index=True)


def importa_fichero_renta(directorio, fich):
    print('   ' + fich)
    global df_dest
    df = pd.read_csv(directorio + fich, sep=';', encoding="ISO-8859-1")
    ind_fich = 400 + int(fich[16:18])
    for index, row in df.iterrows() :
        if str(row['DT']) != 'nan':
            dt = int(row['DT'])
            dtba = int(row['DTBA'])
            year = int(row['Any'])
            df_dest = df_dest.append({'DT': dt,
                                      'DTBA': dtba,
                                      'Indicator': ind_fich,
                                      'Year': year,
                                      'Value': row['Valor']}, ignore_index=True)


def importa_fichero_alquileres(directorio, fich):
    print('   ' + fich)
    global df_dest
    df = pd.read_csv(directorio + fich, sep=';', encoding="ISO-8859-1")
    ind_fich = 500 + int(fich.replace('.csv','').replace('Barris','')[4:])
    for index, row in df.iterrows() :
        if str(row['Valor']) != 'nan':
            dt = int(row['Barri'].split('.')[0])
            dtba = int(row['Codi barri'])
            year = int(row['Any'])
            df_dest = df_dest.append({'DT': dt,
                                      'DTBA': dtba,
                                      'Indicator': ind_fich,
                                      'Year': year,
                                      'Value': row['Valor']}, ignore_index=True)


def crea_tabla_resumen(fichgeo, fichind):
    df_data = pd.read_csv(gb.pathData + gb.fileDataRaw, sep=';', decimal=',')
    df_data['ValueDate'] = df_data.apply(dame_fecha, axis=1)

    df_ind = pd.read_csv(fichind, sep=';')

    df_data = df_data.merge(df_ind, left_on='Indicator', right_on='Indicador')
    df_data['IndEsp'] = df_data.apply(dame_esp, axis=1)

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
                                'coddistrit',
                                'coddistbar',
                                'last_edited_user',
                                'last_edited_date'], axis=1)
    gdf_final['barrio'] = gdf_final.apply(dame_barrio, axis=1)
    gdf_final.to_csv(gb.pathData + gb.fileData, sep=';', decimal='.', index=False)


def elimina_otros_indices(origen, destino):
    df_data = pd.read_csv(origen, sep=';', decimal='.')

    basicos = ['DT', 'DTBA', 'nombre', 'barrio', 'geometry', 'Year', 'ValueDate']

    indices = ['037 Índice de aloctonía estatal',
               '041 Número medio de personas por unidad familiar',
               '098 Actividades económicas por 1.000 habitantes',
               '201 Comercio Restaurantes Hostelería y Reparaciones',
               '311 Número de Pisos Turísticos',
               '401 Renta neta media por persona',
               '474 Índice de Gini',
               '503 Alquiler medio mensual €/m2'
               ]

    for col in df_data.columns:
            if (col not in basicos) & (col not in indices):
                    df_data = df_data.drop(col, axis=1)

    df_data.to_csv(destino, sep=';', decimal='.', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #df_dest = pd.DataFrame(columns=['DT', 'DTBA', 'Indicator', 'Year', 'Value'])

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

    print('Cargando Alquileres...')
    recorre_ficheros_alquileres()
    print('Alquileres finalizado')

    df_dest.to_csv(gb.pathData + gb.fileDataRaw, sep=';', index=False)

    print('Creando tabla resumen...')
    crea_tabla_resumen(gb.pathCSVsOther + gb.fileBarrios, gb.pathCSVsOther + gb.fileIndicadores)
    print('Proceso finalizado')

    print('Creando tabla solo indices...')
    elimina_otros_indices(gb.pathData + gb.fileData, gb.pathData + gb.fileDataT)
    print('Tabla reducida')

