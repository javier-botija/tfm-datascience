import pandas as pd
import plotly

import globals as gb
import cufflinks as cf


def dame_esp(mrow):
    mesp = ("00" + str(mrow.Indicador))[-3:] + " " + str(mrow.Ind_Esp)
    return mesp


def crea_df():
    df_data = pd.read_csv(gb.pathData + gb.fileDataRaw, sep=';', decimal=',')
    df_ind = pd.read_csv(gb.pathCSVsOther + gb.fileIndicadores, sep=';')
    df_data = df_data.merge(df_ind, left_on='Indicator', right_on='Indicador')
    df_data['IndEsp'] = df_data.apply(dame_esp, axis=1)

    # nos quedamos sólo con los indicadores del gráfico y del barrio del Cabanyal
    df_data = df_data[(df_data.Indicator>=26) & (df_data.Indicator<=32) & (df_data.DTBA == 112)]
    df_data = df_data.pivot_table(index='Year', columns='IndEsp', values='Value')
#    df_datast=df_data.groupby(
#            ['DT','DTBA','Year','ValueDate', df_data.IndEsp.values]
#        ).Value.sum().unstack().reset_index()
    return df_data


def crea_plot():
    df_data = crea_df()
    df_data.iplot(kind='line', xTitle='Year', yTitle='value')


if __name__ == '__main__':
    cf.set_config_file(sharing='public', theme='white', offline=True)
    setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)

    crea_plot()