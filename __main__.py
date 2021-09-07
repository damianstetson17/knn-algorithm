# pip install numpy

from knn import Knn
from typing import List
from model.data import Data


def main ():
    #NOT WORKING
    DataSet : List[Data] = []
    #print("# Loading data from txt:\t\t     #")
    data_file_txt = open("data_r2.txt", "r")
    for data in data_file_txt.readlines():
        vectorString = ""
        for caracter in enumerate(data[0:],2):
            if(caracter[1] == ","):
                vectorString+=" " 
            else:
                vectorString+=caracter[1]
        vector = vectorString.split()
        DataSet.append(
            Data( float(vector[0]), float(vector[1]), int(vector[2]) )
        )
    data_file_txt.close()
    knnAlgorithm = Knn(DataSet,10)

if __name__ == '__main__':
    main()