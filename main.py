import sys
import argparse
sys.path.append("code")
import globals as gb
import load
import graphics
import graphic11
import clustering


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Mostrar gráficos en depuración", action="store_true")
    parser.add_argument("-l", "--load", help="Carga los ficheros")
    parser.add_argument("-g", "--graphics", help="Genera los gráficos")
    parser.add_argument("-g11", "--graphic11", help="Genera el gráfico específico de 11")
    parser.add_argument("-c", "--clustering", help="Genera los gráficos y ficheros de clústeres")
    parser.add_argument("-a", "--all", help="Realiza todo el proceso")
    args = parser.parse_args()

    if args.verbose:
        gb.debug = True
    if args.load:
        load.load()
    if args.graphics:
        graphics.graphics()
    if args.graphic11:
        graphic11.graphic11()
    if args.clustering:
        clustering.clustering()
    if args.all or ((args.load == None) & (args.graphics == None) & (args.graphic11 == None) & (args.clustering == None)):
        gb.debug = False
        load.load()
        graphics.graphics()
        graphic11.graphic11()
        clustering.clustering()