# pip install numpy
# pip install matplotlib
import gui
from knn import Knn
from data import Data
from csv import reader
from typing import Counter, List

def startKAlgorithm():
    #parse to int from GUI input
    KNumber = int(gui.KNumber)

    #read from .txt the dataset
    with open(gui.pathDataSetFile, 'r') as read_dataSet:
        DataSet : List[Data] = []
        csv_reader = reader(read_dataSet)

        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            dataListRow = row[0].split()
            DataSet.append(
                Data(
                    float(dataListRow[0]),
                    float(dataListRow[1]),
                    int(dataListRow[2])
                )
            )
    """
    K FOLD VALIDATION EJEMPLO SENCILLO
    a = (8,8,8,8,7,7,7,7)
    aCounter = Counter(a)
    EtiquetaMasRepetida = max(aCounter,key=aCounter.get)
    ocurrenciasDeMaxValRep = 0
    Kacierto=0
    CantidadDeVecesDeLaEtiquetaMasRepetida = aCounter[EtiquetaMasRepetida]
    for etiqueta in aCounter:
        #si la cantidad de la etiqueta, es igual a la cantidad de la EtiquetaMasRepetida
        if aCounter[etiqueta] == CantidadDeVecesDeLaEtiquetaMasRepetida:
            ocurrenciasDeMaxValRep=ocurrenciasDeMaxValRep+1
    #si la cantidad de la EtiquetaMasRepetida no se repite para otras etiquetas (no hay empate)
    if ocurrenciasDeMaxValRep == 1:
            Kacierto = Kacierto+1
    print(f"el mas reptido de {a} es: {EtiquetaMasRepetida}, y por lo tanto se considera que hay: {Kacierto} acierto")
    """

    #Instace of a KNN object 
    knnAlgorithm = Knn(DataSet,KNumber)  

    """START K FOLD VALIDATION"""
    KFoldResults = []
    PuntosConEtiquetasDevecinos = []
    #cargamos la tabla en horizontal de cada punto con sus 9 vecinos
    for data in DataSet:
        PuntosConEtiquetasDevecinos.append(knnAlgorithm.findKFoldNeighbors(data)) 
    
    #contador de acuertos para los k-fold
    correctCount = 0
    #Desde k=1 hasta 10
    for k in range(1,11):
        #recorremos una columna y guardamos primero el punto cabecera,
        #y luego una lista de solo las etiquetas de sus vecinos
        for PuntoConVecinos in PuntosConEtiquetasDevecinos:
            Punto = PuntoConVecinos[0]
            EtiquetasDeVecinos = []
            for i in range(1,k+1):
                EtiquetasDeVecinos.append(PuntoConVecinos[i])
            #Contamos las cantidades de cada etiqueta
            cantidadesEtiquetas = Counter(EtiquetasDeVecinos)
            EtiquetaMasRepetida = max(cantidadesEtiquetas,key=cantidadesEtiquetas.get)
            ocurrenciasDeMaxValRep = 0
            CantidadDeVecesDeLaEtiquetaMasRepetida = cantidadesEtiquetas[EtiquetaMasRepetida]
            for etiqueta in cantidadesEtiquetas:
                if cantidadesEtiquetas[etiqueta] == CantidadDeVecesDeLaEtiquetaMasRepetida:
                    ocurrenciasDeMaxValRep=ocurrenciasDeMaxValRep+1
            if ocurrenciasDeMaxValRep == 1:
                if EtiquetaMasRepetida == Punto.label:
                    correctCount = correctCount+1
            ocurrenciasDeMaxValRep = 0
        KFoldResults.append((k,correctCount))
        correctCount = 0
    
    #Cargamos la tabla con los resultados de Kfold
    gui.kfold_results_table.delete(*gui.kfold_results_table.get_children())
    for Kinfo in KFoldResults:
        gui.kfold_results_table.insert("", 'end', values=Kinfo)
    gui.kfold_results_table.pack(pady=10)
    """END K FOLD VALIDATION"""

    #Execute KNN and generate the grid
    knnAlgorithm.GenerateGrid()

def main ():
    gui.generate_main_menu()     

if __name__ == '__main__':
    main()