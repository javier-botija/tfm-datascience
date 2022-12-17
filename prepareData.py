import geopandas as gpd
import globals as gb

barrios = gpd.read_file(gb.pathoCSVs + gb.fileBarrios)
print(barrios)