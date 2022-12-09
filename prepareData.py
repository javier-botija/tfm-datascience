import geopandas as gpd
from load import globals as gb

barrios = gpd.read_file(gb.pathoCSVs + gb.fileBarrios)
print(barrios)