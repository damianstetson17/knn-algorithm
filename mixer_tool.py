import random
from csv import reader
from typing import List
import tkinter.messagebox

def generateShuffle(pathDataSetFile: str) -> None:
    dataListRow:List[str] = []
    with open(pathDataSetFile, 'r') as read_dataSet:
            csv_reader = reader(read_dataSet)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                dataListRow.append(row[0].split())
            
            random.shuffle(dataListRow)
            filename:str= read_dataSet.name.split("/")[-1]
            newSufflefilename:str= f'datasets/mixed_{filename}'

            with open(newSufflefilename, 'w') as f:
                for i,r in enumerate(dataListRow):
                    f.write(f"{r[0]} {r[1]} {r[2]}\n")
            tkinter.messagebox.showinfo(title="Éxito al crear mezcla", message=f"Se generó el dataset mezclando 'mixed_{filename}'")