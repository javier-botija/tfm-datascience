import os
import pandas as pd
import geopandas as gpd
import globals as gb
import numpy as np


def recorre_ficheros(directorio):
    global df_dest
    ficheros = os.listdir(directorio)
    for fich in ficheros:
        importa_fichero(directorio, fich)
    df_dest.to_csv(gb.pathData + 'dataraw.csv', sep=';', index=False)

def importa_fichero(directorio, fich):
    global df_dest
    df = pd.read_csv(directorio + fich, sep=';')
    for index, row in df.iterrows() :
        for column in [col for col in df.columns if col.find("Valor ") >= 0]:
            df_dest = df_dest.append({'DT': row['DT'],
                                      'DTBA': row['DTBA'],
                                      'Indicator': row['Indicador'],
                                      'Description': fich.replace('.csv',''),
                                      'Year': column.replace('Valor ', ''),
                                      'Value': row[column]}, ignore_index=True)


def crea_tabla_resumen(fichgeo, fichind):
    #global df_dest
    df_dest = pd.read_csv(gb.pathData + 'dataraw.csv', sep=';', decimal=',')
    # Filtro de años
    #df_dest = df_dest[df_dest['Year']==2021]
    df_ind = pd.read_csv(fichind, sep=';')

    df_dest = df_dest.merge(df_ind, left_on='Indicator', right_on='Indicador')
    # Filtro de Subtema
    df_dest = df_dest[df_dest['SubTema'] == 'Vivienda']
    # Agrupamos los resultados
    df_dest=df_dest.groupby(
        ['DT','DTBA','Year', df_dest.Ind_Esp.values]
    ).Value.sum().unstack().reset_index()

    gdf_barrios = gpd.read_file(fichgeo)
    gdf_barrios.insert(0, "DTBA", pd.to_numeric(gdf_barrios.coddistbar, downcast='integer'), True)
    gdf_final = gdf_barrios.merge(df_dest, on='DTBA')
    gdf_final = gdf_final.drop(['gis_gis_barrios_area','objectid','linkid','codbarrio','coddistbar','last_edited_user','last_edited_date'], axis=1)
    gdf_final.to_csv(gb.pathData + 'data.csv', sep=';', decimal='.', index=False)
    gdf_final.to_file(gb.pathData + 'data.geojson', driver='GeoJSON')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df_dest = pd.DataFrame(columns=['DT', 'DTBA', 'Indicator', 'Description', 'Year', 'Value'])
    #recorre_ficheros(gb.pathCSVs)
    crea_tabla_resumen(gb.pathoCSVs + gb.fileBarrios, gb.pathoCSVs + gb.fileIndicadores)
