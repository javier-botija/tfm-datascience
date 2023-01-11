import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
import warnings
import globals as gb
import os


def dame_codigos(lista):
    nlista = []
    for val in range(len(lista)):
        nlista.append(lista[val][0:3])
    return nlista

def dame_cluster_ord(mrow):
    global g_cluster
    if g_cluster == 1:
        if mrow['cluster'] == 0:
            cl = 0
        elif mrow['cluster'] == 1:
            cl = 2
        elif mrow['cluster'] == 2:
            cl = 1
        else:
            cl = 3
    elif g_cluster == 2:
        if mrow['cluster'] == 0:
            cl = 1
        elif mrow['cluster'] == 1:
            cl = 2
        elif mrow['cluster'] == 2:
            cl = 0
        else:
            cl = 3
    elif g_cluster == 3:
        if mrow['cluster'] == 0:
            cl = 0
        elif mrow['cluster'] == 1:
            cl = 2
        elif mrow['cluster'] == 2:
            cl = 3
        else:
            cl = 1
    elif g_cluster == 4:
        if mrow['cluster'] == 0:
            cl = 1
        elif mrow['cluster'] == 1 :
            cl = 0
        elif mrow['cluster'] == 2:
            cl = 2
        else:
            cl = 3
    elif g_cluster == 5:
        if mrow['cluster'] == 0:
            cl = 0
        elif mrow['cluster'] == 1:
            cl = 1
        elif mrow['cluster'] == 2:
            cl = 2
        else:
            cl = 3
    elif g_cluster == 6:
        if mrow['cluster'] == 0:
            cl = 2
        elif mrow['cluster'] == 1:
            cl = 0
        elif mrow['cluster'] == 2:
            cl = 1
        else:
            cl = 3
    elif g_cluster == 7:
        if mrow['cluster'] == 0:
            cl = 2
        elif mrow['cluster'] == 1:
            cl = 1
        elif mrow['cluster'] == 2:
            cl = 0
        else:
            cl = 3
    return cl

def dame_label_cluster(mrow):
    return 'Cluster ' + str(mrow['cluster'])


def elimina_ceros(df_data):
    df_data_new = df_data
    for col in gb.indexes:
        df_data_new = df_data_new[df_data_new[col] != 0]
    return df_data_new

def genera_plot_hist(df_data):
    df_data.hist(figsize=(20,10))
    if gb.debug:
        plt.show()
    else:
        plt.savefig(gb.pathGraphics + gb.fileGhist)


def genera_boxplot(df_data_vars):
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df_data_vars)
    plt.figure(figsize=(10,8))
    plt.boxplot(X, vert=True, patch_artist=False);
    plt.xticks([1,2,3,4,5,6,7],df_data_vars.columns,rotation=10, fontsize=6)
    if gb.debug:
        plt.show()
    else:
        plt.savefig(gb.pathGraphics + gb.fileGboxplot)


def genera_plot_norma(df_data_vars):
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(25, 8))
    nrow=0
    ncol=0
    for col in df_data_vars.columns:
        x_data = df_data_vars[col]
        axs[nrow, ncol].hist(x=x_data, bins=30, color="#3182bd", alpha=0.5)
        axs[nrow, ncol].plot(x_data, np.full_like(x_data, -0.01), '|k', markeredgewidth=1)
        #axs[nrow, ncol].set_title(col)
        axs[nrow, ncol].set_xlabel(col, fontsize=10)
        axs[nrow, ncol].set_ylabel('número')
        ncol = ncol + 1
        if ncol>3:
            ncol = 0
            nrow = nrow + 1
    plt.tight_layout()
    if gb.debug:
        plt.show()
    else:
        plt.savefig(gb.pathGraphics + gb.fileGplotNorma)


def tabla_correlaciones(df_data_vars):
    corr_matrix = df_data_vars.corr(method='pearson')
    #print(corr_matrix)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 10))
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
    if gb.debug:
        plt.show()
    else:
        plt.savefig(gb.pathGraphics + gb.fileGheatmap)

def genera_pairplot(df_data_vars):
    labels = dame_codigos(gb.indexes)
    g = sns.pairplot(df_data_vars.dropna(), size=2.5,
                 vars=gb.indexes,
                 kind='scatter')

    for ax, lbl in zip(g.axes.flatten(), labels) :
        ax.set_xlabel(lbl, rotation = 45)
        ax.set_ylabel(lbl, rotation = 90)


    if gb.debug:
        plt.show()
    else:
        plt.savefig(gb.pathGraphics + gb.fileGpaitplot)


def genera_obtienek(df_data_or):
    Nc = range(2, 10)
    X = np.array(df_data_or[gb.indexes].dropna())
    kmeans = [KMeans(n_clusters=i, random_state=5) for i in Nc]
    #print(kmeans)
    score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
    #print(score)
    silhouette = []
    for i in range(len(kmeans)):
        cluster_labels = kmeans[i].fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        silhouette.append(silhouette_avg)

    #silhouette = [silhouette_score(X, kmeans[i].fit_predict(X)) for i in range(len(kmeans))]
    # print(silhouette)
    plt.figure(figsize=(10,5))
    plt.subplot(1, 2, 1)
    plt.plot(Nc, score)
    plt.xlabel('Número de clústeres')
    plt.ylabel('valor')
    plt.title('Método del codo')

    plt.subplot(1, 2, 2)
    plt.plot(Nc, silhouette)
    plt.xlabel('Número de clústeres')
    plt.ylabel('valor')
    plt.title('Análisis de silueta')
    if gb.debug:
        plt.show()
    else:
        plt.savefig(gb.pathGraphics + gb.fileGk)

def dame_text(modelo, clusters, exc):
    txt = modelo
    if exc != '':
        txt = txt + '_sin_' + exc
    txt = txt + '_' + str(clusters)
    return txt

def genera_fichero_Clusters(df_data, modelo, clusters, exc=''):
    # si no existe tomamos el que se nos pasa como base
    if not os.path.exists(gb.pathData + gb.fileDataC):
        df_cluster = df_data.copy()
    else:
        df_cluster = pd.read_csv(gb.pathData + gb.fileDataC, sep=';', decimal='.')
    # eliminamos las columnas base
    if 'cluster' in df_cluster.columns:
        df_cluster.drop(columns=['cluster'])
    if 'namecluster' in df_cluster.columns:
        df_cluster.drop(columns=['namecluster'])

    name_col = dame_text(modelo, clusters, exc)
    # las columnas nuevas a generar por si existieran
    if 'c_' + name_col in df_cluster.columns:
        df_cluster.drop(columns=['c_' + name_col])
    if 'n_' + name_col in df_cluster.columns:
        df_cluster.drop(columns=['n_' + name_col])
    df_cluster['c_' + name_col] = df_data['cluster'].to_numpy().tolist()
    df_cluster['n_' + name_col] = df_data['namecluster'].to_numpy().tolist()
    df_cluster.to_csv(gb.pathData + gb.fileDataC, sep=';', decimal='.', index=False)


def genera_kmeans(df_data_or, clusters, exc = ''):
    global g_cluster
    indexes = gb.indexes
    if exc != '':
        indexes = list(filter(lambda x : exc not in x, indexes))
    df_data_vars=df_data_or[indexes]

    scaler = MinMaxScaler()
    X = scaler.fit_transform(df_data_vars)
    kmeans = KMeans(n_clusters=clusters, random_state=5).fit(X)
    labels = kmeans.predict(X)
    #print(labels)
    df_data_or['cluster'] = labels
    if clusters == 3:
        if (exc == '') or (exc == '201') or (exc =='474'):
            g_cluster = 1
        elif (exc == '042') or (exc == '503'):
            g_cluster = 5
        else:
            g_cluster = 4
    else:
        if exc == '':
            g_cluster = 6
        else:
            g_cluster = 2

    df_data_or['cluster'] = df_data_or.apply(dame_cluster_ord, axis=1)
    df_data_or['namecluster'] = df_data_or.apply(dame_label_cluster, axis=1)

    genera_fichero_Clusters(df_data_or, 'KM', clusters, exc)

def genera_SpectralClustering(df_data_or, clusters):
    global g_cluster
    df_data_vars = df_data_or[gb.indexes]
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df_data_vars)
    sc = SpectralClustering(n_clusters=clusters, random_state=5).fit(X)
    labels = sc.labels_
    #print(labels)
    df_data_or['cluster'] = labels
    if clusters == 3:
        g_cluster = 2
    else:
        g_cluster = 3
    df_data_or['cluster'] = df_data_or.apply(dame_cluster_ord, axis=1)
    df_data_or['namecluster'] = df_data_or.apply(dame_label_cluster, axis=1)

    genera_fichero_Clusters(df_data_or, 'SC', clusters)

def genera_boxplot_clusters(modelo, clusters, exc=''):
    df_data = pd.read_csv(gb.pathData + gb.fileDataC, sep=';', decimal='.')
    # equivalencia de los clusteres con los nombres y colores
    if (clusters == 3):
        labels = ['Riesgo Bajo', 'Riesgo Medio', 'Gentrificado']
        colors = ['green', 'goldenrod', 'tomato']
    else:
        labels = ['Riesgo Bajo', 'Riesgo Medio Bajo', 'Riesgo Medio Alto', 'Gentrificado']
        colors = ['green', 'yellowgreen', 'goldenrod', 'tomato']
    name_col = dame_text(modelo, clusters, exc)
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(25, 10))
    nrow=0
    ncol=0
    for col in gb.indexes:
        data_index = []
        for cluster in range(clusters):
            data_index.append(df_data[df_data['c_' + name_col] == cluster][col])
        bplot = axs[nrow, ncol].boxplot(data_index, vert=True, patch_artist=True, labels=labels)
        axs[nrow, ncol].set_xlabel(col, fontsize=10)
        for patch, color in zip(bplot['boxes'], colors) :
            patch.set_facecolor(color)
        ncol = ncol + 1
        if ncol>3:
            ncol = 0
            nrow = nrow + 1
    plt.tight_layout()
    if gb.debug:
        plt.show()
    else:
        plt.savefig(gb.pathGraphics + gb.fileGboxplotcluster.replace('cluster','cluster_' + name_col))



def clustering():
    plt.style.use('ggplot')
    warnings.filterwarnings('ignore')
    df_data = pd.read_csv(gb.pathData + gb.fileDataClean, sep=';', decimal='.')
    df_data = elimina_ceros(df_data)
    df_data_vars = df_data[gb.indexes]
    gb.debug = False
    genera_plot_hist(df_data_vars)
    genera_boxplot(df_data_vars)
    genera_plot_norma(df_data_vars)
    tabla_correlaciones(df_data_vars)
    genera_pairplot(df_data_vars)
    genera_obtienek(df_data)
    genera_kmeans(df_data, 3)
    genera_boxplot_clusters('KM', 3)
    genera_kmeans(df_data, 4)
    genera_boxplot_clusters('KM', 4)
    genera_SpectralClustering(df_data, 3)
    genera_boxplot_clusters('SC', 3)
    genera_SpectralClustering(df_data, 4)
    genera_boxplot_clusters('SC', 4)

    for ind in gb.indexes:
        genera_kmeans(df_data, 3, ind[0:3])
        genera_boxplot_clusters('KM', 3, ind[0:3])

if __name__ == '__main__':
    clustering()