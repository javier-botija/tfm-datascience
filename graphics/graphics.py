import pandas as pd
import plotly

import globals as gb
import cufflinks as cf


def crea_df(Indice, Var, DT):
    df_data = pd.read_csv(gb.pathData + gb.fileData, sep=';', decimal=',')
    if DT:
        df_data = df_data[df_data.DT.isin(DT)]

    df_data = df_data.pivot_table(index='Year', columns='barrio', values=Indice)

    if Var:
        for col in df_data.columns:
            barrio = ''
            for index, row in df_data.iterrows() :
                if barrio == '':
                    barrio = col
                    valorant = row[col]
                valor = row[col]
                row[col]= valor - valorant
                valorant = valor

    #df_data = df_data.dropna()
    return df_data


def crea_plot(Indice, Var = False, DT = []):
    df_data = crea_df(Indice, Var, DT)
    if Var:
        Indice = Indice + ' (Variación)'
    df_data.iplot(kind='line', xTitle='Year', yTitle=Indice)


if __name__ == '__main__':
    cf.set_config_file(sharing='public', theme='white', offline=True)
    setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)

    indices = gb.indexes
    #indices = ['503 Alquiler medio mensual €/m2']
    DT = [11, 1, 2]
    DT = []
    for indice in indices:
        crea_plot(indice, DT = DT)
