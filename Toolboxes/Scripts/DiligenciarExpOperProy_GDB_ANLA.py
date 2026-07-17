import arcpy

# arcpy.env.workspace = r'C:\o\OneDrive - SERINGTEC\zecl\PROYECTOS\ECO027017\GDB\GDB_ECO_027_017.gdb'
# expediente = ""
# operador = ""
# proyecto = 'ESTUDIOS Y DISEÑOS PARA EL MEJORAMIENTO DE LA INFRAESTRUCTURA VIAL Y REDES DE ALCANTARILLADO PLUVIAL EN EL CASCO URBANO DEL MUNICIPIO DE VALLE DEL GUAMUEZ, PUTUMAYO'

arcpy.env.workspace = arcpy.GetParameterAsText(0)
expediente = arcpy.GetParameterAsText(1)
operador = arcpy.GetParameterAsText(2)
proyecto = arcpy.GetParameterAsText(3)

datasets = arcpy.ListDatasets()
for ds in datasets:
    featureclasses = arcpy.ListFeatureClasses(feature_dataset=ds)
    for fc in featureclasses:
        fields = arcpy.ListFields(fc)
        for field in fields:
            if field.name == 'EXPEDIENTE':
                arcpy.management.CalculateField(fc, field.name, "'{}'".format(expediente),"PYTHON3")
            elif field.name == 'OPERADOR':
                arcpy.management.CalculateField(fc, field.name, "'{}'".format(operador),"PYTHON3")
            elif field.name == 'PROYECTO':
                arcpy.management.CalculateField(fc, field.name, "'{}'".format(proyecto),"PYTHON3")

print('Script Finalizado')
