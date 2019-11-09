import arcpy
from arcpy import env
from images2gif import writeGif
from PIL import Image

polygon = arcpy.SelectLayerByAttribute_management("D:\\ArcGISProjects\\Verona\\Backscatter.gdb\\Uso_suolo_backscatter_iw1_VH", "NEW_SELECTION", "Id = 57608")

env.workspace = "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\TimeLapse"

images = arcpy.ListRasters()



catalog = []
for image in images:
    catalog.append(arcpy.sa.ExtractByMask(image, polygon))

catalog_name = "D:\\Progetti_python\\Verona\\Sentinel1\\BACKSCATTER\\Multitemporal_spleckle\\TimeLapse\\Extract_D_201801.tif", "D:\\Progetti_python\\Verona\\Sentinel1\\BACKSCATTER\\Multitemporal_spleckle\\TimeLapse\\Extract_D_201802.tif", "D:\\Progetti_python\\Verona\\Sentinel1\\BACKSCATTER\\Multitemporal_spleckle\\TimeLapse\\Extract_D_201803.tif", "D:\\Progetti_python\\Verona\\Sentinel1\\BACKSCATTER\\Multitemporal_spleckle\\TimeLapse\\Extract_D_201804.tif", "D:\\Progetti_python\\Verona\\Sentinel1\\BACKSCATTER\\Multitemporal_spleckle\\TimeLapse\\Extract_D_201805.tif"
img = Image.open("D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\TimeLapse\D_20180105.tif")
import matplotlib.pyplot as plt
plt.imshow(img)


images = [Image.open(fn) for fn in catalog_name]

filename = "D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\TimeLapse\my_gif.GIF"
writeGif(filename, catalog, duration=0.2)


import imageio
images = []
for filename in catalog_name:
    images.append(imageio.imread(filename))
imageio.mimsave('D:\Progetti_python\Verona\Sentinel1\BACKSCATTER\Multitemporal_spleckle\TimeLapse\my_gif.GIF', images)

