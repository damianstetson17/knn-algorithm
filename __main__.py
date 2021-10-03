# pip install numpy
# pip install matplotlib

from knn import Knn
from data import Data
from tkinter import *
from csv import reader
import tkinter.messagebox
from typing import Counter, List

pathDataSetFile = "Not selected."
KNumber = 1
KFoldResults = []

def GUI ():
    global KNumber
    global pathDataSetFile
    root = Tk()
    root.title("Main Menú - KNN - Stetson & Piotroski")
    #initial values for start the algorithm
    frame_values_selected = LabelFrame(root, text="SELECTED VALUES", padx=65,pady=71.5)
    frame_values_selected.grid(row=1, column=1)
    label_data_set_path = Label(frame_values_selected, text="DATA SET path file: "+pathDataSetFile)
    label_data_set_path.pack()
    #number k label
    label_clusters = Label(frame_values_selected, text="Number of k selected: "+str(KNumber))
    label_clusters.pack(pady=10)
    #start the K algorithm button
    button_start_K = Button(frame_values_selected,text="START K ALGORITHM", command=startButton)
    button_start_K.pack()

    #inputs frame
    frame_inputs = LabelFrame(root, text="INITIAL VALUES", padx=50,pady=50)
    frame_inputs.grid(row=1, column=0)
    button_select_data_set = Button(frame_inputs, text = "Select DATA SET .txt file", width=25,
                                        command = lambda: setPathFile(label_data_set_path))
    button_select_data_set.pack()

    #k scale
    k_scale_input = Scale(frame_inputs, label="Select the number of K:", 
                            from_=1, to=10, orient=HORIZONTAL, length=200,
                            command = lambda a: setKNumber(a,label_clusters))
    k_scale_input.set(KNumber)
    k_scale_input.pack(pady=20)

    #KFoldResultlabel = Label(root, text="\n".join(map(str, yourlist)))
    root.mainloop()

"""START GUI BUTTONS FUNCIONS"""
def setPathFile(label_data_set_path):
    global pathDataSetFile
    from tkinter import filedialog
    pathDataSetFile = filedialog.askopenfilename(title="Select a data set",
                                                filetypes = (("text files","*.txt"),("all files","*.*")))
    label_data_set_path.config(text="DATA SET path file: "+pathDataSetFile)

def setKNumber(val,label_clusters):
        global KNumber
        KNumber=val
       #print(f"Number of clusters selected: {self.clustersNumber}")
        label_clusters.config(text="Number of K selected: "+str(KNumber))

def startButton():
    if pathDataSetFile != "Not selected.":
        if pathDataSetFile != "":
            startKAlgorithm()
        else:
            tkinter.messagebox.showerror('ERROR AL INTENTAR EJECUTAR', 'Primero debe seleccionar un DATASET antes de ejecutar')
    else:
        tkinter.messagebox.showerror('ERROR AL INTENTAR EJECUTAR', 'Primero debe seleccionar un DATASET antes de ejecutar')
"""END GUI BUTTONS FUNCIONS"""

def startKAlgorithm():
    global KNumber
    global pathDataSetFile
    global KFoldResults

    #parse to int from GUI
    KNumber = int(KNumber)

    with open(pathDataSetFile, 'r') as read_dataSet:
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

    # a = (8,8,8,8,7,7,7,7)
    # aCounter = Counter(a)
    # EtiquetaMasRepetida = max(aCounter,key=aCounter.get)
    # ocurrenciasDeMaxValRep = 0
    # Kacierto=0
    # CantidadDeVecesDeLaEtiquetaMasRepetida = aCounter[EtiquetaMasRepetida]
    # for etiqueta in aCounter:
    #     #si la cantidad de la etiqueta, es igual a la cantidad de la EtiquetaMasRepetida
    #     if aCounter[etiqueta] == CantidadDeVecesDeLaEtiquetaMasRepetida:
    #         ocurrenciasDeMaxValRep=ocurrenciasDeMaxValRep+1
    # #si la cantidad de la EtiquetaMasRepetida no se repite para otras etiquetas (no hay empate)
    # if ocurrenciasDeMaxValRep == 1:
    #         Kacierto = Kacierto+1
    # print(f"el mas reptido de {a} es: {EtiquetaMasRepetida}, y por lo tanto se considera que hay: {Kacierto} acierto")


    #start algorithm
    knnAlgorithm = Knn(DataSet,KNumber)  
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
        KFoldResults.append(f"Para k={k} hay {correctCount} aciertos")
        correctCount = 0
    for Kinfo in KFoldResults:
        print(f"{Kinfo}\t")
    
    #plot
    knnAlgorithm.GenerateGrid()

    #show results popUp
    tkinter.messagebox.showinfo(title='K-Fold Validation:', message="\n".join(map(str, KFoldResults))) 

def main ():
    GUI()     

if __name__ == '__main__':
    main()