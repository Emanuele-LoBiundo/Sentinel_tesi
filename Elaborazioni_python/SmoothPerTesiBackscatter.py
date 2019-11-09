import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter



BackscatterVH = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\SpeckleMultiTimeSeriesVH_originali.csv", sep=";", index_col="Id", decimal=",")
BackscatterVV = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\SpeckleMultiTimeSeriesVV_originali.csv", sep=";", index_col="Id", decimal=",")
SmoothVH = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\TutteDate\BackscatterVHcomplete30.csv", sep=";", index_col="Id", decimal=",")
SmoothVV = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\TutteDate\BackscatterVVcomplete30.csv", sep=";", index_col="Id", decimal=",")
meteo = pd.read_csv("D:\Progetti_python\Verona\stazioni_meteo\Rilievisenzaprimedate.csv", sep=";", index_col="ID", decimal=",")
meteoJoin = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\Prati\Join_particelle_stazioni.csv", sep=";", index_col="Id", decimal=",")



tableVH = BackscatterVH.drop("DE_VARIETA", axis=1)
tableVV = BackscatterVV.drop("DE_VARIETA", axis=1)

tableSVH = SmoothVH.drop("DE_VARIETA", axis=1)
tableSVV = SmoothVV.drop("DE_VARIETA", axis=1)

#############################SELEZIONA DATA############################################
#inputVal = input("Inserisci id.......     ")
inputVal = 4303
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


rowBackVH = select_row(tableVH)
rowBackVV = select_row(tableVV)

rowBackSVH = select_row(tableSVH)
rowBackSVV = select_row(tableSVV)

rowMeteo = select_row(meteo)


##################################################Asse_X#################################
x_asse = list(tableVH.columns.values)
x_asse = [datetime.datetime.strptime(item[0:10], "%d/%m/%Y") for item in x_asse[0:len(x_asse)]]
x_asse_meteo = list(meteo.columns.values)
x_asse_meteo = [datetime.datetime.strptime(item, "%Y%m%d") for item in x_asse_meteo[0:len(x_asse_meteo)]]
#x_asse_meteo = [datetime.datetime.strptime(item, "%d/%m/%Y") for item in x_asse_meteo]


##################################################PLOT#################################

fig = plt.figure(figsize=(16, 8))
fig.suptitle('Id: ' + str(inputVal), ha="left", x = 0.03, y = 1, fontsize=12)

ax = fig.add_subplot(2,1,1)
plt.ylabel('Backscatter VH [dB]', fontsize=10)
ax.plot(x_asse, rowBackVH , 'g-o', color= "black", label= "BackscatterVH")
ax.plot(x_asse, rowBackSVH , 'g-o', color= "blue", label= "BackscatterVH")
ax.grid(which='major', linestyle='-.', linewidth='0.1', color='black')
ax4 = ax.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
plt.ylabel('Precipitazioni [mm]', fontsize=10)
ax4.bar(x_asse_meteo, rowMeteo, color=color, width=0.6, label="Meteo")
ax.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax.set_xlim([datetime.date(2018, 1, 5), datetime.date(2018, 12, 31)])
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)


ax1 = fig.add_subplot(2 ,1, 2)
ax1.plot(x_asse,rowBackVV, 'g-o', color= "black", label= "Backscatter")
ax1.plot(x_asse,rowBackSVV, 'g-o', color= "blue", label= "Smooth")

ax1.grid(which='major', linestyle='-.', linewidth='0.1', color='black')
plt.ylabel('Backscatter VV [dB]', fontsize=10)
ax3 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax3.bar(x_asse_meteo, rowMeteo, color=color, width=0.6, label="Meteo")
ax3.tick_params(axis='y', labelcolor="black")
plt.ylabel('Precipitazioni [mm]', fontsize=10)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax1.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax1.xaxis_date()
ax1.legend(bbox_to_anchor=(1.04, 1), loc='upper left', borderaxespad=0.)
ax3.legend(bbox_to_anchor=(1.04, 0.85), loc='upper left', borderaxespad=0.)
ax1.set_xlim([datetime.date(2018, 1, 5), datetime.date(2018, 12, 31)])
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)

plt.subplots_adjust(hspace=0.1, wspace=0.5)
fig.tight_layout(h_pad= 0.7, w_pad= 0.7)
plt.show()




