import arcpy
import os

# Parámetros de entrada
gdb_in = r"D:\CURSO_ARCGIS_PRO\INSUMOS_CURSO\Servicio-205\Test_to_cut.gdb"       # GDB original
gdb_out = r"D:\CURSO_ARCGIS_PRO\INSUMOS_CURSO\Servicio-205\Carto100k_test.gdb"       # GDB destino
clip_feature = r"D:\CURSO_ARCGIS_PRO\CURSO_ARCGIS_PRO\CURSO_ARCGIS_PRO.gdb\AOI"    # Polígono para cortar

# Crear GDB de salida si no existe
if not arcpy.Exists(gdb_out):
    arcpy.CreateFileGDB_management(os.path.dirname(gdb_out),
                                   os.path.basename(gdb_out))

# --- CORREGIDO: Copiar todos los dominios de gdb_in a gdb_out ---
print("Copiando dominios entre Geodatabases...")
domains = arcpy.da.ListDomains(gdb_in)
for domain in domains:
    # Solo procesamos si el dominio no existe ya en la de destino
    if domain.name not in [d.name for d in arcpy.da.ListDomains(gdb_out)]:
        try:
            # Ruta temporal para exportar el dominio
            temp_dom_table = "memory/temp_dom_table"
            
            # Exportar dominio de origen a tabla en memoria
            arcpy.management.DomainToTable(gdb_in, domain.name, temp_dom_table, 
                                           "code", "description")
            
            # Importar tabla en memoria como dominio en GDB de destino
            arcpy.management.TableToDomain(temp_dom_table, "code", "description", 
                                           gdb_out, domain.name, domain.description, 
                                           "REPLACE")
            
            # Línea corregida: Usamos arcpy.Delete_management directamente
            arcpy.Delete_management(temp_dom_table)
            
        except Exception as e:
            print(f"No se pudo copiar el dominio {domain.name}: {e}")
print("Dominios copiados con éxito.\n")

# -------------------------------------------------------------

arcpy.env.workspace = gdb_in
datasets = arcpy.ListDatasets("", "Feature")

for ds in datasets:
    ds_in = os.path.join(gdb_in, ds)
    sr = arcpy.Describe(ds_in).spatialReference
    ds_out = os.path.join(gdb_out, ds)
    if not arcpy.Exists(ds_out):
        arcpy.CreateFeatureDataset_management(gdb_out, ds, sr)

    arcpy.env.workspace = ds_in
    feature_classes = arcpy.ListFeatureClasses()

    for fc in feature_classes:
        fc_in = os.path.join(ds_in, fc)
        fc_out = os.path.join(ds_out, fc)

        # Crear feature class con mismo esquema
        desc = arcpy.Describe(fc_in)
        arcpy.CreateFeatureclass_management(ds_out, fc,
                                            geometry_type=desc.shapeType,
                                            spatial_reference=desc.spatialReference)

        # Copiar campos
        fields = [f for f in arcpy.ListFields(fc_in) if f.type not in ("OID", "Geometry")]
        for f in fields:
            arcpy.AddField_management(fc_out, f.name, f.type,
                                      f.precision, f.scale, f.length,
                                      f.aliasName, f.isNullable, f.required)

        # Copiar dominios (Ahora sí funcionará porque ya existen en gdb_out)
        for f in fields:
            if f.domain:
                arcpy.AssignDomainToField_management(fc_out, f.name, f.domain)

        # Cortar datos y añadirlos
        temp_clip = "memory/temp_clip" # Cambiado 'in_memory' a 'memory' (más moderno y rápido en Pro)
        arcpy.Clip_analysis(fc_in, clip_feature, temp_clip)
        arcpy.Append_management(temp_clip, fc_out, "NO_TEST")
        arcpy.Delete_management(temp_clip)

        print(f"Capa {fc} cortada y exportada con dominios en {fc_out}")