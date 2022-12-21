import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import warnings
import globals as gb


def dame_codigos(lista):
    nlista = []
    for val in range(len(lista)):
        nlista.append(lista[val][0:3])
    return nlista

def dame_label_cluster(mrow):
    return 'Cluster ' + str(mrow['cluster'])


def genera_plot_hist(df_data):
    df_data.hist()
    plt.show()


def genera_plot_norma(df_data_vars):
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(25, 5))
    nrow=0
    ncol=0
    for col in df_data_vars.columns:
        x_data = df_data_vars[col]
        axs[nrow, ncol].hist(x=x_data, bins=20, color="#3182bd", alpha=0.5)
        axs[nrow, ncol].plot(x_data, np.full_like(x_data, -0.01), '|k', markeredgewidth=1)
        axs[nrow, ncol].set_title(col)
        axs[nrow, ncol].set_xlabel('variable')
        axs[nrow, ncol].set_ylabel('número')
        ncol = ncol + 1
        if ncol>3:
            ncol = 0
            nrow = nrow + 1
    plt.tight_layout()
    plt.show()


def tabla_correlaciones(df_data_vars):
    corr_matrix = df_data_vars.corr(method='pearson')
    #print(corr_matrix)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
    sns.heatmap(
        corr_matrix,
        annot     = True,
        cbar      = False,
        annot_kws = {"size": 8},
        vmin      = -1,
        vmax      = 1,
        center    = 0,
        cmap      = sns.diverging_palette(20, 220, n=200),
        square    = True,
        ax        = ax
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation = 45,
        horizontalalignment = 'right',
    )
    ax.tick_params(labelsize = 10)
    plt.show()

def genera_pairplot(df_data_vars):
    labels = dame_codigos(gb.indexes)
    g = sns.pairplot(df_data_vars.dropna(), size=1.5,
                 vars=gb.indexes,
                 kind='scatter')

    for ax, lbl in zip(g.axes.flatten(), labels) :
        ax.set_xlabel(lbl, rotation = 45)
        ax.set_ylabel(lbl, rotation = 90)


    plt.show()


def genera_obtienek(df_data_or):
    Nc = range(1, 10)
    X = np.array(df_data_or[gb.indexes].dropna())
    kmeans = [KMeans(n_clusters=i) for i in Nc]
    #print(kmeans)
    score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
    #print(score)
    plt.plot(Nc, score)
    plt.xlabel('Número de  Clusters')
    plt.ylabel('valor')
    plt.title('Método del codo')
    plt.show()


def genera_kmeans(df_data_or, clusters):
    df_data_vars=df_data_or[gb.indexes]
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df_data_vars)
    kmeans = KMeans(n_clusters=clusters).fit(X)
    labels = kmeans.predict(X)
    #print(labels)
    df_data_or['cluster'] = labels
    df_data_or['namecluster'] = df_data_or.apply(dame_label_cluster, axis=1)
    df_data_or.to_csv(gb.pathData + gb.fileDataC.replace('Cluster','Cluster' + '_' + str(clusters)) , sep=';', decimal='.', index=False)



if __name__ == '__main__':
    plt.style.use('ggplot')
    warnings.filterwarnings('ignore')
    df_data = pd.read_csv(gb.pathData + gb.fileDataClean, sep=';', decimal='.')
    df_data_vars = df_data[gb.indexes]
    #genera_plot_hist(df_data_vars)
    #genera_plot_norma(df_data_vars)
    #tabla_correlaciones(df_data_vars)
    genera_pairplot(df_data_vars)
    #genera_obtienek(df_data)
    #genera_kmeans(df_data, 3)
    #genera_kmeans(df_data, 4)

