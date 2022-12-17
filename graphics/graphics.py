import pandas as pd
import matplotlib.pyplot as plt
import plotly

import globals as gb
import cufflinks as cf
from IPython.display import display,HTML


def dame_barrio(mrow):
    barrio = str(mrow.DTBA) + ' ' + mrow.nombre
    return barrio


def crea_df(Indice):
    df_data = pd.read_csv(gb.pathData + gb.fileData, sep=';', decimal=',')
    #df_data = df_data[df_data.DT.isin([11])]
    df_data['barrio'] = df_data.apply(dame_barrio, axis=1)
    df_data = df_data.pivot_table(index='Year', columns='barrio', values=Indice)
    #df_data = df_data.dropna()
    return df_data


def crea_plot(Indice):
    df_data = crea_df(Indice)
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


    #crea_plot('027 Distribución porcentual de población de nacionalidad extranjera Europea no UE')
    #crea_plot('041 Número medio de personas por unidad familiar')
    #crea_plot('040 Población de 18 o más años con nivel de estudios de Bachillerato o superior')
    #crea_plot('090 % Viviendas con valor catastral menor de 18.000 euros')
    #crea_plot('098 Actividades económicas por 1.000 habitantes')
    #crea_plot('201 Comercio Restaurantes Hostelería y Reparaciones')
    crea_plot('301 Número de Airbnb')
    crea_plot('302 Número de Pisos Turísticos')
    #crea_plot('401 Renta neta media por persona')
    #crea_plot('402 Renta neta media por hogar')
    #crea_plot('403 Media de la renta por unidad de consumo')
    #crea_plot('407 Porcentaje de ingresos - Salarios')
    #crea_plot('408 Porcentaje de ingresos - Pensiones')
    #crea_plot('409 Porcentaje de ingresos - Desocupación')
    #crea_plot('410 Porcentaje de ingresos - Incapacidad')
    #crea_plot('411 Porcentaje de ingresos - Arrendamientos')
    #crea_plot('474 Índice de Gini')
    #crea_plot('475 Distribución de la renta P80/P20')
