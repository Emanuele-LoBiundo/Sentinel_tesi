import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


Ndvi = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\DatabaseOriginali\Sentinel2\InterpolatiUltimo.csv", sep=";", index_col="Id", decimal=",")
Centroidi = pd.read_csv("D:\Progetti_python\Verona\ProgettoFinale\TutteDateSentinel1\Centroidi_Ndvi.csv", sep=";", index_col="Id", decimal=",")


tableNdvi = Ndvi.drop("DE_VARIETA", axis=1)


inputVal = 14016
def select_row(table):
    a = list(table.index.values)
    try:
        if type(a[0]) == str:
            table = table.loc[["S" + str(inputVal)]].values[0]
        else:
            table = table.loc[[inputVal]].values[0]
    except:
        table = table.loc[[inputValMeteo]].values[0]
    return table


rowNdvi = select_row(tableNdvi)
rowNdvi2 = select_row(tableNdvi)
rowCentroidi = Centroidi.loc[[130]].values[0]

x_asse = list(tableNdvi.columns.values)
x_asse = [datetime.datetime.strptime(item[0:10], "D%Y%m%d") for item in x_asse[0:len(x_asse)]]
x_asseCen = list(Centroidi.columns.values)
x_asseCen = [datetime.datetime.strptime(item[0:10], "%d/%m/%Y") for item in x_asseCen[0:len(x_asseCen)]]


fig= plt.figure(figsize=(16, 4))
ax = fig.add_subplot()
plt.ylabel('Ndvi', fontsize=10)
ax.plot(x_asse, rowNdvi , 'g', color= "black", label= "Id: 41016")
ax.plot(x_asseCen, rowCentroidi, 'g', color= "blue", label= "Centroide 130")
ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')
ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left', borderaxespad=0.)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax.set_xlim([datetime.date(2018, 4, 8), datetime.date(2018, 9, 26)])
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)

plt.subplots_adjust(hspace=0.1, wspace=0.5)
fig.tight_layout(h_pad= 0.7, w_pad= 0.7)
plt.show()

