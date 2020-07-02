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


filepath ="C:\\Users\\Timothy\\Desktop\\resume runner\\"

pythonKeywords=["python","Python"]
sasKeywords=["SAS","sas","Sas"]

keywords=pythonKeywords+sasKeywords

filepathInput=filepath+"Input\\"
filepathContinue=filepath+"Continue\\"
filepathDisregard=filepath+"Disregard\\"

files=os.listdir(filepathInput)

filedf=pd.DataFrame(data={'file':files})
filedf['python']=0
filedf['sas']=0

#f="Tiffany Negri Resume.docx"

for f in files:
    if ".docx" in f:
        document=docx.Document(filepathInput+f)
        for k in keywords:
            for p in document.paragraphs:
                if k in p.text:
                    kcount=p.text.count(k)
                    #print(p.text)
                    #print()
                    print(f+" contains "+k)
                    if k in pythonKeywords:
                        filedf.loc[filedf['file']==f,'python']+=kcount
                    if k in sasKeywords:
                        filedf.loc[filedf['file']==f,'sas']+=kcount
        #os.remove(filepathInput+f)
                    #need to change this to wait for end of file
                    #os.rename(filepathInput+f,filepathContinue+f)
                #else:
                    #need to change this to wait for end of file
                    #os.rename(filepathInput+f,filepathDisregard+f)
    if ".pdf" in f:
        pdfFileObj=open(filepathInput+f, mode="rb")
        pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
        for p in range(0,pdfReader.numPages-1):
            print(p)
            pdfPage=pdfReader.getPage(p)
            pageText=pdfPage.extractText()
            #print(pageText)
            for k in keywords:
                if k in pageText:
                    kcount=pageText.count(k)
                    print(f+" contains "+k)
                    if k in pythonKeywords:
                        filedf.loc[filedf['file']==f,'python']+=kcount
                    if k in sasKeywords:
                        filedf.loc[filedf['file']==f,'sas']+=kcount
        pdfFileObj.close()
        #os.remove(filepathInput+f)
                    #need to change this to wait for end of file
                    #pdfFileObj.close()
                    #shutil.move(filepathInput+f,filepathContinue+f)
                #else:
                    #need to change this to wait for end of file
                    #pdfFileObj.close()
                    #shutil.move(filepathInput+f,filepathDisregard+f)

#document=docx.Document()
fileCon=filedf.loc[(filedf['sas']>2) | (filedf['python']>3)]
fileDis=filedf.loc[(filedf['sas']<=2) & (filedf['python']<=3)]

for f1 in fileCon['file']:
    shutil.move(filepathInput+f1,filepathContinue+f1)
for f2 in fileDis['file']:
    shutil.move(filepathInput+f2,filepathDisregard+f2)
    
        
        
        
    
            
    