import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter



Coerenza_VH = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\DatabaseOriginali\Coerenza\VH_Sentinel1_Coerenza.csv", sep=";", index_col="Id", decimal=",")
Coerenza_VV = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\DatabaseOriginali\Coerenza\VV_Sentinel1_Coerenza.csv", sep=";", index_col="Id", decimal=",")
Ndvi = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\DatabaseOriginali\Sentinel2\InterpolatiUltimo.csv", sep=";", index_col="Id", decimal=",")
BackscatterVH = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\DatabaseOriginali\Backscatter\SpeckleMultiTimeSeriesVH_originali.csv", sep=";", index_col="Id", decimal=",")
BackscatterVV = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\DatabaseOriginali\Backscatter\SpeckleMultiTimeSeriesVV_originali.csv", sep=";", index_col="Id", decimal=",")
BackscatterVH_2 = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\DatabaseOriginali\Backscatter\Smooth\BackscatterVHcomplete30.csv", sep=";", index_col="Id", decimal=",")
BackscatterVV_2 = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\DatabaseOriginali\Backscatter\Smooth\BackscatterVVcomplete30_2.csv", sep=";", index_col="Id", decimal=",")



#############################SELEZIONA DATA############################################
inputVal = 72950
def seleziona_rigaNorm(table):
    table = table.drop("DE_VARIETA", axis=1)
    a = list(table.index.values)
    try:
        if type(a[0]) == str:
            table = table.loc[["S" + str(inputVal)]].values
            table = table[0]
            table = (table - table.min()) / (table.max() - table.min())
        else:
            table = table.loc[[inputVal]].values
            table = table[0]
            table = (table - table.min()) / (table.max() - table.min())
    except:
        table = table.loc[[inputValMeteo]].values
        table = table[0]
        table = (table - table.min()) / (table.max() - table.min())
    return table




rowCohVH = seleziona_rigaNorm(Coerenza_VH)
rowCohVV = seleziona_rigaNorm(Coerenza_VV)

rowBackVH = seleziona_rigaNorm(BackscatterVH)
rowBackVV = seleziona_rigaNorm(BackscatterVV)

rowBackVH_2 = seleziona_rigaNorm(BackscatterVH_2)
rowBackVV_2 = seleziona_rigaNorm(BackscatterVV_2)

Ndvi2 = Ndvi.drop("DE_VARIETA", axis=1)
rowNdvi = Ndvi2.loc[["S" + str(inputVal)]].values[0]


##################################################Asse_X#################################
x_asse = list(BackscatterVH.columns.values)
x_asse = [datetime.datetime.strptime(item, "%d/%m/%Y") for item in x_asse[1:len(x_asse)]]

x_asse_ndvi = list(Ndvi.columns.values)
x_asse_ndvi = [datetime.datetime.strptime(item, "D%Y%m%d") for item in x_asse_ndvi[1:len(x_asse_ndvi)]]

x_asse_coh = list(Coerenza_VH.columns.values)
x_asse_coh = [datetime.datetime.strptime(item, "%d/%m/%Y") for item in x_asse_coh[1:len(x_asse_coh)]]
#x_asse_meteo = [datetime.datetime.strptime(item, "%d/%m/%Y") for item in x_asse_meteo]

##################################################PLOT#################################

fig = plt.figure(figsize=(16, 8))
fig.suptitle('Id: ' + str(inputVal), ha="left", x = 0.03, y = 1, fontsize=12)

ax = fig.add_subplot(3,1, 1)
ax.plot(x_asse_ndvi, rowNdvi, '-', color="red", label= "Ndvi")
ax.legend(bbox_to_anchor=(1.02, 0.8), loc='upper left', borderaxespad=0.)
ax.grid(which='major', linestyle='-', linewidth='0.1', color='black')
plt.ylabel('Ndvi', fontsize=10)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax.set_xlim([datetime.date(2018, 1, 1), datetime.date(2018, 12, 31)])
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
plt.subplots_adjust(wspace=0.5)


ax1 = fig.add_subplot(3 ,1, 2)
ax1.plot(x_asse,rowBackVH, 'g-o', color= "green", label= "Backscatter VH")
ax1.plot(x_asse,rowBackVV, 'g-o', color= "blue", label= "Backscatter VH")
ax1.grid(which='major', linestyle='-', linewidth='0.1', color='black')
color = 'tab:blue'
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax1.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax1.xaxis_date()
ax1.legend(bbox_to_anchor=(1.02, 0.7), loc='upper left', borderaxespad=0.)
ax1.set_xlim([datetime.date(2018, 1, 1), datetime.date(2018, 12, 31)])
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
plt.ylabel('Backscatter [dB]', fontsize=10)


ax2 = fig.add_subplot(3 ,1, 3)
ax2.plot(x_asse_coh,rowCohVH, 'g-o', color= "green", label= "Coerenza VH")
ax2.plot(x_asse_coh,rowCohVV, 'g-o', color= "blue", label= "Coerenza VV")
ax2.grid(which='major', linestyle='-', linewidth='0.1', color='black')
ax2.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax2.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax2.xaxis_date()
plt.ylabel('Coerenza', fontsize=10)
ax2.legend(bbox_to_anchor=(1.02, 0.6), loc='upper left', borderaxespad=0.)
ax2.set_xlim([datetime.date(2018, 1, 1), datetime.date(2018, 12, 31)])
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
plt.subplots_adjust(hspace=0.5)
fig.tight_layout()
plt.show()




