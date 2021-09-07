import math
import numpy
from model.data import Data
from typing import Any, List
import matplotlib.pyplot as plt
from operator import itemgetter

class Knn:
    def __init__(self, dataSet: List[Data], kNeighborsNumber: int) -> None:
        self.dataSet : List[Data]   = dataSet
        self.kNeighborsNumber : int = kNeighborsNumber
    
    def euclideanDist(self, x1:float, y1:float, x2:float, y2:float) -> float:
        return round(
                math.sqrt(
                            ( (x2-x1)**2 ) + ( (y2-y1)**2 )
                        ),2)
    
    def findMinInDataSet(self) -> Data:
        xArrayPoints = [d.x for d in self.dataSet]
        yArrayPoints = [d.y for d in self.dataSet]

        return Data(min(xArrayPoints), min(yArrayPoints))

    def findMaxInDataSet(self) -> Data:
        xArrayPoints = [d.x for d in self.dataSet]
        yArrayPoints = [d.y for d in self.dataSet]

        return Data(max(xArrayPoints), max(yArrayPoints))

    def findNeighbors(self, GridPoint) -> List[Any]:
        #get all euclidian distances
        AllEuclideanDistances : List[float]  = [
                                    self.euclideanDist(GridPoint[0],GridPoint[1], data.x, data.y)
                                    for data in self.dataSet
                                    ]
        # we got this:
        # dataset[(x,y,lbl),(xx,yy,lbl2)]
        # eucResult[2,7]
        # and we need to convert into this:
        # datasWithEucli = ([data.x, data.y ,data.label, eucDist=2],[...])
        datasWithEucli = []
        i=0
        for data in self.dataSet:
            datasWithEucli.append( [data.x, data.y, data.label, AllEuclideanDistances[i]] )
            i=i+1
        
        #sort by most nearby eucDist
        datasWithEucli = sorted(datasWithEucli, key=lambda d : d[3])
        #get only the k number of Neighbors of that min euclidians
        #print(f"Primeros {self.kNeighborsNumber} vecinos de [{GridPoint[0]},{GridPoint[1]}]: {datasWithEucli[:self.kNeighborsNumber]}")
        return datasWithEucli[:self.kNeighborsNumber]

    def most_frequent(self,List) -> int:
        counter = 0
        num = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i
        return num

    def DefineLabel(self, point) -> int:
        Neighbors : List[Any] = self.findNeighbors(point)
        labelsExist = [n[2] for n in Neighbors]
        return self.most_frequent(labelsExist)

    def GenerateGrid(self) -> Any:
        #find the min & max
        CoordMinData :Data  = self.findMinInDataSet()
        CoordMaxData :Data  = self.findMaxInDataSet()

        #make a range from x & y
        grid_x_range = numpy.arange(CoordMinData.x - 1, CoordMaxData.x + 1, 0.5)
        grid_y_range = numpy.arange(CoordMinData.y - 1, CoordMaxData.y + 1, 0.5)

        #return coordinate matrices from coordinate vectors
        grid_x, grid_y = numpy.meshgrid(grid_x_range, grid_y_range)

        NeighborsListLabel : List[Data] = []
        for n in range( len( grid_x.flatten() ) ):
            point = numpy.array( [grid_x.flatten()[n], grid_y.flatten()[n]] )
            NeighborsListLabel.append( self.DefineLabel(point) )

        #plot
        gridPlot = plt.figure(1)
        plt.scatter(grid_x,grid_y,
                    c = NeighborsListLabel,
                    alpha = 0.5,
                    cmap= "Set1",
                    marker="s",)

        plt.scatter([data.x for data in self.dataSet],
                    [data.y for data in self.dataSet],
                    c = [data.label for data in self.dataSet],
                    alpha = 0.9,
                    cmap= "Set1",
                    marker="x",
                    linewidths=5,
                    linewidth=3)

        plt.show()