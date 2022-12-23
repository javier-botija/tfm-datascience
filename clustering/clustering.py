import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
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


def elimina_ceros(df_data):
    df_data_new = df_data
    for col in gb.indexes:
        df_data_new = df_data_new[df_data_new[col] != 0]
    return df_data_new

def genera_plot_hist(df_data):
    df_data.hist()
    plt.show()


def genera_boxplot(df_data_vars):
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df_data_vars)
    plt.boxplot(X, vert=True, patch_artist=False);
    plt.xticks([1,2,3,4,5,6,7],df_data_vars.columns,rotation=10, fontsize=6)
    plt.show()


def genera_plot_norma(df_data_vars):
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(25, 5))
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
    plt.show()


def genera_kmeans(df_data_or, clusters):
    df_data_vars=df_data_or[gb.indexes]
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df_data_vars)
    kmeans = KMeans(n_clusters=clusters, random_state=5).fit(X)
    labels = kmeans.predict(X)
    #print(labels)
    df_data_or['cluster'] = labels
    df_data_or['namecluster'] = df_data_or.apply(dame_label_cluster, axis=1)
    df_data_or.to_csv(gb.pathData + gb.fileDataC.replace('Cluster','Cluster' + '_' + str(clusters)) , sep=';', decimal='.', index=False)

def genera_hist_cluster(df_data):
    df_data.hist(hue='cluster', x=gb.indexes)
    plt.show()

def genera_plot_cluster(df_data):
    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(25, 5))
    nrow=0
    ncol=0
    for col in gb.indexes:
        x_data = df_data[[col,'cluster']]
        axs[nrow, ncol] = sns.histplot(data=x_data, x=col, hue='cluster', multiple='dodge', shrink=.9)
        #axs[nrow, ncol].plot(x_data, np.full_like(x_data, -0.01), '|k', markeredgewidth=1)
        #axs[nrow, ncol].set_title(col)
        axs[nrow, ncol].set_xlabel(col, fontsize=10)
        axs[nrow, ncol].set_ylabel('número')
        ncol = ncol + 1
        if ncol>3:
            ncol = 0
            nrow = nrow + 1
    plt.tight_layout()
    plt.show()

def genera_boxplot_clusters(df_data):
    clusters = df_data.cluster.unique()
    if len(clusters) == 3:
        labels = ['Riesgo Medio', 'Riesgo Bajo', 'Gentrificado']
        colors = ['turquoise', 'gold', 'coral']
    else:
        labels = ['Riesgo Medio Alto', 'Riesgo Medio Bajo', 'Riesgo Bajo', 'Gentrificado']
        colors = ['turquoise', 'pink', 'gold', 'coral']

    fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(25, 5))
    nrow=0
    ncol=0
    for col in gb.indexes:
        data_index = []
        for cluster in clusters:
            data_index.append(df_data[df_data['cluster'] == cluster][col])
        bplot = axs[nrow, ncol].boxplot(data_index, vert=True, patch_artist=True, labels=labels)
        axs[nrow, ncol].set_xlabel(col, fontsize=10)

        #axs[nrow, ncol].xticks(range(1, len(clusters) + 1), labels, rotation=10, fontsize=6)
        for patch, color in zip(bplot['boxes'], colors) :
            patch.set_facecolor(color)
        ncol = ncol + 1
        if ncol>3:
            ncol = 0
            nrow = nrow + 1
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plt.style.use('ggplot')
    warnings.filterwarnings('ignore')
    df_data = pd.read_csv(gb.pathData + gb.fileDataClean, sep=';', decimal='.')
    df_data = elimina_ceros(df_data)
    df_data_vars = df_data[gb.indexes]
    #genera_plot_hist(df_data_vars)
    #genera_boxplot(df_data_vars)
    #genera_plot_norma(df_data_vars)
    #tabla_correlaciones(df_data_vars)
    #genera_pairplot(df_data_vars)
    #genera_obtienek(df_data)
    #genera_kmeans(df_data, 3)
    #genera_kmeans(df_data, 4)

    #df_data = pd.read_csv(gb.pathData + gb.fileDataC.replace('Cluster','Cluster' + '_' + str(3)), sep=';', decimal='.')
    #genera_boxplot_clusters(df_data)
    df_data = pd.read_csv(gb.pathData + gb.fileDataC.replace('Cluster','Cluster' + '_' + str(4)), sep=';', decimal='.')
    genera_boxplot_clusters(df_data)

