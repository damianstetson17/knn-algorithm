# pip install numpy
# pip install matplotlib

from knn import Knn
from csv import reader
from typing import List
from model.data import Data

def main ():
    with open('./dataSets/aggregation.txt', 'r') as read_dataSet:
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
            #print(f"dataset size: {len(DataSet)}")
    #start algorithm
    knnAlgorithm = Knn(DataSet,10)
    knnAlgorithm.GenerateGrid()

if __name__ == '__main__':
    main()