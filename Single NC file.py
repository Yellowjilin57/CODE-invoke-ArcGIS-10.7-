# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys 
arcpy_path = [r'D:\Arcgis\ArcGIS10.7\Lib\site-packages',r'D:\Arcgis\Desktop10.7\arcpy', r'D:\Arcgis\Desktop10.7\bin',r'D:\Arcgis\Desktop10.7\ArcToolbox\Scripts']
sys.path.extend(arcpy_path)
import arcpy
import arcpy.sa as aass
import numpy as np

from arcpy import env
env.workspace = r"C:\Users\MECHREVO\Desktop\NC"
# Set local variable
inNetCDFFile = r"C:\Users\MECHREVO\Desktop\NC\NC\Data_forcing_01dy_010deg\prec\prec_201601-201612.nc"
#variable = "prec"
#inNetCDFFile = r"C:\Users\MECHREVO\Desktop\NC\NC\Data_ancillary\elev_CMFD_V0106_B-01_010deg.nc"
variable = "prec"
XDimension = "lon"
YDimension = "lat"
outRasterLayer = "rainfall2.tif"
bandDimmension = ""
#dimensionValues =""
#dimensionValues = [["time", '2016/12/29 10:30:00']]
dimensionValues = [["time", '2016/12/29 10:30:00']]
valueSelectionMethod = ""
cellRegistration = ""

# Execute MakeNetCDFRasterLayer
arcpy.MakeNetCDFRasterLayer_md(inNetCDFFile, variable, XDimension, YDimension,
                               outRasterLayer, bandDimmension, dimensionValues, 
                               valueSelectionMethod, cellRegistration)




inZoneData = r"C:\Users\MECHREVO\Desktop\NC\BJ\Yangtze.shp"
zoneField = "Name"
inValueRaster = "rainfall2.tif"
outTable = "zona.dbf"
# Execute ZonalStatisticsAsTable
#outZSaT = aass.ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "NODATA", "MEAN")
outZSaT = aass.ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable,"NODATA", "MEAN")

#outZSaT = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "NODATA", "MEAN", "ALL_SLICES")


import pandas as pd
from dbfread import DBF
path = r'C:\Users\MECHREVO\Desktop\NC\zona.dbf' # 文件目录
table = DBF(path, encoding='GBK')
df = pd.DataFrame(iter(table))
df = df.drop(['COUNT','AREA'],axis=1)
dft = df.set_index('Name')
dftt = dft.T


















