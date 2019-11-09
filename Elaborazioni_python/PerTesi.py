import arcpy
from arcpy import env
import os

env.workspace = ""  # Cartella delle immagini da elaborare
rasters = arcpy.ListRasters()  # Crea una lista delle immagini all'interno della cartella
rasters.sort()  # Ordina le immagini all'interno della lista
destination_path = ""  # Cartella di destinazione
# Loop per ogni immagine
for k in rasters:
    outRaster = os.path.join(destination_path, k[:-4] + ".dbf")  # Nome della tabella in uscita
    z = arcpy.gp.ZonalStatisticsAsTable_sa("Feature", "Id", k, outRaster, "DATA", "MEAN")  # Comando statistica Zonale
    print(k + "_____done.")


workspace = arcpy.env.workspace = "" # Percorso del geodatabase
tables = arcpy.ListTables() # Crea una lista con le tabelle della statistica zonale.
#Loop per ogni tabella
for z in tables:
    try:
        arcpy.JoinField_management("Feature", "Id", z, "Id", z) #Comando di Join tra le feature e la tabella.
        print("Done " + z)
    except:
        print("Error " + z)
