# tfm-datascience

|[UOC]
(https://github.com/javier-botija/tfm-datascience/tree/main/UOC-logo.png)

Este es el repositorio del código correspondiente al desarrollo del proyecto de final
de máster en Ciencia de Datos de la UOC con título "Estudio de los factores de gentrificación de los barrios en la ciudad de Valencia".

Para ejecutar el código una vez clonado, es necesario instalar los requerimientos utilizando
el comando `pip install -r requierements.txt`. En Windows puede dar algún problema
al instalar la librería `geopandas`, concretamente su dependencia Fiona con el error ` A GDAL API version must be specified. Provide a path to gdal-config using a GDAL_CONFIG environment variable or use a GDAL_VERSION environment variable.` No obstante, en Linux funciona perfectamente.

Una vez ejecutado el comando, ya se puede ejecutar el código con la instrucción `python __main__.py`.

- **--load**: Carga de los ficheros y transformaciones
- **--graphics**: Generación de los plotly de los índices seleccionados
- **--graphic11**: Generación del plotly de nacionalidades
- **--clustering**: Generación de gráficos y ejecuta el algoritmo de k-means
