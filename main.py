# pip install numpy
# pip install matplotlib

import gui
from knn import Knn
from data import Data
import kfoldvalidation
from csv import reader
from typing import List

def startKFold():
    #parse to int from GUI input
    KNumber:int = int(gui.KNumber)

    #read from .txt dataset
    with open(gui.pathDataSetFile, 'r') as read_dataSet:
        csv_reader = reader(read_dataSet)
        DataSet : List[Data] = []
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
    
    #Instace of a KNN object 
    knnAlgorithm:Knn = Knn(DataSet,KNumber)

    #Exec the Kfold validation
    kfoldvalidation.executeValidation(knnAlgorithm)

def startKnn():
    #parse to int from GUI input
    KNumber:int = int(gui.KNumber)

    #read from .txt dataset
    with open(gui.pathDataSetFile, 'r') as read_dataSet:
        csv_reader = reader(read_dataSet)
        DataSet : List[Data] = []
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
            
    knnAlgorithm:Knn = Knn(DataSet,KNumber)
    #Execute KNN algorithm and generate the grid
    knnAlgorithm.GenerateGrid()

def main ():
    gui.generate_main_menu()     

if __name__ == '__main__':
    main()