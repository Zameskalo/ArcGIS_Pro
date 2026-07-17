#CoordenadasTD = "CoordenadasTD_PQ15"
#VerticesTrayectorias = "TrayectoriasSE_Feature_Merge"

CoordenadasTD = arcpy.GetParameterAsText(0)
NamePZ_CoordsTD = arcpy.GetParameterAsText(1)
VerticesTrayectorias = arcpy.GetParameterAsText(2)
NamePZ_Vertices = arcpy.GetParameterAsText(3)


# Se eliminan los campos de trayectoria si existen en la capa de coordenadas TD
campos_trayectorias = ['A3116XSup','A3116YSup','A3116XAtr','A3116YAtr','A3116XTD','A3116YTD','B3117XSup','B3117YSup','B3117XAtr','B3117YAtr','B3117XTD','B3117YTD','CTM12XSup','CTM12YSup','CTM12XAtr','CTM12YAtr','CTM12XTD','CTM12YTD']
campos_capa = arcpy.ListFields(CoordenadasTD)
for campo in campos_capa:
    for campo_trayectoria in campos_trayectorias:
        if campo.name == campo_trayectoria:
            arcpy.management.DeleteField(CoordenadasTD,campo.name)

# Se agregan los campos de trayectoria a la capa de coordenadas TD
campos_trayectorias = ['A3116XSup','A3116YSup','A3116XAtr','A3116YAtr','A3116XTD','A3116YTD','B3117XSup','B3117YSup','B3117XAtr','B3117YAtr','B3117XTD','B3117YTD','CTM12XSup','CTM12YSup','CTM12XAtr','CTM12YAtr','CTM12XTD','CTM12YTD']
for nombre_campo in campos_trayectorias:
    arcpy.management.AddField(CoordenadasTD,nombre_campo,'DOUBLE')

descriptorCoordenadasTD = arcpy.Describe(CoordenadasTD)
CoordenadasTD_name = descriptorCoordenadasTD.name.split('.')[0]

# Se calculan los campos de trayectorias de acuerdo con la capa de vértices

#Coordenadas de superficie
arcpy.analysis.TableSelect(VerticesTrayectorias,"CoordenadasSuperficie","TipoCoord = '1Sup'")
arcpy.management.AddJoin(CoordenadasTD,NamePZ_CoordsTD,"CoordenadasSuperficie",NamePZ_Vertices)

arcpy.management.CalculateFields(
    in_table=CoordenadasTD,
    expression_type="PYTHON3",
    fields="{0}.A3116X{1} !{2}.x3116! #;{0}.A3116Y{1} !{2}.y3116! #;{0}.B3117X{1} !{2}.x3117! #;{0}.B3117Y{1} !{2}.y3117! #;{0}.CTM12X{1} !{2}.xCTM12! #;{0}.CTM12Y{1} !{2}.yCTM12! #".format(CoordenadasTD_name,'Sup','CoordenadasSuperficie'),
    code_block="",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.management.RemoveJoin(CoordenadasTD_name,"CoordenadasSuperficie")

#Coordenadas de aterrizaje
arcpy.analysis.TableSelect(VerticesTrayectorias,"CoordenadasAterrizaje","TipoCoord = '2Atr'")
arcpy.management.AddJoin(CoordenadasTD,NamePZ_CoordsTD,"CoordenadasAterrizaje",NamePZ_Vertices)
arcpy.management.CalculateFields(
    in_table=CoordenadasTD,
    expression_type="PYTHON3",
    fields="{0}.A3116X{1} !{2}.x3116! #;{0}.A3116Y{1} !{2}.y3116! #;{0}.B3117X{1} !{2}.x3117! #;{0}.B3117Y{1} !{2}.y3117! #;{0}.CTM12X{1} !{2}.xCTM12! #;{0}.CTM12Y{1} !{2}.yCTM12! #".format(CoordenadasTD_name,'Atr','CoordenadasAterrizaje'),
    code_block="",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.management.RemoveJoin(CoordenadasTD_name,"CoordenadasAterrizaje")

#Coordenadas de Fondo
arcpy.analysis.TableSelect(VerticesTrayectorias,"CoordenadasFondo","TipoCoord = '3TD'")
arcpy.management.AddJoin(CoordenadasTD,NamePZ_CoordsTD,"CoordenadasFondo",NamePZ_Vertices)
arcpy.management.CalculateFields(
    in_table=CoordenadasTD,
    expression_type="PYTHON3",
    fields="{0}.A3116X{1} !{2}.x3116! #;{0}.A3116Y{1} !{2}.y3116! #;{0}.B3117X{1} !{2}.x3117! #;{0}.B3117Y{1} !{2}.y3117! #;{0}.CTM12X{1} !{2}.xCTM12! #;{0}.CTM12Y{1} !{2}.yCTM12! #".format(CoordenadasTD_name,'TD','CoordenadasFondo'),
    code_block="",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
arcpy.management.RemoveJoin(CoordenadasTD_name,"CoordenadasFondo")