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

api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')
time.sleep(1)
print("Credenziali corrette \nBenvenuto " + username)
time.sleep(1)


footprint = geojson_to_wkt(read_geojson(percorso))


products = api.query(footprint,
                     platformname = 'Sentinel-1',
                     date = (dataIniziale, dataFinale),
                     producttype='SLC',
                     orbitdirection='ASCENDING'
                     )

df = api.to_dataframe(products)
df = df.sort_values('beginposition')