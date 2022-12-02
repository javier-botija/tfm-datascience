import os
import pandas as pd
import geopandas as gpd
import globals as gb
import numpy as np


def damefecha(mrow):
    mfechastr = "01/01/" + str(mrow.Year)
    mfecha = pd.to_datetime(mfechastr)
    return mfecha


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
    df_data = pd.read_csv(gb.pathData + 'dataraw.csv', sep=';', decimal=',')
    df_data['ValueDate'] = df_data.apply(damefecha, axis=1)

    df_ind = pd.read_csv(fichind, sep=';')

    df_data = df_data.merge(df_ind, left_on='Indicator', right_on='Indicador')

    gdf_barrios = gpd.read_file(fichgeo)
    gdf_barrios.insert(0, "DTBA", pd.to_numeric(gdf_barrios.coddistbar, downcast='integer'), True)

    # Filtro de Subtema
    for Tema in df_data['Tema'].unique():
        df_datast = df_data[df_data['Tema'] == Tema]
        # Agrupamos los resultados
        df_datast=df_datast.groupby(
            ['DT','DTBA','ValueDate', df_datast.Ind_Esp.values]
        ).Value.sum().unstack().reset_index()

        gdf_final = gdf_barrios.merge(df_datast, on='DTBA')

        gdf_final = gdf_final.drop(['gis_gis_barrios_area','objectid','linkid','codbarrio','coddistbar','last_edited_user','last_edited_date'], axis=1)
        gdf_final.to_csv(gb.pathData + 'data_' + Tema + '.csv', sep=';', decimal='.', index=False)
        #gdf_final.to_file(gb.pathData + 'data_' + Tema + '.geojson', driver='GeoJSON')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df_dest = pd.DataFrame(columns=['DT', 'DTBA', 'Indicator', 'Description', 'Year', 'Value'])
    #recorre_ficheros(gb.pathCSVs)
    crea_tabla_resumen(gb.pathoCSVs + gb.fileBarrios, gb.pathoCSVs + gb.fileIndicadores)
