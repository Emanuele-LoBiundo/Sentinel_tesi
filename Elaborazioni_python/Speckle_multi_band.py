#STatistica zonale
import arcpy
from arcpy import env
import os
env.workspace = "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\Merge_VV"
rasters = arcpy.ListRasters()
rasters.sort()
destination_path= "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\StatisticaZonale_VV"



for k in rasters:
     outRaster = os.path.join(destination_path, k[:-4] + ".dbf")
     z = arcpy.gp.ZonalStatisticsAsTable_sa("D:\\ArcGISProjects\\Verona\\Multi_temporal_Speckle.gdb\\Uso_suolo_Multi_Speckle_VV", "Id", k,  outRaster, "DATA", "MEAN")
     print(k + "_____done.")



arcpy.env.workspace = "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\StatisticaZonale_VV"
outLocation = "D:\\ArcGISProjects\\Verona\\Multi_temporal_Speckle.gdb"
tablesmove = arcpy.ListTables()

for table in tablesmove:
          arcpy.TableToGeodatabase_conversion(table, outLocation)

#Cambia nomi
arcpy.env.workspace = "D:\\ArcGISProjects\\Verona\\Multi_temporal_Speckle.gdb"
tables = arcpy.ListTables()
for fc in tables:
     fieldList = arcpy.ListFields(fc)
     new_name = fc
     new_name2 = fc
     for field in fieldList:
          if field.name == 'MEAN':
               arcpy.AlterField_management(fc, field.name, new_name2, new_name2)
               print(field.name, "cambiato in", new_name2)
          if field.name == new_name:
               arcpy.AlterField_management(fc, field.name, new_name2, new_name2)




workspace = arcpy.env.workspace = "D:\\ArcGISProjects\\Verona\\Multi_temporal_Speckle.gdb"
tables = arcpy.ListTables()
tables.sort()

for z in tables:
     arcpy.JoinField_management("D:\\ArcGISProjects\\Verona\\Multi_temporal_Speckle.gdb\\Uso_suolo_Multi_Speckle_VV", "Id", z, "Id", z)
     print("Done " + z)



arcpy.env.workspace="D:\\ArcGISProjects\\Verona\\Multi_temporal_Speckle.gdb"
# Process: Convert Table To CSV File
feature = arcpy.ListTables()
arcpy.TableToTable_conversion("D:\\ArcGISProjects\\Verona\\Multi_temporal_Speckle.gdb\\Uso_suolo_Multi_Speckle_VV", "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\database_VV" , "SpeckleMultiTimeSeriesVV.csv")

for file in dir(arcpy):
     if "table".lower() in file.lower():
          print(file)

for file in dir(arcpy):
     if "table".lower() in file.lower():
          print(file)