import os
import pandas as pd


def recorre_ficheros(directorio):
    global df_dest
    ficheros = os.listdir(directorio)
    for fich in ficheros:
        importa_fichero(directorio, fich)


def importa_fichero(directorio, fich) :
    global df_dest
    df = pd.read_csv(directorio + fich, sep=';')
    for index, row in df.iterrows() :
        for column in [col for col in df.columns if col.find("Valor ") >= 0] :
            df_dest = df_dest.append({'DT': row['DT'],
                                      'DTBA': row['DTBA'],
                                      'Indicator': row['Indicador'],
                                      'Description': fich.replace('.csv',''),
                                      'Year': column.replace('Valor ', ''),
                                      'Value': row[column]}, ignore_index=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__' :
    df_dest = pd.DataFrame(columns=['DT', 'DTBA', 'Indicator', 'Description', 'Year', 'Value'])
    recorre_ficheros('../CSVs/')
    df_dest.to_csv('../data.csv', sep=';')

