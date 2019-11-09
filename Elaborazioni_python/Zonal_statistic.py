
#STatistica zonale
import arcpy
from arcpy import env
import os
env.workspace = "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\ImmaginiBackScatter\MergeIw1Iw2\VH"
rasters = arcpy.ListRasters()


destination_path= "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\ImmaginiBackScatter\MergeIw1Iw2\Statistica_zonale\VH"
for k in rasters:
     outRaster = os.path.join(destination_path, "D_"+ k[0:11] + ".dbf")
     z = arcpy.gp.ZonalStatisticsAsTable_sa("D:\\ArcGISProjects\\Verona\\Backscatter.gdb\\Uso_suolo_backscatter_iw1_VH", "Id", k,  outRaster, "DATA", "MEAN")
     print(str(k[0:8]), "_____done.")

arcpy.env.workspace = "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\ImmaginiBackScatter\MergeIw1Iw2\Statistica_zonale\VH"
outLocation = "D:\ArcGISProjects\Verona\Backscatter.gdb"
tablesmove = arcpy.ListTables()

for table in tablesmove:
     if "D_2018" in table:
          arcpy.TableToGeodatabase_conversion(table, outLocation)
     else:
          print(table)

#Cambia nomi
arcpy.env.workspace = "D:\\ArcGISProjects\\Verona\\Backscatter.gdb"
tables = arcpy.ListTables()
for fc in tables:
     if "D_2018" in fc:
          fieldList = arcpy.ListFields(fc)
          new_name = fc
          new_name2 = fc
          for field in fieldList:
               if field.name == 'MEAN':
                    arcpy.AlterField_management(fc, field.name, new_name2, new_name2)
                    print(field.name, "cambiato in", new_name2)
               if field.name == new_name:
                    arcpy.AlterField_management(fc, field.name, new_name2, new_name2)




workspace = arcpy.env.workspace = "D:\\ArcGISProjects\\Verona\\Backscatter.gdb"
tables = arcpy.ListTables()
for z in tables:
    if "D_2018" in z:
        try:
            arcpy.JoinField_management('Uso_suolo_backscatter_iw1_VH', "Id", z, "Id", z)
            print("Done " + z)
        except:
            print("Error " + z)
    else:
        print(z + " is not NDVI table")
        pass

arcpy.env.workspace="D:\\ArcGISProjects\\Verona\\Backscatter.gdb"
# Process: Convert Table To CSV File
feature = arcpy.ListTables()
arcpy.TableToTable("Uso_suolo_backscatter_iw1_VH", "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\TimeSeriesBackscatter","TimeSeriesVH")