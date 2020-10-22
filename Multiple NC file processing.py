# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:01:53 2020

@author: JLIN
"""

import sys 
arcpy_path = [r'D:\Arcgis\ArcGIS10.7\Lib\site-packages',r'D:\Arcgis\Desktop10.7\arcpy', r'D:\Arcgis\Desktop10.7\bin',r'D:\Arcgis\Desktop10.7\ArcToolbox\Scripts']
sys.path.extend(arcpy_path)
import arcpy
import arcpy.sa as aass
import pandas as pd
from dbfread import DBF
from arcpy import env
env.workspace = r"C:\Users\MECHREVO\Desktop\NC\dbfload"

##  时间
dass = pd.date_range('2016/01/01 10:30:00', '2016/12/31 10:30:00',freq='1D') 
jk = []
for ijs in range(0,len(dass)):
    boxis = str(dass[ijs])
    jk.append(boxis)
boxit = jk

# Set local variable
inNetCDFFile = r"C:\Users\MECHREVO\Desktop\NC\NC\Data_forcing_01dy_010deg\prec\prec_201601-201612.nc"

#variable = "prec"
#inNetCDFFile = r"C:\Users\MECHREVO\Desktop\NC\NC\Data_ancillary\elev_CMFD_V0106_B-01_010deg.nc"
for ij in range(0,len(boxit)):
    variable = "prec"
    XDimension = "lon"
    YDimension = "lat"
    outRasterLayer = "prec_2016_"+str(ij)+".tif"
    bandDimmension = ""
#dimensionValues =""
#dimensionValues = [["time", '2016/12/29 10:30:00']]
    dimensionValues = [["time", boxit[ij]]]
    valueSelectionMethod = ""
    cellRegistration = ""
# Execute MakeNetCDFRasterLayer
    arcpy.MakeNetCDFRasterLayer_md(inNetCDFFile, variable, XDimension, YDimension,
                               outRasterLayer, bandDimmension, dimensionValues, 
                               valueSelectionMethod, cellRegistration)
    
    inZoneData = r"C:\Users\MECHREVO\Desktop\NC\BJ\Yangtze.shp"
    zoneField = "Name"
    inValueRaster = "prec_2016_"+str(ij)+".tif"
    outTable = "zona_"+str(ij)+".dbf"
# Execute ZonalStatisticsAsTable
#outZSaT = aass.ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "NODATA", "MEAN")
    outZSaT = aass.ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable,"NODATA", "MEAN")

#outZSaT = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "NODATA", "MEAN", "ALL_SLICES")

###整理数据
    
changdu = len(boxit)  
def Adataframe(data):
    path = "C:\\Users\\MECHREVO\\Desktop\\NC\\dbfload\\"+data+".dbf" # 文件目录
    table = DBF(path, encoding='GBK')
    df = pd.DataFrame(iter(table))
    return df
def pailiezuhe(changdu):
    dkl = []
    for jj in range(0,changdu):
        dsij = 'zona_'+ str(jj)
        zona = Adataframe(dsij)
        zona = zona.drop(['COUNT','AREA'],axis=1)
        zonat = zona.set_index('Name')
        zonatt = zonat.T
        dkl.append(zonatt)
    pddkl = pd.concat(dkl)
    return pddkl

final_res = pailiezuhe(changdu)

final_res.to_csv('2016_pres.csv')














