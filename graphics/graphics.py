import pandas as pd
import matplotlib.pyplot as plt
import plotly

import globals as gb
import cufflinks as cf
from IPython.display import display,HTML





def crea_df(Indice, Var):
    df_data = pd.read_csv(gb.pathData + gb.fileData, sep=';', decimal=',')
    #df_data = df_data[df_data.DT.isin([11])]

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


def crea_plot(Indice, Var = False):
    df_data = crea_df(Indice, Var)
    if Var:
        Indice = Indice + ' (Variación)'
    df_data.iplot(kind='line', xTitle='Year', yTitle=Indice)



def dibuja_graficos(Indice):
    df_data = pd.read_csv(gb.pathData + gb.fileData, sep=';', decimal=',')

    # Cree un nuevo subgrafo,
    # la cuadrícula es 1x2,
    # el número de serie es 1,
    # el primer número es el número de filas,
    # el segundo número es el número de columnas,
    # lo que indica la disposición de los subgrafos, y el tercer número es el número de serie del subgrafo
    fig, axs = plt.subplots(2, 2)
    fig.suptitle(Indice)



    row = 0
    for dt in df_data[(df_data[Indice].notnull())].DT.unique():
        row = row + 1
        col = 0
        if row<3:
            print('dt' + str(dt))
            for dtba in df_data[(df_data.DT == dt) & (df_data[Indice].notnull())].DTBA.unique():
                col = col + 1
                if col < 3:
                    print('dtba' + str(dtba))
                    df_filter = df_data[(df_data.DT == dt) & (df_data.DTBA == dtba) & (df_data[Indice].notnull())]
                    x = df_filter.Year
                    y = df_filter[Indice].to_list()
                    print(row, col, dt, dtba, y)
                    axs[row-1, col-1].plot(x, y)
                    #print(row-1,col-1, dt, dtba)
                    #axs[0, 0].set_title(df_filter.nombre[0])



#    for ax in axs.flat :
#        ax.set(xlabel='Años', ylabel='Valores')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
#    for ax in axs.flat :
#        ax.label_outer()


    # Mostrar
    #fig.show()
    plt.show()

if __name__ == '__main__':
    cf.set_config_file(sharing='public', theme='white', offline=True)
    setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)
    indices = ['027 Distribución porcentual de población de nacionalidad extranjera Europea no UE',
               '041 Número medio de personas por unidad familiar',
               '098 Actividades económicas por 1.000 habitantes',
               '201 Comercio Restaurantes Hostelería y Reparaciones',
               '311 Número de Pisos Turísticos',
               '401 Renta neta media por persona',
               '474 Índice de Gini',
               '503 Alquiler medio mensual €/m2'
               ]
    indices = ['026 Distribución porcentual de población de nacionalidad extranjera de la Unión Europea',
               '027 Distribución porcentual de población de nacionalidad extranjera Europea no UE',
               '028 Distribución porcentual de población de nacionalidad extranjera de África',
               '029 Distribución porcentual de población de nacionalidad extranjera de América del Norte',
               '030 Distribución porcentual de población de nacionalidad extranjera de América Central',
               '031 Distribución porcentual de población de nacionalidad extranjera de América del Sur',
               '032 Distribución porcentual de población de nacionalidad extranjera de Asia Oceanía o apátrida',
               '033 Índice de autoctonía',
               '034 Índice de autoctonía provincial',
               '035 Índice de autoctonía Comunidad Valenciana',
               '036 Índice de autoctonía estatal',
               '037 Índice de aloctonía estatal',
               '038 Índice de autoctonía UE'
               ]

    for indice in indices:
        crea_plot(indice)
