import main
import mixer_tool
from tkinter import *
from tkinter import ttk
import tkinter.messagebox

root = Tk()
KNumber = 1
pathDataSetFile = "Not selected."
frame_values_selected = LabelFrame(root, text="SELECTED VALUES", padx=65,pady=71.5)

#number k table label
kfold_results_table = ttk.Treeview(frame_values_selected, columns=("#1","#2"), show="headings")
kfold_results_table.heading("#1", text="K Value",anchor=N)
kfold_results_table.heading("#2", text="Success",anchor=N)
kfold_results_table.column("#1",anchor=N)
kfold_results_table.column("#2",anchor=N)

def generate_main_menu ():
    global KNumber
    global pathDataSetFile
    
    root.title("Main Menú - KNN - Stetson & Piotroski")
    #initial values for start the algorithm
    frame_values_selected.grid(row=1, column=1)
    label_data_set_path = Label(frame_values_selected, text="DATA SET path file: "+pathDataSetFile)
    label_data_set_path.pack()
    #number k label
    label_clusters = Label(frame_values_selected, text="Number of k selected: "+str(KNumber))
    label_clusters.pack(pady=10)
    
    #start the K algorithm button
    button_start_K = Button(frame_values_selected,text="START KNN ALGORITHM",
                            command=startKNNButton)
    button_start_K.pack(pady=10)
    #start the K algorithm button
    button_start_K = Button(frame_values_selected,text="START KFOLDVALIDATION ALGORITHM",
                            command=startKFoldButton)
    button_start_K.pack(pady=10)

    #inputs frame
    frame_inputs = LabelFrame(root, text="INITIAL VALUES", padx=50,pady=50)
    frame_inputs.grid(row=1, column=0)
    button_select_data_set = Button(frame_inputs, text = "Select DATA SET .txt file", width=25,
                                        command = lambda: setPathFile(label_data_set_path))
    button_select_data_set.pack()

    #Este btn solo es utilizado en desarrollo para el informe como generador de mezclas.
    #button_shuffle = Button(frame_inputs, text = "Generate a shuffle", width=25,
                                       # command = lambda: generateSuffle(pathDataSetFile))
    #button_shuffle.pack(pady=5)

    #k scale
    k_scale_input = Scale(frame_inputs, label="Select the number of K:", 
                            from_=1, to=10, orient=HORIZONTAL, length=200,
                            command = lambda a: setKNumber(a,label_clusters))
    k_scale_input.set(KNumber)
    k_scale_input.pack(pady=10)

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

def startKNNButton():
    if pathDataSetFile != "Not selected.":
        if pathDataSetFile != "":
            main.startKnn()
        else:
            tkinter.messagebox.showerror('ERROR AL INTENTAR EJECUTAR', 'Primero debe seleccionar un DATASET antes de ejecutar')
    else:
        tkinter.messagebox.showerror('ERROR AL INTENTAR EJECUTAR', 'Primero debe seleccionar un DATASET antes de ejecutar')

def startKFoldButton():
    if pathDataSetFile != "Not selected.":
        if pathDataSetFile != "":
            main.startKFold()
        else:
            tkinter.messagebox.showerror('ERROR AL INTENTAR EJECUTAR', 'Primero debe seleccionar un DATASET antes de ejecutar')
    else:
        tkinter.messagebox.showerror('ERROR AL INTENTAR EJECUTAR', 'Primero debe seleccionar un DATASET antes de ejecutar')

def generateSuffle(pathDataSetFile):
    if pathDataSetFile != "Not selected.":
        if pathDataSetFile != "":
            mixer_tool.generateShuffle(pathDataSetFile)
        else:
            tkinter.messagebox.showerror('ERROR AL INTENTAR MEZCLAR', 'Primero debe seleccionar un DATASET antes de ejecutar')
    else:
        tkinter.messagebox.showerror('ERROR AL INTENTAR MEZCLAR', 'Primero debe seleccionar un DATASET antes de ejecutar')