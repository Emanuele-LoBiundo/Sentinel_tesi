import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter



Coerenza_VH = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\TutteDateSentinel1\Coerenza\VH_Sentinel1_Coerenza.csv", sep=";", index_col="Id", decimal=",")
Coerenza_VV = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\TutteDateSentinel1\Coerenza\VV_Sentinel1_Coerenza.csv", sep=";", index_col="Id", decimal=",")
Ndvi = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\FiltroDate\Sentinel2.csv", sep=";", index_col="Id", decimal=",")
BackscatterVH = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\FiltroDate\BackscatterVH.csv", sep=";", index_col="Id", decimal=",")
BackscatterVV = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\FiltroDate\BackscatterVV.csv", sep=";", index_col="Id", decimal=",")
BackscatterVHsmooth = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\FiltroDate\Smooth\BackscatterVHsmooth30Ok.csv", sep=";", index_col="Id", decimal=",")
meteoDat = pd.read_csv("D:\Progetti_python\Verona\stazioni_meteo\Rilievi_con_date_backscatter_daApr_Sett.csv", sep=";", index_col="ID", decimal=",")
meteo = pd.read_csv("D:\Progetti_python\Verona\stazioni_meteo\Rilievi_tutte_date_daApr_mag.csv", sep=";", index_col="ID", decimal=",")
meteoJoin = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\Prati\Join_particelle_stazioni.csv", sep=";", index_col="Id", decimal=",")

NdviNoNorm = Ndvi.drop("DE_VARIETA", axis=1)

#############################NORMALIZZAZIONE############################################
def normalizzazione(table):
    table = table.drop("DE_VARIETA", axis=1)
    table = table.transpose()
    table = (table - table.min()) / (table.max() - table.min())
    table = table.transpose()
    return table
NormCohVH = normalizzazione(Coerenza_VH)
NormCohVV = normalizzazione(Coerenza_VV)
NormBackVH = normalizzazione(BackscatterVH)
NormBackVV = normalizzazione(BackscatterVV)
NormBackVHsmooth = normalizzazione(BackscatterVHsmooth)
NormNdvi = normalizzazione(Ndvi)


#############################SELEZIONA DATA############################################
#inputVal = input("Inserisci id.......     ")
inputVal = 20066
inputValMeteo = int(meteoJoin.loc[["S" + str(inputVal)]].values[0])
def select_row(table):
    a = list(table.index.values)
    try:
        if type(a[0]) == str:
            table = table.loc[["S" + str(inputVal)]].values
        else:
            table = table.loc[[inputVal]].values
    except:
        table = table.loc[[inputValMeteo]].values
    table = table[0]
    return table

rowCohVH = select_row(NormCohVH)
rowCohVV = select_row(NormCohVV)
rowBackVH = select_row(NormBackVH)
rowBackVV = select_row(NormBackVV)
rowBackVHsmooth = select_row(NormBackVHsmooth)
rowNdvi = select_row(NormNdvi)
rowMeteo = select_row(meteo)
rowNdviNoNorm = select_row(NdviNoNorm)
rowfiltroCohVH = select_row(filtroCohVH)


##################################################Asse_X#################################
x_asse = list(Coerenza_VH.columns.values)
x_asse = [datetime.datetime.strptime(item[2:10], "%Y%m%d") for item in x_asse[1:len(x_asse)]]
x_asse_ndvi = list(Ndvi.columns.values)
x_asse_ndvi = [datetime.datetime.strptime(item[1:10], "%Y%m%d") for item in x_asse_ndvi[1:len(x_asse_ndvi)]]
x_asse_meteo = list(meteo.columns.values)
x_asse_meteo = [datetime.datetime.strptime(item, "%Y%m%d") for item in x_asse_meteo[0:len(x_asse_meteo)]]
#x_asse_meteo = [datetime.datetime.strptime(item, "%d/%m/%Y") for item in x_asse_meteo]



##################################################FILTRO PIOGGIA#################################

def filtro_pioggia(table, meteoJoinTable, meteoTable):
    table = table.join(meteoJoinTable, how = "left" )
    for i in meteoTable.index.values:
        for j in range(0, len(meteoTable) - 1):
            if meteoTable.loc[[i], [meteoTable.columns.values[j]]].values > 0.25:
                table.loc[table["Id_stazion"] == i, [table.columns.values[j]]] = None
    table = table.drop("Id_stazion", axis=1)
    return table

filtroCohVH = filtro_pioggia(NormCohVH, meteoJoin, meteoDat)


##################################################PLOT#################################

fig = plt.figure(figsize=(16, 8))
fig.suptitle('Id: ' + str(inputVal), ha="left",x = 0.03, fontsize=12)


ax = fig.add_subplot(3,1, 1)
ax.plot(x_asse_ndvi, rowNdvi, 'o', color="red", label= "Ndvi")
ax.plot(x_asse,rowCohVH, 'g-o', color= "green", label= "CohVH")
ax.plot(x_asse,rowCohVV, 'g-o', color= "blue", label="CohVV")

ax.plot(x_asse,rowfiltroCohVH, 'g-o', color= "red", label="VHNoPioggia")

ax.legend(bbox_to_anchor=(1.04, 0.8), loc='upper left', borderaxespad=0.)
ax.grid(which='major', linestyle='-.', linewidth='0.2', color='black')
ax.set_title("Coherence")
ax4 = ax.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.bar(x_asse_meteo, rowMeteo, color=color, width=0.2, label="Meteo")
ax.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax.set_xlim([datetime.date(2018, 4, 1), datetime.date(2018, 10, 1)])
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)



ax1 = fig.add_subplot(3 ,1, 2)
ax1.plot(x_asse_ndvi, rowNdvi, 'o', color="red", label= "Ndvi")
ax1.plot(x_asse,rowBackVH, 'g-o', color= "green", label= "BackVH")
ax1.plot(x_asse,rowBackVHsmooth, 'g-o', color= "purple", label= "BackVHsmooth")
ax1.plot(x_asse,rowBackVV, 'g-o', color= "blue", label= "BackVV")
ax1.grid(which='major', linestyle='-.', linewidth='0.2', color='black')
ax3 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax3.bar(x_asse_meteo, rowMeteo, color=color, width=0.2, label="Meteo")
ax3.tick_params(axis='y', labelcolor=color)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax1.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax1.xaxis_date()
ax1.legend(bbox_to_anchor=(1.04, 0.7), loc='upper left', borderaxespad=0.)
ax1.set_xlim([datetime.date(2018, 4, 1), datetime.date(2018, 10, 1)])
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
ax1.set_title("Basckscatter")


ax2 = fig.add_subplot(3 ,1, 3)
ax2.plot(x_asse_ndvi, rowNdviNoNorm, 'o', color="red", label= "Ndvi")
ax2.grid(which='major', linestyle='-.', linewidth='0.2', color='black')
ax2.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax2.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax2.xaxis_date()
ax2.set_title("Ndvi")
ax2.legend(bbox_to_anchor=(1.04, 0.6), loc='upper left', borderaxespad=0.)
ax2.set_xlim([datetime.date(2018, 4, 1), datetime.date(2018, 10, 1)])
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
plt.subplots_adjust(hspace=0.5)
fig.tight_layout()
plt.show()




