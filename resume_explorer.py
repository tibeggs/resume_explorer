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

#set file path to setup
filepath ="C:\\Users\\Timothy\\Desktop\\resume runner\\"

#set sas and python keywords
pythonKeywords=["python","Python"]
sasKeywords=["SAS","sas","Sas"]

#create combined keyword list
keywords=pythonKeywords+sasKeywords

#create filepath directions
filepathInput=filepath+"Input\\"
filepathContinue=filepath+"Continue\\"
filepathDisregard=filepath+"Disregard\\"

#read all files in input directory
files=os.listdir(filepathInput)

#create dataframe with all file names and counter for sas and python
filedf=pd.DataFrame(data={'file':files})
filedf['python']=0
filedf['sas']=0

#check for if keywords appear in paragraph or page
for f in files:
    if ".docx" in f:
        document=docx.Document(filepathInput+f)
        for k in keywords:
            for p in document.paragraphs:
                if k in p.text:
                    kcount=p.text.count(k)
                    print(f+" contains "+k)
                    if k in pythonKeywords:
                        filedf.loc[filedf['file']==f,'python']+=kcount
                    if k in sasKeywords:
                        filedf.loc[filedf['file']==f,'sas']+=kcount

    if ".pdf" in f:
        pdfFileObj=open(filepathInput+f, mode="rb")
        pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
        for p in range(0,pdfReader.numPages-1):
            print(p)
            pdfPage=pdfReader.getPage(p)
            pageText=pdfPage.extractText()
            for k in keywords:
                if k in pageText:
                    kcount=pageText.count(k)
                    print(f+" contains "+k)
                    if k in pythonKeywords:
                        filedf.loc[filedf['file']==f,'python']+=kcount
                    if k in sasKeywords:
                        filedf.loc[filedf['file']==f,'sas']+=kcount
        pdfFileObj.close()

#subset file dataframe into continuers and Disregard
fileCon=filedf.loc[(filedf['sas']>2) | (filedf['python']>3)]
fileDis=filedf.loc[(filedf['sas']<=2) & (filedf['python']<=3)]

#move files to appropriate loaction
for f1 in fileCon['file']:
    shutil.move(filepathInput+f1,filepathContinue+f1)
for f2 in fileDis['file']:
    shutil.move(filepathInput+f2,filepathDisregard+f2)
    
        
        
        
    
            
    