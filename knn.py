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
        return math.sqrt(
                            ( (x2-x1)**2 ) + ( (y2-y1)**2 )
                        )
    
    def findMinInDataSet(self) -> Data:
        xArrayPoints = [x[0] for x in self.dataSet]
        yArrayPoints = [y[1] for y in self.dataSet]

        return Data(min(xArrayPoints), min(yArrayPoints))

    def findMaxInDataSet(self) -> Data:
        xArrayPoints = [x[0] for x in self.dataSet]
        yArrayPoints = [y[1] for y in self.dataSet]

        return Data(max(xArrayPoints), max(yArrayPoints))

    def findNeighbors(self, GridPoint) -> List[Data]:
        #get the eculidian distances
        AllEuclideanDistances : List[float]  = [
                                    self.euclideanDist(GridPoint[0],GridPoint[1], data[0], data[1])
                                    for data in self.dataSet
                                    ]

        # dataset[(x,y,lbl),(xx,yy,lbl2)]
        # eucResult[2,7]
        # datasWithEucli = ([x,yy,label,2],[xx,yy,lbl2,7])
        datasWithEucli = numpy.array(self.dataSet, AllEuclideanDistances).sort( key=itemgetter(3))

        #get only the k number of Neighbors of that min euclidians
        return datasWithEucli[:self.kNeighborsNumber]

    def GenerateGrid(self) -> Any:
        #find the min & max
        CoordMin :Data  = self.findMinInDataSet()
        CoordMax :Data  = self.findMaxInDataSet()

        #make a range from x & y
        grid_x_range = numpy.arange(CoordMin[0] - 1, CoordMax[0] + 1)
        grid_y_range = numpy.arange(CoordMin[1] - 1, CoordMax[1] + 1)

        #return coordinate matrices from coordinate vectors
        grid_x, grid_y = numpy.meshgrid(grid_x_range, grid_y_range)

        NeighborsListLabel : List[Data]
        for n in range( len( grid_x.flatten() ) ):
            point = numpy.array( [grid_x.flatten()[n], grid_y.flatten()[n]] )
            NeighborsListLabel.append( self.findNeighbors(point)[:2] )

        #plot
        gridPlot = plt.figure(1)
        plt.scatter(grid_x,grid_y,
                    c = NeighborsListLabel,
                    alpha = 0.3,
                    cmap= "Set1")

        plt.scatter(self.dataSet[0],
                    self.dataSet[1],
                    c = self.dataSet[2],
                    alpha = 0.3,
                    cmap= "Set1",
                    marker="d")

        plt.show()