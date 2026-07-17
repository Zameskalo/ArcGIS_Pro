import arcpy

#capas = "CoordenadasTD_Optimizacion;DistanciasOptimizacion;LocacionesOptimizacion" #I Guess
#out_sr = sr = arcpy.SpatialReference(3116)
#carpeta_salida = r'C:\zecl\RUBIALES\SHP\Optimizacion\Test_20240823'

capas = arcpy.GetParameterAsText(0)
sr_code = arcpy.GetParameterAsText(1)
carpeta_salida = arcpy.GetParameterAsText(2)

splittedCapas = capas.split(';')
out_sr = arcpy.SpatialReference(int(sr_code))

for capa in splittedCapas:
    capaDesc = arcpy.Describe(capa)
    nombreCapa = capaDesc.basename
    capaSalida = carpeta_salida + '\\' + nombreCapa + '_' + sr_code
    arcpy.management.Project(capa,capaSalida,out_sr)