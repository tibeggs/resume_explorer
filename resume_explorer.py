# -*- coding: utf-8 -*-
"""
PDF/Word Document Scanner

Created on Wed Jul  1 22:30:56 2020

@author: Timothy
"""

import os
import docx
import PyPDF2
import shutil
import pandas as pd
import tkinter as tk
import configparser
import json
import textract
import sys

import win32com.client as win32
from win32com.client import constants
from glob import glob
import re




#set file path to setup
#filepathdefault ="C:\\Users\\Timothy\\Desktop\\resume runner\\"
#
##set sas and python keywords
#pythonKeywordsdefault=["python","Python"]
#sasKeywordsdefault=["SAS","sas","Sas"]
#
##create combined keyword list
#keywords=pythonKeywords+sasKeywords
#
##create filepath directions
#filepathInput=filepath+"Input\\"
#filepathContinue=filepath+"Continue\\"
#filepathDisregard=filepath+"Disregard\\"
#
##read all files in input directory
#files=os.listdir(filepathInput)
#
##create dataframe with all file names and counter for sas and python
#filedf=pd.DataFrame(data={'file':files})
#filedf['python']=0
#filedf['sas']=0

#function to pass multiple functions to single object
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


class rGUI:
    def __init__(self,window):
        #exit program
        def close_all(self):
            rGUI.filepath=self.efp.get()
            rGUI.pythonKeywords=self.epk.get().split(" ")
            rGUI.sasKeywords=self.esk.get().split(" ")
            rGUI.keywords = rGUI.pythonKeywords+rGUI.sasKeywords
            rGUI.pythonC=int(self.epc.get())
            rGUI.sasC=int(self.esc.get())
            window.destroy()
            
        self.window=window
        rGUI.keywords = rGUI.pythonKeywords+rGUI.sasKeywords
        window.grid_columnconfigure(0,weight=1)
        window.grid_columnconfigure(1,weight=1)
        window.grid_rowconfigure(0,weight=1)
        window.grid_rowconfigure(1,weight=1)
        window.grid_rowconfigure(2,weight=1)
        window.grid_rowconfigure(3,weight=1)
        window.grid_rowconfigure(4,weight=1)
        window.grid_rowconfigure(5,weight=1)
        
        lfp = tk.Label(window, text="Program Directory:", anchor="w",font="Arial 10")
        lpk=tk.Label(window, text="String 1 Keywords (separate with spaces):", anchor="w",font="Arial 10")
        lpc=tk.Label(window, text="Number of Occurences of Values in String 1:", anchor="w",font="Arial 10")
        lsk=tk.Label(window, text="String 2 Keywords (separate with spaces):", anchor="w",font="Arial 10")
        lsc=tk.Label(window, text="Number of Occurences of Values in String 2:", anchor="w",font="Arial 10")
        

        lfp.grid(row=1,column=0)
        lpk.grid(row=2,column=0)
        lpc.grid(row=3,column=0)
        lsk.grid(row=4,column=0)
        lsc.grid(row=5,column=0)
        
        
        self.efp = tk.Entry(window, width=50)
        self.efp.insert(tk.END,rGUI.filepath)
        
        self.epk = tk.Entry(window, width=50)
        self.epk.insert(tk.END,rGUI.pythonKeywords)
        
        self.epc = tk.Entry(window, width=50)
        self.epc.insert(tk.END, rGUI.pythonC)
        
        self.esk = tk.Entry(window, width=50)
        self.esk.insert(tk.END,rGUI.sasKeywords)
        
        
        self.esc = tk.Entry(window, width=50)
        self.esc.insert(tk.END, rGUI.sasC)
        
        self.efp.grid(row=1,column=1, sticky='ew')
        self.epk.grid(row=2,column=1, sticky='ew')
        self.epc.grid(row=3, column=1, sticky='ew')
        self.esk.grid(row=4,column=1, sticky='ew')
        self.esc.grid(row=5,column=1, sticky='ew')
        
        buttonv = tk.Button(window, text = "Submit", command = lambda: close_all(self))
        buttonv.grid(row=6,column=0, columnspan=2)
        
        
if __name__=="__main__":
    #define argument and data directories from config strings
    config=configparser.ConfigParser()
    if getattr(sys, 'frozen', False):
        # frozen
        cpath = os.path.dirname(sys.executable)  
    else:
        # unfrozen
        cpath = os.path.dirname(os.path.realpath(__file__))
    #cpath=os.path.dirname(os.path.realpath(__file__))
    config.read(cpath+"/r_config.ini")
    
    rGUI.pythonKeywords=json.loads(config.get('DEFAULT','cpythonKeywords'))
    rGUI.sasKeywords= json.loads(config.get('DEFAULT','csasKeywords'))
    rGUI.filepath=config['DEFAULT']['cfilepath']
    rGUI.pythonC=int(config['DEFAULT']['cpythoncount'])
    rGUI.sasC=int(config['DEFAULT']['csascount'])
    
    master = tk.Tk()
    window = rGUI(master)
     
    #run primary gui
    tk.mainloop()
        
    


#create filepath directions
filepathInput=rGUI.filepath+"Input\\"
filepathContinue=rGUI.filepath+"Continue\\"
filepathDisregard=rGUI.filepath+"Disregard\\"

#read all files in input directory
files=os.listdir(filepathInput)

# Create list of paths to .doc files
paths = glob(filepathInput+'*.doc', recursive=True)

def save_as_docx(path):
    # Opening MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(path)
    doc.Activate ()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(re.escape(r'\.\w+$'), '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    doc.Close(False)

for path in paths:
    save_as_docx(path)
    os.remove(path)



#for f in files:
#    if f.endswith(".doc"):
#        shutil.move(filepathInput+f,filepathInput+f+"x")
#files=os.listdir(filepathInput)

#create dataframe with all file names and counter for sas and python
files=os.listdir(filepathInput)
filedf=pd.DataFrame(data={'file':files})
filedf['python']=0
filedf['sas']=0


        
#check for if keywords appear in paragraph or page
for f in files:
    if ".docx" in f:
        document=docx.Document(filepathInput+f)
        for k in rGUI.keywords:
            for p in document.paragraphs:
                if k in p.text:
                    kcount=p.text.count(k)
                    print(f+" contains "+k)
                    if k in rGUI.pythonKeywords:
                        filedf.loc[filedf['file']==f,'python']+=kcount
                    if k in rGUI.sasKeywords:
                        filedf.loc[filedf['file']==f,'sas']+=kcount

    if ".pdf" in f:
        pdfFileObj=open(filepathInput+f, mode="rb")
        pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
        for p in range(0,pdfReader.numPages-1):
            pdfPage=pdfReader.getPage(p)
            pageText=pdfPage.extractText()
            for k in rGUI.keywords:
                if k in pageText:
                    kcount=pageText.count(k)
                    print(f+" contains "+k)
                    if k in rGUI.pythonKeywords:
                        filedf.loc[filedf['file']==f,'python']+=kcount
                    if k in rGUI.sasKeywords:
                        filedf.loc[filedf['file']==f,'sas']+=kcount
        pdfFileObj.close()
        
fileDC=filedf.loc[(filedf['sas']==0) | (filedf['python']==0)]
for f in fileDC['file']:
    text=str(textract.process(filepathInput+f))
    for k in rGUI.keywords:
        if k in text:
            kcount=text.count(k)
            print(f+" contains "+k)
            if k in rGUI.pythonKeywords:
                filedf.loc[filedf['file']==f,'python']+=kcount
            if k in rGUI.sasKeywords:
                filedf.loc[filedf['file']==f,'sas']+=kcount
        

#subset file dataframe into continuers and Disregard
fileCon=filedf.loc[(filedf['sas']>rGUI.sasC) | (filedf['python']>rGUI.pythonC)]
fileDis=filedf.loc[(filedf['sas']<=rGUI.sasC) & (filedf['python']<=rGUI.pythonC)]

#move files to appropriate loaction
for f1 in fileCon['file']:
    shutil.move(filepathInput+f1,filepathContinue+f1)
for f2 in fileDis['file']:
    shutil.move(filepathInput+f2,filepathDisregard+f2)
    
        
        
        
    