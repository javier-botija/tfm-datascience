# tfm-datascience

|[UOC]
(https://camo.githubusercontent.com/cfd60245a1fb39e8e19f3ed8c60c16d5bbb3873a74a38259802d88270291c823/687474703a2f2f7777772e756f632e6564752f706f7274616c2f5f7265736f75726365732f636f6d6d6f6e2f696d61746765732f6d617263615f554f432f554f435f4d61737465726272616e642e6a7067)

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
