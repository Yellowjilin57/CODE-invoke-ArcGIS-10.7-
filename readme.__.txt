1。准备python环境。如果您的电脑以前安装过python3.7的话，需要重新安装python2.7；由于arcgis的独特机制，因此只支持python2.7；
如果您的电脑之前没有配置过python,推荐您使用anaconda2（一个集成了所有必备工具的包），下载地址：
https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/

下载的版本需要对应您的arcgis版本，如果您的arcgis版本是10.7（对应的python是2.7.15），您可以下载anaconda2-5.3.0（32位）。其他的arcgis版本，可以参照您arcgis对应的python版本进行下载。 

2。下载了之后，安装到您的自定义位置，并勾选这两个选项（添加到环境变量）。随后点击确定等，完成安装。
 

3。安装完anaconda之后，就可以从windows开始界面打开python的IDLE，spyder进行编程了。
 
4。需要配置您电脑上的python的环境变量，因为需要与arcgis上的python连理。因此需要在spyder里输入如下语句：里面需要修改成您电脑的arcgis对应的目录。

1.	import sys   
2.	  
3.	arcpy_path = [
4.	r'D:\Arcgis\ArcGIS10.7\Lib\sitepackages', 
5.	r'D:\Arcgis\Desktop10.7\arcpy', 
6.	r'D:\Arcgis\Desktop10.7\bin',
7.	r'D:\Arcgis\Desktop10.7\ArcToolbox\Scripts']  
8.	  
9.	sys.path.extend(arcpy_path)  

5。随后输入：
1.	import arcpy  
2.	import arcpy.sa as aass  

如果没有报错，就说明环境配置成功，已经可以开始分析了。如果有报错，请联系我，我们一起分析一下问题所在。

6。打开CMD，输入pip install dbfread
如果有其他提示，请按照它的提示，安装dbfread，这是数据库转换工具。

7. 需要更改的地方，都标注并编了号，一共有0-7步需要更改成您想要的格式。更改的内容都在注释里。

1.	import sys   
2.	arcpy_path = [r'D:\Arcgis\ArcGIS10.7\Lib\site-packages',r'D:\Arcgis\Desktop10.7\arcpy', r'D:\Arcgis\Desktop10.7\bin',r'D:\Arcgis\Desktop10.7\ArcToolbox\Scripts']  
3.	sys.path.extend(arcpy_path)  
4.	import arcpy  
5.	import arcpy.sa as aass  
6.	import pandas as pd  
7.	from dbfread import DBF  
8.	from arcpy import env  
9.	env.workspace = r"C:\Users\MECHREVO\Desktop\NC\dbfload"           ### 0--这是工作目录，更改成本次模型您的工作目录，并且每完成一个nc文件的转换，需要更换一个目录，这是因为之前的数据已经覆盖了，新的数据需要写入另外一个文件夹。  
10.	  
11.	##  时间  
12.	dass = pd.date_range('2016/01/01 10:30:00', '2016/12/31 10:30:00',freq='1D')   ## 1--修改成您的起始时间，如果是2015年的数据，则修改成2015/01/01 10:30:00；'2015/12/31 10:30:00'，其中不要修改10：30：00，这是NC数据默认的时间格式  
13.	jk = []  
14.	for ijs in range(0,len(dass)):  
15.	    boxis = str(dass[ijs])  
16.	    jk.append(boxis)  
17.	boxit = jk  
18.	  
19.	  
20.	# Set local variable  
21.	inNetCDFFile = r"C:\Users\MECHREVO\Desktop\NC\NC\Data_forcing_01dy_010deg\prec\prec_201601-201612.nc"     ## 2--把这里更改成您的NC数据的路径  
22.	  
23.	for ij in range(0,len(boxit)):  
24.	    variable = "prec"       ## 3--如果与prec一致，则不需要修改，如果您所分析的NC数据的变量名与此不一致，则修改成其他，如pres(气压等)  
25.	    XDimension = "lon"  
26.	    YDimension = "lat"  
27.	    year = 2016      ## 4-- 这里我分析的是2016年，如果您的数据是2017年，可以改成2017等其他的  
28.	    outRasterLayer = "prec_"+str(year)+"_"+str(ij)+".tif"        
29.	    bandDimmension = ""  
30.	    dimensionValues = [["time", boxit[ij]]]  
31.	    valueSelectionMethod = ""  
32.	    cellRegistration = ""  
33.	# Execute MakeNetCDFRasterLayer  
34.	    arcpy.MakeNetCDFRasterLayer_md(inNetCDFFile, variable, XDimension, YDimension,  
35.	                               outRasterLayer, bandDimmension, dimensionValues,   
36.	                               valueSelectionMethod, cellRegistration)  
37.	      
38.	    inZoneData = r"C:\Users\MECHREVO\Desktop\NC\BJ\Yangtze.shp"             ## 5--修改成您的子流域shp格式的目录  
39.	    zoneField = "Name"                                
40.	    inValueRaster = "prec_"+str(year)+"_"+str(ij)+".tif"        
41.	    outTable = "zona_"+str(ij)+".dbf"  
42.	    outZSaT = aass.ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable,"NODATA", "MEAN")  
43.	  
44.	  
45.	###整理数据  
46.	changdu = len(boxit)    
47.	def Adataframe(data):  
48.	    path = "C:\\Users\\MECHREVO\\Desktop\\NC\\dbfload\\"+data+".dbf" # 6--同样修改成您的工作目录  
49.	    table = DBF(path, encoding='GBK')  
50.	    df = pd.DataFrame(iter(table))  
51.	    return df  
52.	def pailiezuhe(changdu):  
53.	    dkl = []  
54.	    for jj in range(0,changdu):  
55.	        dsij = 'zona_'+ str(jj)  
56.	        zona = Adataframe(dsij)  
57.	        zona = zona.drop(['COUNT','AREA'],axis=1)  
58.	        zonat = zona.set_index('Name')  
59.	        zonatt = zonat.T  
60.	        dkl.append(zonatt)  
61.	    pddkl = pd.concat(dkl)  
62.	    return pddkl  
63.	  
64.	final_res = pailiezuhe(changdu)  
65.	  
66.	final_res.to_csv('2016_pres.csv')            ### 7--更改成您要生成数据的名字  

