import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter



Coerenza_VH = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\Prati\Prati_Coerenza_VH.csv", sep=";", index_col="Id", decimal=",")
Coerenza_VV = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\Prati\Prati_Coerenza_VV.csv", sep=";", index_col="Id", decimal=",")
Coerenza_VH_VV = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\Prati\Prati_Coerenza_VH_VV.csv", sep=";", index_col="Id", decimal=",")
Ndvi = pd.read_csv("D:\Progetti_python\Verona\Sentinel_2\Database_corretto\Prati\Prati.csv", sep=";", index_col="Id", decimal=",")
BackscatterVH = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\Prati\Prati_Backscatter_VH.csv", sep=";", index_col="Id", decimal=",")
BackscatterVV = pd.read_csv("D:\Progetti_python\Verona\Sentinel1\Databases_tutti\Prati\Prati_Backscatter_VV.csv", sep=";", index_col="Id", decimal=",")
meteo = pd.read_csv("D:\Progetti_python\Verona\stazioni_meteo\Rilievi_tutte_date_daApr_mag.csv", sep=";", index_col="ID", decimal=",")

rowCohVHProva = Coerenza_VH[0:10].drop("DE_VARIETA" , axis=1)
myarrayCohVHProva = np.asarray(rowCohVHProva.squeeze()).astype(float)
normedCohVHProva = (myarrayCohVHProva-myarrayCohVHProva.min())/(myarrayCohVHProva.max()-myarrayCohVHProva.min())




x_asse = list(Coerenza_VH.columns.values)
x_asse = x_asse[1:len(Coerenza_VH)]
x_asse = [datetime.datetime.strptime(item[2:10], "%Y%m%d") for item in x_asse]

x_asse_ndvi = list(Ndvi.columns.values)
x_asse_ndvi = x_asse_ndvi[1:len(x_asse_ndvi)]
x_asse_ndvi = [datetime.datetime.strptime(item[1:10], "%Y%m%d") for item in x_asse_ndvi]

x_asse_meteo = list(meteo.columns.values)
x_asse_meteo = [datetime.datetime.strptime(item, "%Y%m%d") for item in x_asse_meteo]


inputVal = input("Inserisci id.......     ")
inputValMeteo = input("Inserisci id stazione meteorologica.......     ")


rowMeteo = meteo.loc[[int(inputValMeteo)]]
myarrayMeteo = np.asarray(rowMeteo.squeeze()).astype(float)

rowCohVH = Coerenza_VH.loc[["S" + inputVal]].drop("DE_VARIETA" , axis=1)
rowCohVV = Coerenza_VV.loc[["S" + inputVal]].drop("DE_VARIETA" , axis=1)
rowCohVH_VV = Coerenza_VH_VV.loc[["S" + inputVal]].drop("DE_VARIETA" , axis=1)
rowBackVH = BackscatterVH.loc[["S" + inputVal]].drop("DE_VARIETA" , axis=1)
rowBackVV = BackscatterVV.loc[["S" + inputVal]].drop("DE_VARIETA" , axis=1)
rowNdvi = Ndvi.loc[["S" + inputVal]].drop("DE_VARIETA" , axis=1)

myarrayCohVH = np.asarray(rowCohVH.squeeze()).astype(float)
normedCohVH = (myarrayCohVH-myarrayCohVH.min())/(myarrayCohVH.max()-myarrayCohVH.min())
myarrayCohVV = np.asarray(rowCohVV.squeeze()).astype(float)
normedCohVV = (myarrayCohVV-myarrayCohVV.min())/(myarrayCohVV.max()-myarrayCohVV.min())
myarrayCohVH_VV = np.asarray(rowCohVH_VV.squeeze()).astype(float)
normedCohVH_VV = (myarrayCohVH_VV-myarrayCohVH_VV.min())/(myarrayCohVH_VV.max()-myarrayCohVH_VV.min())
myarrayNdvi = np.asarray(rowNdvi.squeeze()).astype(float)
normedNdvi = (myarrayNdvi-myarrayNdvi.min())/(myarrayNdvi.max()-myarrayNdvi.min())
myarrayBackscatterVH = np.asarray(rowBackVH.squeeze()).astype(float)
normedBackVH = (myarrayBackscatterVH-myarrayBackscatterVH.min())/(myarrayBackscatterVH.max()-myarrayBackscatterVH.min())
myarrayBackscatterVV = np.asarray(rowBackVV.squeeze()).astype(float)
normedBackVV = (myarrayBackscatterVV-myarrayBackscatterVV.min())/(myarrayBackscatterVV.max()-myarrayBackscatterVV.min())




# first we'll do it the default way, with gaps on weekends


# first we'll do it the default way, with gaps on weekends
fig = plt.figure(figsize=(16, 8))

ax = fig.add_subplot(3,1, 1)
ax.plot(x_asse_ndvi, normedNdvi, 'o', color="red", label= "Ndvi")
ax.plot(x_asse,normedCohVH, 'g-o', color= "green", label= "CohVH")
ax.plot(x_asse,normedCohVV, 'g-o', color= "blue", label="CohVV")
ax.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
ax.grid(which='major', linestyle='-.', linewidth='0.2', color='black')
ax.set_title("Coherence")
ax4 = ax.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax4.bar(x_asse_meteo, myarrayMeteo, color=color, width=0.2, label="Meteo")
ax.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax.set_xlim([datetime.date(2018, 4, 1), datetime.date(2018, 10, 1)])
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)



ax1 = fig.add_subplot(3 ,1, 2)
ax1.plot(x_asse_ndvi, normedNdvi, 'o', color="red", label= "Ndvi")
ax1.plot(x_asse,normedBackVH, 'g-o', color= "green", label= "BackVH")
ax1.plot(x_asse,normedBackVV, 'g-o', color= "blue", label= "BackVV")
ax1.grid(which='major', linestyle='-.', linewidth='0.2', color='black')
ax3 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax3.bar(x_asse_meteo, myarrayMeteo, color=color, width=0.2, label="Meteo")
ax3.tick_params(axis='y', labelcolor=color)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax1.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax1.xaxis_date()
ax1.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
ax1.set_xlim([datetime.date(2018, 4, 1), datetime.date(2018, 10, 1)])
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=90)
ax1.set_title("Basckscatter")


ax2 = fig.add_subplot(3 ,1, 3)
ax2.plot(x_asse_ndvi, myarrayNdvi, 'o', color="red", label= "Ndvi")

ax2.grid(which='major', linestyle='-.', linewidth='0.2', color='black')
ax2.xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax2.xaxis.set_major_formatter(DateFormatter('%d-%b'))
ax2.xaxis_date()
ax2.set_title("Ndvi")
ax2.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
ax2.set_xlim([datetime.date(2018, 4, 1), datetime.date(2018, 10, 1)])
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
plt.subplots_adjust(hspace=0.5)
fig.tight_layout()
plt.show()
