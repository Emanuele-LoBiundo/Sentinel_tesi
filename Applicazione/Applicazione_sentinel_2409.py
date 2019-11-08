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


datframe_ut = input("Hai già un dataframe personalizzato? Premi qualsiasi tasto per ricercarne uno nuovo[y,n]")

if datframe_ut.lower() == "y":
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


    print("Sono state individuate ", str(len(df)), "immagini.")
    continuare3 = input("Vuoi vedere la preview delle immagini?[y,n]: ")

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
                count += 1
                print(count, '/', len(link_band))
            except:
                print("url {} did not return a valid response".format(url))
        else:
            pass

    sys.exit()

else:
    pass





start_point = input("Hai inserito i parametri?[y,n]")

if start_point.lower() == "y":
    print("Hai inserito:")
    print("Prima data per la ricerca:",dataIniziale)
    print("Seconda data per la ricerca:", dataFinale)
    print("Massima copertura nuvolosa", cloud + "%" )
    print("Sto ricercando le immagini")
else:
    sys.exit()

api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')
time.sleep(1)
print("Credenziali corrette \nBenvenuto " + username)
time.sleep(1)


footprint = geojson_to_wkt(read_geojson(percorso))


products = api.query(footprint,
                     platformname = 'Sentinel-2',
                     date = (dataIniziale, dataFinale),
                     cloudcoverpercentage=(0, cloud))

df = api.to_dataframe(products)
df = df.sort_values('beginposition')
df_information = df['title'].tolist()

#CALCOLO VALORI UNIVOCI PER IL FILTRO
#LISTA CODICI CON "TILE" ETC
prova_cod = []
for title in df_information:
    prova_cod.append(title[-27:-16])

tileS = []
for tile in df_information:
    tileS.append(tile[-22:-16])
tileS = list(set(tileS))

orbit_number = []
for title in df_information:
    orbit_number.append(title[-27:-23])
orbit_number = list(set(orbit_number))


print("Sono state trovate " + str(len(df)) + " immagini")

print("Tra le immagini trovate ci sono:\n" , str(len(tileS)), "TILE: ", tileS, "\n" , str(len(orbit_number)), "ORBITE RELATIVE: ", orbit_number)

time.sleep(1)


salvare_dat_pr = input("Salvare il database completo con " + str(len(df)) + " record?[y,n]: ")

time.sleep(1)

if salvare_dat_pr.lower()== "y":
    folder_dat_principale = input("Inserire il percorso dove salvare il file: ")
    name_fold_principale =  input("Inserire il nome del file: ")
    df.to_csv(folder_dat_principale + "\\" + name_fold_principale + ".csv", sep=';')
    time.sleep(1)
    print("Il file è stato creato nel percorso " + folder_dat_principale + "\\" + name_fold_principale + ".csv")
    time.sleep(1)
    print("Continue process filtering...")
else:
    time.sleep(1)
    print("Continue process filtering...")
    time.sleep(1)


#CALCOLO DEL VALORE UNIVOCO
a = list(set(prova_cod))
v = []
for s in a:
    v.append(next((x for x in df_information if s in x), None))

#DATAFRAME CON LE RIGHE UNIVOCHE FILTRATE
filtered = df[df['title'].isin(v)]

password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, 'https://scihub.copernicus.eu/dhus',username, password)
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
opener.open("https://scihub.copernicus.eu/dhus")
urllib.request.install_opener(opener)

#PRIMO PREVIEW
preview_primo = filtered["link_icon"].tolist()
nuova_lista_senza_eccezzioni = []
lista_preview = []
for URL in preview_primo:
    try:
        with urllib.request.urlopen(URL) as url:
            lista_preview.append(url.read())
        nuova_lista_senza_eccezzioni.append(URL)
    except:
        print("E' stato riscontrato un problema con " + df.loc[df['link_icon'] == URL, 'title'].iloc[0])
        pass

filtered = df[df['link_icon'].isin(nuova_lista_senza_eccezzioni)]
names_first_preview = filtered['title'].tolist()

lista_preview_def = []
for URL in nuova_lista_senza_eccezzioni:
    with urllib.request.urlopen(URL) as url:
        lista_preview_def.append(url.read())



current = 0

def move(delta):
    global current, nuova_lista_senza_eccezzioni
    if not (0 <= current + delta < len(nuova_lista_senza_eccezzioni)):
        print('End', 'No more image.')
        return
    current += delta
    photo = ImageTk.PhotoImage(Image.open(io.BytesIO(lista_preview_def[current])))
    label1['text'] = names_first_preview[current]
    label1['image'] = photo
    label1.photo = photo


print("Adesso verrà visualizzata la preview per la scelta del Livello del prodotto (es.MSIL2A), del tile (T****) e dell'orbita relativa (R****)\nControlla il nome sotto ogni immagine e appunta i valori ")

continuare3 = input("Vuoi vedere la preview?[y,n]: ")
print("Premere Quit per terminare")

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
    continuare = input("Continuare con il filtro del Livello del prodotto , del tile e dell'orbita relativa ?[y,n]: ")
else:
    continuare = input("Continuare con il filtro del Livello del prodotto, del tile e dell'orbita relativa ?[y,n]: ")

if continuare.lower() == "y":
    print("Continue processing...")
    # SCELTA DEL LIVELLO DEL PRODOTTO
    level_product = ['MSIL2A', 'MSIL1C']
    print("Scelta filtro del livello del prodotto!")
    print("Seleziona: ")
    for f, m in zip(level_product, range(0, len(level_product))):
        print(str(m), "per", f)
    print("Premere qualsiasi cosa per saltare il filtro livello")
    filtro_livello = input("")

    if filtro_livello.isdigit() & int(filtro_livello) < len(level_product):
        df = df[df['title'].str.contains(level_product[int(filtro_livello)])]
    else:
        pass

    print("Adesso le immagini sono: ", str(len(df)))

    # SCELTA DEL TILE
    print("Scelta del Tile!")
    print("Seleziona: ")
    for f, m in zip(tileS, range(0, len(tileS))):
        print(str(m), "per", f)
    print("Premere qualsiasi cosa per saltare il filtro del Tile")

    filtro_tile = input("Inserisci il numero corrispondente al Tile: ")

    if filtro_tile.isdigit() & int(filtro_tile) < len(tileS):
        df = df[df['title'].str.contains(tileS[int(filtro_tile)])]
    else:
        pass

    print("Adesso le immagini sono: ", str(len(df)))

    # SCELTA ORBITA RELATIVA
    print("Scelta dell' orbita relativa!")
    print("Seleziona: ")
    for f, m in zip(orbit_number, range(0, len(orbit_number))):
        print(str(m), "per", f)
    print("Premere qualsiasi cosa per saltare il filtro dell'orbita relativa")
    filtro_orbit = input("Inserisci il numero corrispondente all'orbita relativa: ")
    if filtro_orbit.isdigit() & int(filtro_orbit) < len(orbit_number):
        df = df[df['title'].str.contains(orbit_number[int(filtro_orbit)])]
    else:
        pass

    df = df.sort_values('beginposition')
else:
    pass


print("Le immagini filtrate sono " + str(len(df)))
time.sleep(1)
salvare_dat_sec = input("Salvare il database filtrato con " + str(len(df)) + " record?[y,n]: ")
if salvare_dat_sec.lower()== "y":
    folder_dat_principale = input("Inserire il percorso dove salvare il file: ")
    name_fold_principale =  input("Inserire il nome del file: ")
    df.to_csv(folder_dat_principale + "\\" + name_fold_principale + ".csv", sep=';')
    print("Il file è stato creato nel percorso " + folder_dat_principale + "\\" + name_fold_principale + ".csv")
    time.sleep(1)
    print("Continue process...")
else:
    time.sleep(1)
    print("Continue process...")




preview = df['link_icon'].tolist()
#Lista con gli id
id_product = df.index.tolist()

#lista con i nomi
name_product= df['title'].tolist()

date_Product = df['beginposition'].tolist()
type(time.strptime(date_Product[0][0:10], '%Y-%m-%d'))

#lista con le date
date_product = []
for i in range(len(name_product)):
    date_product.append(name_product[i][11:26])

#crea una lista con i link di accesso e le credenziali
link_list = []
for i in range (0,len(id_product)):
    link_list.append('https://scihub.copernicus.eu/dhus/odata/v1/Products(%27'+id_product[i]+'%27)/Nodes(%27'+name_product[i]+'.SAFE%27)/Nodes(%27GRANULE%27)/Nodes')


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
             'https://scihub.copernicus.eu/dhus/odata/v1/Products(%27' + id_product[i] + '%27)/Nodes(%27' + name_product[
                    i] + '.SAFE%27)/Nodes(%27GRANULE%27)/Nodes(\'' + last_code[
                    i] + '\')/Nodes(%27IMG_DATA%27)/Nodes(%27R'+ band[4:7] +'%27)/Nodes(\'' + code_exception[i] + '_' + date_product[
                    i] + '_'+ band + '.jp2\')/$value')
        #immagini prima del 2018/04
        else:
            link_band.append(
                'https://scihub.copernicus.eu/dhus/odata/v1/Products(%27' + id_product[i] + '%27)/Nodes(%27' + name_product[
                    i] + '.SAFE%27)/Nodes(%27GRANULE%27)/Nodes(\'' + last_code[
                    i] + '\')/Nodes(%27IMG_DATA%27)/Nodes(%27R'+ band[4:7] +'%27)/Nodes(\'' + first_code[i] + '_' + date_product[
                    i] + '_'+ band + '.jp2\')/$value')






myPath = input("Inserire il percorso della cartella dove verranno scaricati i file: ")




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
        except:
            print("url {} did not return a valid response".format(url))
    else:
        pass

