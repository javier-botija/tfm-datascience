import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import globals as gb


barrios = gpd.read_file(gb.pathoCSVs + gb.fileBarrios)
print(barrios)