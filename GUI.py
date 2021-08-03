'''
Created on Jul 21, 2021

@author: suvanamruth
'''
from tkinter import *
from tkinter import filedialog, Text
import Dictionary
from Dictionary import mainFunction
from tkinter import ttk

root = Tk()
root.title("Analyze Showtech Files")

inputFileDir = "blank"
DictionaryDir = "blank"

def open():
    global inputFileDir
    root.filename = filedialog.askopenfilename(initialdir = "/", title = "Choose Input File")
    text = "File Selected: " + root.filename
    label = Label(root, text = text).pack()
    inputFileDir = root.filename 
    
def openDict():
    global DictionaryDir
    root.filename2 = filedialog.askopenfilename(initialdir = "/", title = "Choose Dictionary File")
    text2 = "Dictionary Selected: " + root.filename2
    label = Label(root, text = text2).pack()
    DictionaryDir = root.filename2
    
btn = Button(root, text = "Open Input File", command = open).pack()
btn2 = Button(root,text = "Open Dictionary", command = openDict).pack()

def analyze():
    global inputFileDir
    global DictionaryDir
    mainFunction(inputFileDir, DictionaryDir)
    my_tree = ttk.Treeview(root, show = ["headings"])
    my_tree['columns'] = ("Warning Level", "String Found", "Filename", "Component")
    my_tree.column("Warning Level", width = 120)
    my_tree.column("String Found", width = 300)
    my_tree.column("Filename", width = 720)
    my_tree.column("Component", width = 120) 
    
    my_tree.heading("Warning Level", text = "Warning Level", anchor = W)
    my_tree.heading("String Found", text = "String Found", anchor = W)
    my_tree.heading("Filename", text = "Filename", anchor = W)
    my_tree.heading("Component", text = "Component", anchor = W)
    for i in Dictionary.results:
        my_tree.insert(parent = "", index = "end", values = i)
    
    my_tree.pack()

btn3 = Button(root,text = "Analyze", command = analyze).pack()
    

root.mainloop()