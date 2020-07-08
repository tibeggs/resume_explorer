# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:24:14 2020

@author: Timothy
"""

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('pdftotext')