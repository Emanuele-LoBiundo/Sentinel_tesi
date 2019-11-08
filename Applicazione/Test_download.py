from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from urllib.request import urlretrieve
import tkinter
import os
from PIL import Image, ImageTk
import io
import requests
import sys
import xml.etree.ElementTree as ET
import pandas as pd
import time
import urllib.request
import configparser


my_config_parser = configparser.ConfigParser()
my_config_parser.read('D:\Progetti_python\Applicazione Sentinel Download\myconfig.ini')



username = my_config_parser["DEFAULT"]['username']
password = my_config_parser["DEFAULT"]['password']
dataIniziale = my_config_parser["DEFAULT"]['dataIniziale']
dataFinale = my_config_parser["DEFAULT"]['dataFinale']
cloud = my_config_parser["DEFAULT"]['cloud']
percorso = my_config_parser["DEFAULT"]['percorso']
bande = my_config_parser["DEFAULT"]['bande']
bande = bande.split(',')



print("Benvenuto\nPrima di cominciare modifica i parametri di ricerca nel file 'myconfig.ini' che si trova all'interno della cartella dist/Applicazione_finale")

datframe_ut = input("Hai già un dataframe personalizzato premi qualsiasi tasto per ricercarne uno nuovo?[y,n]")

datf = input("Seleziona il percorso del tuo dataframe:  ")
df = pd.read_csv(datf, sep=';', index_col=0, header=0)
df = df.dropna(how='all')


password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, 'https://scihub.copernicus.eu/dhus', username, password)
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
opener.open("https://scihub.copernicus.eu/dhus")
urllib.request.install_opener(opener)

preview = df['link_icon'].tolist()
# Lista con gli id
id_product = df.index.tolist()

# lista con i nomi
name_product = df['title'].tolist()

date_Product = df['beginposition'].tolist()
type(time.strptime(date_Product[0][0:10], '%Y-%m-%d'))

# lista con le date
date_product = []
for i in range(len(name_product)):
    date_product.append(name_product[i][11:26])

# crea una lista con i link di accesso e le credenziali
link_list = []
for i in range(0, len(id_product)):
    link_list.append(
        'https://scihub.copernicus.eu/dhus/odata/v1/Products(%27' + id_product[i] + '%27)/Nodes(%27' + name_product[
            i] + '.SAFE%27)/Nodes(%27GRANULE%27)/Nodes')

v = []
for URL in preview:
    with urllib.request.urlopen(URL) as url:
        v.append(url.read())

current = 0


def move(delta):
    global current, v
    if not (0 <= current + delta < len(v)):
        print('End', 'No more image.')
        return
    current += delta
    photo = ImageTk.PhotoImage(Image.open(io.BytesIO(v[current])))
    label1['text'] = name_product[current]
    label1['image'] = photo
    label1.photo = photo


print("Adesso verrà visualizzata la preview delle", str(len(df)), "immagini.")
continuare3 = input("Vuoi vedere la preview?[y,n]: ")

if continuare3.lower() == "y":
    print("Continue processing...")
    root = tkinter.Tk()

    label1 = tkinter.Label(root, compound=tkinter.TOP)
    label1.pack(side=tkinter.TOP)

    frame = tkinter.Frame(root)
    frame.pack()

    tkinter.Button(frame, text='Previous picture', command=lambda: move(-1)).pack(side=tkinter.LEFT)
    tkinter.Button(frame, text='Next picture', command=lambda: move(+1)).pack(side=tkinter.LEFT)
    tkinter.Button(frame, text='Quit', command=root.destroy).pack(side=tkinter.LEFT)

    move(0)

    root.mainloop()
    print("Chiudere la finestra preview per procedere")
    continuare = input("Continuare con il download?[y,n]: ")

    if continuare.lower() == "y":
        print("Avvio processo di download....\nAttendere qualche istante...Generazione codici in corso...")
    else:
        sys.exit()
else:
    print("Avvio processo di download....\nAttendere qualche istante...Generazione codici in corso...")

codici = []
first_code = []
last_code = []
code_exception = []

for i in range(0, len(link_list)):
    url = link_list[i]
    r = requests.get(url, auth=(username, password))
    root = ET.fromstring(r.content)
    i += 1
    local_users = []
    for link in root.iter('{http://www.w3.org/2005/Atom}link'):
        local_users.append(link.attrib['href'])
    codici = []
    for e in local_users:
        for element in e.split():
            if element.endswith("e"):
                codici.append(element)
                for j in range(0, len(codici)):
                    first_code.append(codici[j][11:17])
                    last_code.append(codici[j][7:len(codici) - 10])
                    code_exception.append(codici[j][7:17])

# generazioni codici

link_band = []
for i in range(0, len(name_product)):
    for band in bande:
        if pd.Timestamp(date_Product[i]) < pd.Timestamp("2018-03-22"):
            link_band.append(
                'https://scihub.copernicus.eu/dhus/odata/v1/Products(%27' + id_product[i] + '%27)/Nodes(%27' +
                name_product[
                    i] + '.SAFE%27)/Nodes(%27GRANULE%27)/Nodes(\'' + last_code[
                    i] + '\')/Nodes(%27IMG_DATA%27)/Nodes(%27R' + band[4:7] + '%27)/Nodes(\'' + code_exception[
                    i] + '_' + date_product[
                    i] + '_' + band + '.jp2\')/$value')
        # immagini prima del 2018/04
        else:
            link_band.append(
                'https://scihub.copernicus.eu/dhus/odata/v1/Products(%27' + id_product[i] + '%27)/Nodes(%27' +
                name_product[
                    i] + '.SAFE%27)/Nodes(%27GRANULE%27)/Nodes(\'' + last_code[
                    i] + '\')/Nodes(%27IMG_DATA%27)/Nodes(%27R' + band[4:7] + '%27)/Nodes(\'' + first_code[
                    i] + '_' +
                date_product[
                    i] + '_' + band + '.jp2\')/$value')

print("Sono stati generati " + str(len(link_band)) + ' links')
myPath = input("Inserire il percorso della cartella dove verranno scaricati i file: ")


for url in link_band:
    # Split on the rightmost / and take everything on the right side of that
    name = "L2A" + url[-37:-9]



count = 0
for url in link_band:
    # Split on the rightmost / and take everything on the right side of that
    name = "L2A" + url[-37:-28] + 'D' + url[64:68] + url[-21:-9]

    # Combine the name and the downloads directory to get the local filename
    filename = os.path.join(myPath, name)

    # Download the file if it does not exist
    if not os.path.exists(filename):
        try:
            urlretrieve(url, filename)
            print(" %-15s %-10s %25s" % ('--', name, 'downloaded'))
            print(count, '/', len(link_band))
            count += 1
        except:
            print("url {} did not return a valid response".format(url))
    else:
        pass


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file



a = []
for file in files(myPath):
    a.append(file)

b = []
for url in link_band:
    text = "L2A" + url[-37:-9]
    b.append(text)


for i, j in zip(filename2,filename):
    if i != j:
        print(i)
    else:
        pass

for file in link_band:
    print(file)