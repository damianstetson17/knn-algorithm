import gui
import numpy
from typing import Counter
import matplotlib.pyplot as plt

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

def executeValidation(knnAlgorithm):
    KFoldResults = []
    PuntosConEtiquetasDevecinos = []
    #cargamos la tabla en horizontal de cada punto con sus 9 vecinos
    for data in knnAlgorithm.dataSet:
        PuntosConEtiquetasDevecinos.append(knnAlgorithm.findKFoldNeighbors(data)) 
    
    #contador de acuertos para los k-fold
    correctCount = 0
    #Desde k=1 hasta n-1
    for k in range(1,len(PuntosConEtiquetasDevecinos)):
        #recorremos una columna y guardamos primero el punto cabecera,
        #y luego una lista de solo las etiquetas de sus vecinos
        for PuntoConVecinos in PuntosConEtiquetasDevecinos:
            Punto = PuntoConVecinos["point"]
            EtiquetasDeVecinos = PuntoConVecinos["neighbors_label_list"][:k]
            # for i in range(1,k+1):
            #     EtiquetasDeVecinos.append(PuntoConVecinos[i])
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
        KFoldResults.append({"k":k, "accuracy":correctCount})
        correctCount = 0
    
    xList = []
    yList = []
    for KFold in KFoldResults:
        xList.append(KFold["k"])
        yList.append(KFold["accuracy"])
    
    plt.plot(xList,yList,'r--')
    plt.title("K Fold Validation")
    plt.xlabel('K Number')
    plt.ylabel('K accuracy')

    KFoldResults = sorted(KFoldResults, reverse=True, key=lambda d : d["accuracy"])
    maximo = KFoldResults[0]
    toShow = []
    for KFold in KFoldResults:
        if KFold["accuracy"] == maximo["accuracy"]:
            toShow.append([KFold["k"],KFold["accuracy"]])

    plt.annotate(f'Most Acurrate ({maximo["k"]};{maximo["accuracy"]})',
                xy=(maximo["k"], maximo["accuracy"]),
                xytext=(maximo["k"], maximo["accuracy"]/2),
                arrowprops=dict(facecolor='black', arrowstyle="->"))

    #Cargamos la tabla con los resultados de Kfold
    gui.kfold_results_table.delete(*gui.kfold_results_table.get_children())
    for bettersKinfo in toShow:
        gui.kfold_results_table.insert("", 'end', values=bettersKinfo)
    gui.kfold_results_table.pack(pady=10)

    plt.ion()
    plt.show()