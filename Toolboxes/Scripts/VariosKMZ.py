import arcpy

#capas = "Centroides_PQ15";"CoordenadasTD_PQ15";"TrayectoriasSERINGTEC_PQ15";"Locaciones_PQ15"
#carpeta_salida = r'C:\zecl\RUBIALES\Entregas\2024\20240822_Paquete15\KMZ'

capas = arcpy.GetParameterAsText(0)
carpeta_salida = arcpy.GetParameterAsText(1)

splittedCapas = capas.split(';')

for capa in splittedCapas:
    KMZsalida = carpeta_salida + '\\' + capa + '.kmz'
    arcpy.conversion.LayerToKML(capa,KMZsalida)