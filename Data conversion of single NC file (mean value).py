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
env.workspace = r"D:\NC\dbfload1"           ### 0--这是工作目录，更改成本次模型您的工作目录，并且每完成一个nc文件的转换，需要更换一个目录，这是因为之前的数据已经覆盖了，新的数据需要写入另外一个文件夹。

##  时间
#dass = pd.date_range('2016/01/01 10:30:00', '2016/12/31 10:30:00',freq='1D')   ## 1--修改成您的起始时间，如果是2015年的数据，则修改成2015/01/01 10:30:00；'2015/12/31 10:30:00'，其中不要修改10：30：00，这是NC数据默认的时间格式
#jk = []
#for ijs in range(0,len(dass)):
#    boxis = str(dass[ijs])
#    jk.append(boxis)
#boxit = jk

input_wenjianjia =  ['prec_2016.nc','prec_2017.nc']
yearlist = [2016,2017]

for ik in range(0,len(input_wenjianjia)):
    inNetCDFFile = "D:\\NC\\dataload\\"+str(input_wenjianjia[ik])     ## 2--把这里更改成您的NC数据的路径
    dass = pd.date_range(str(yearlist[ik])+'/01/01 10:30:00', str(yearlist[ik])+'/01/03 10:30:00',freq='1D')   ## 1--修改成您的起始时间，如果是2015年的数据，则修改成2015/01/01 10:30:00；'2015/12/31 10:30:00'，其中不要修改10：30：00，这是NC数据默认的时间格式
    jk = []
    for ijs in range(0,len(dass)):
        boxis = str(dass[ijs])
        jk.append(boxis)
    boxit = jk
    
    for ij in range(0,len(boxit)):
        variable = "prec"       ## 3--如果与prec一致，则不需要修改，如果您所分析的NC数据的变量名与此不一致，则修改成其他，如pres(气压等)
        XDimension = "lon"
        YDimension = "lat"
        year = yearlist[ik]      ## 4-- 这里我分析的是2016年，如果您的数据是2017年，可以改成2017等其他的
        outRasterLayer = "prec_"+str(year)+"_"+str(ij)+".tif"      
        bandDimmension = ""
        dimensionValues = [["time", boxit[ij]]]
        valueSelectionMethod = ""
        cellRegistration = ""
    # Execute MakeNetCDFRasterLayer
        arcpy.MakeNetCDFRasterLayer_md(inNetCDFFile, variable, XDimension, YDimension,
                                   outRasterLayer, bandDimmension, dimensionValues, 
                                   valueSelectionMethod, cellRegistration)
        
        inZoneData = r"D:\NC\BJ\Yangtze.shp"             ## 5--修改成您的子流域shp格式的目录
        zoneField = "Name"                              
        inValueRaster = "prec_"+str(year)+"_"+str(ij)+".tif"      
        outTable = "zona_"+str(year)+str(ij)+".dbf"
        outZSaT = aass.ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable,"NODATA", "MEAN")
    
    
    ###整理数据
    changdu = len(boxit)  
    def Adataframe(data):
        path = "D:\\NC\\dbfload1\\"+data+".dbf" # 6--同样修改成您的工作目录
        table = DBF(path, encoding='GBK')
        df = pd.DataFrame(iter(table))
        return df
    def pailiezuhe(changdu):
        dkl = []
        for jj in range(0,changdu):
            dsij = 'zona_'+ str(year)+str(jj)
            zona = Adataframe(dsij)
            zona = zona.drop(['COUNT','AREA'],axis=1)
            zonat = zona.set_index('Name')
            zonatt = zonat.T
            dkl.append(zonatt)
        pddkl = pd.concat(dkl)
        return pddkl
    
    final_res = pailiezuhe(changdu)
    
    final_res.to_csv('D:\\NC\\result\\'+str(year)+'_pres.csv')            ### 7--更改成您要生成数据的名字
    













