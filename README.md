# CODE-invoke-ArcGIS-10.7-
This code is mainly called ArcGIS to achieve automatic operation

————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

1。 Prepare the python environment. If you have previously installed Python 3.7 on your computer, you need to re install python2.7. Due to the unique mechanism of ArcGIS, only python2.7 is supported;
If your computer has not been configured with Python before, it is recommended that you use anaconda2 (a package that integrates all the necessary tools). Download address:
https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/
The download version needs to correspond to your ArcGIS version. If your ArcGIS version is 10.7 (the corresponding Python version is 2.7.15), you can download anaconda2-5.3.0 (32-bit). Other ArcGIS versions can be downloaded according to the python version corresponding to ArcGIS.
2。 After downloading, install to your custom location and check both options (add to environment variables). Then click OK to complete the installation.
3。 After installing anaconda, you can open Python idle and Spyder from the windows start interface for programming.
4。 You need to configure the environment variables for Python on your computer, because you need to connect with Python on ArcGIS. So you need to enter the following statement in Spyder: it needs to be changed to the directory corresponding to ArcGIS of your computer.
1.	import sys
Two
3.	arcpy_ path = [
4.	r'D:\Arcgis\ArcGIS10.7\Lib\sitepackages',
5.	r'D:\Arcgis\Desktop10.7\arcpy',
6.	r'D:\Arcgis\Desktop10.7\bin',
7.	r'D:\Arcgis\Desktop10.7\ArcToolbox\Scripts']
Eight
Nine sys.path.extend (arcpy_ path)
5。 Then enter:
1.	import arcpy
2.	import  arcpy.sa  as aass
If no error is reported, the environment configuration is successful and the analysis can be started. If there is an error, please contact me and we will analyze the problem together.
6。 Open CMD and enter PIP install dbfread
If you have other prompts, follow its instructions and install dbfread, the database conversion tool.
7. The places that need to be changed are marked and numbered. There are 0-7 steps to change to the format you want. The changes are all in the comments.
1.	import sys
2.	arcpy_ path = [r'D:\Arcgis\ArcGIS10.7\Lib\site-packages',r'D:\Arcgis\Desktop10.7\arcpy', r'D:\Arcgis\Desktop10.7\bin',r'D:\Arcgis\Desktop10.7\ArcToolbox\Scripts']
Three sys.path.extend (arcpy_ path)
4.	import arcpy
5.	import  arcpy.sa  as aass
6.	import pandas as pd
7.	from dbfread import DBF
8.	from arcpy import env
Nine env.workspace  =This is the working directory. Change your working directory in the cost sub model. Every time you complete the conversion of an NC file, you need to change a directory. This is because the previous data has been covered, and the new data needs to be written to another folder.
Ten
11. Time
12.	dass =  pd.date_ Range ('2016 / 01 / 01 10:30:00 ','2016 / 12 / 31 10:30:00', freq'1d ')) ාාාාාාාාාාාාාා񖓿񖓿񖓿ාා񖓿񖓿ාා#######ා
13.	jk = []
14.	for ijs in range(0,len(dass)):
15.	    boxis = str(dass[ijs])
sixteen jk.append (boxis)
17.	boxit = jk
Eighteen
Nineteen
20.	# Set local variable
21.	inNetCDFFile = r"C:\Users\MECHREVO\Desktop\NC\NC\Data_ forcing_ 01dy_ 010deg\prec\prec_ 201601-201612. NC "ාා 2 -- change this to the path of your NC data
Twenty-two
23.	for ij in range(0,len(boxit)):
24. Variable = "prec" ාාාාාාාාාාාාාාාාාාාාා񖓿񖓿񖓿ා
25.	    XDimension = "lon"
26.	    YDimension = "lat"
27. Year = 2016 ා 4 -- here I analyze 2016. If your data is 2017, you can change it to 2017 and others
28.	    outRasterLayer = "prec_ "+str(year)+"_ "+str(ij)+".tif"
29.	    bandDimmension = ""
30.	    dimensionValues = [["time", boxit[ij]]]
31.	    valueSelectionMethod = ""
32.	    cellRegistration = ""
33.	# Execute MakeNetCDFRasterLayer
thirty-four arcpy.MakeNetCDFRasterLayer_ md(inNetCDFFile, variable, XDimension, YDimension,
35.	                               outRasterLayer, bandDimmension, dimensionValues,
36.	                               valueSelectionMethod, cellRegistration)
Thirty-seven
38.	    inZoneData = r"C:\Users\MECHREVO\Desktop\NC\BJ\ Yangtze.shp "ාාාාාාාාාාාාාාාාාාා
39.	    zoneField = "Name"
40.	    inValueRaster = "prec_ "+str(year)+"_ "+str(ij)+".tif"
41.	    outTable = "zona_ "+str(ij)+".dbf"
42.	    outZSaT =  aass.ZonalStatisticsAsTable (inZoneData, zoneField, inValueRaster, outTable,"NODATA", "MEAN")
Forty-three
Forty-four
45. Sorting out data
46.	changdu = len(boxit)
47.	def Adataframe(data):
48. Path = "C: \ \ users \ \ mechrevo \ \ desktop \ \ NC \ \ dbfloat \ \" + data + ". DBF" ා 6 -- also change to your working directory
49.	    table = DBF(path, encoding='GBK')
50.	    df =  pd.DataFrame (iter(table))
51.	    return df
52.	def pailiezuhe(changdu):
53.	    dkl = []
54.	    for jj in range(0,changdu):
55.	        dsij = 'zona_ '+ str(jj)
56.	        zona = Adataframe(dsij)
57.	        zona =  zona.drop (['COUNT','AREA'],axis=1)
58.	        zonat =  zona.set_ index('Name')
