import arcpy

aprx = arcpy.mp.ArcGISProject("CURRENT")
map_layer_list = []
for m in aprx.listMaps():
    for layer in m.listLayers():
        map_layer_list.append(layer.name)

# Imprimir la lista de nombres de capas
for layer_name in map_layer_list:
    print(layer_name)

print(len(map_layer_list), ' capas')