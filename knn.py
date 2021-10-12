import math
import numpy
from data import Data
from typing import Any, List
import matplotlib.pyplot as plt

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
        xArrayPoints:List[float] = [d.x for d in self.dataSet]
        yArrayPoints:List[float] = [d.y for d in self.dataSet]

        return Data(min(xArrayPoints), min(yArrayPoints))

    def findMaxInDataSet(self) -> Data:
        xArrayPoints:List[float] = [d.x for d in self.dataSet]
        yArrayPoints:List[float] = [d.y for d in self.dataSet]

        return Data(max(xArrayPoints), max(yArrayPoints))

    def findKFoldNeighbors(self, point:Data) -> dict[int, list[float]]:
        AllEuclideanDistances : List[float]  = [self.euclideanDist(point.x,
                                                                   point.y,
                                                                   data.x,
                                                                   data.y)for data in self.dataSet]
        
        #Unimos las distancias euclidianas de cada punto
        #con su label y ordenamos por menor eucdist
        datasWithEucli:List[dict[int, list[float]]] = []
        for i, data in enumerate(self.dataSet):
            datasWithEucli.append({
                                    "neighbor_label":data.label,
                                    "euclidean_distance":AllEuclideanDistances[i]
                                })
        datasWithEucli = sorted(datasWithEucli, key = lambda d : d["euclidean_distance"])
        #sacamos el primero que seria la distancia consigo mismo
        datasWithEucli.pop(0)
        #Ahora en la lista resultado 
        #primero guardamos el punto, luego las etiquetas
        #de los más cercanos basandonos en la lista datasWithEucli
        ListNeighbors:List[int] = []
        for data in datasWithEucli:
            ListNeighbors.append(data["neighbor_label"])

        return ({
                    "point": point,
                    "neighbors_label_list":ListNeighbors
                })

    def findNeighbors(self, GridPoint) -> List[dict[int, int, int, list[float]]]:
        #get all euclidian distances
        AllEuclideanDistances : List[float] =   [self.euclideanDist(GridPoint[0],GridPoint[1], data.x, data.y)
                                                for data in self.dataSet]
        # we got this:
        # dataset[(x,y,lbl),(xx,yy,lbl2)]
        # eucResult[2,7]
        # and we need to convert into this:
        # datasWithEucli = ([data.x, data.y ,data.label, eucDist=2],[...])
        datasWithEucli:List[Any] = []
        i=0
        for data in self.dataSet:
            datasWithEucli.append( 
                                {
                                    "x":data.x,
                                    "y":data.y,
                                    "label":data.label,
                                    "euclidean_distance":AllEuclideanDistances[i]
                                })
            i=i+1
        
        #sort by most nearby eucDist
        datasWithEucli = sorted(datasWithEucli, key=lambda d : d["euclidean_distance"])
        #get only the k number of Neighbors of that min euclidians
        return datasWithEucli[:self.kNeighborsNumber]

    def most_frequent(self, List) -> int:
        counter = 0
        num = List[0]
        
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency > counter):
                counter = curr_frequency
                num = i
        return num

    def DefineLabel(self, point) -> int:
        Neighbors:List[Any] = self.findNeighbors(point)
        labelsExist:List[int] = [n["label"] for n in Neighbors]
        return self.most_frequent(labelsExist)

    def GenerateGrid(self) -> None:
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

        fig = plt.figure()
        fig.suptitle(f"KNN con K={self.kNeighborsNumber}")
        GridAndData = fig.add_subplot(121)
        Grid = fig.add_subplot(122)

        #plot grid
        GridAndData.scatter(grid_x,grid_y,
                    c = NeighborsListLabel,
                    alpha = 0.4,
                    cmap= "tab20",
                    marker="s",
                    label="Grilla")

        #plot dataset
        GridAndData.scatter([data.x for data in self.dataSet],
                    [data.y for data in self.dataSet],
                    c = [data.label for data in self.dataSet],
                    alpha = 0.9,
                    cmap= "tab20",
                    marker="X",
                    label="Data Set",
                    linewidths=5,
                    linewidth=3)

        Grid.pcolormesh(grid_x,grid_y,
                    numpy.asarray(NeighborsListLabel).reshape(grid_x.shape),
                    shading="auto",
                    alpha = 1,
                    cmap= "tab20")

        plt.title(f"KNN con K={self.kNeighborsNumber}")

        GridAndData.set_title('Grilla con Data Set')

        Grid.set_title('Grilla')
        Grid.set_xlabel('Eje x')
        Grid.set_ylabel('Eje y')
        fig.canvas.manager.set_window_title('Inteligencia Artificial II - Gráfico KNN')
        GridAndData.legend(loc='upper center',
                   bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=5)
                   
        plt.show()