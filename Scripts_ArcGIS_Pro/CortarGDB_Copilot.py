# -*- coding: utf-8 -*-
import arcpy
import os

# ==================================================
# PARÁMETROS
# ==================================================

gdb_origen = r"C:\O\OneDrive - SERINGTEC\zecl\PROYECTOS\temp\GDB\Carto100000_Colombia_DI_2022.gdb"

gdb_destino = r"C:\O\OneDrive - SERINGTEC\zecl\PROYECTOS\temp\GDB\Carto100k.gdb"

poligono_corte = r"C:\O\OneDrive - SERINGTEC\zecl\PROYECTOS\temp\temp.gdb\AOI"

xml_temp = r"C:\O\OneDrive - SERINGTEC\zecl\PROYECTOS\temp\SchemaTemp.xml"

# ==================================================
# CONFIGURACIÓN
# ==================================================

arcpy.env.overwriteOutput = True

# ==================================================
# CREAR GDB DESTINO
# ==================================================

if not arcpy.Exists(gdb_destino):

    carpeta = os.path.dirname(gdb_destino)
    nombre_gdb = os.path.basename(gdb_destino)

    arcpy.management.CreateFileGDB(
        carpeta,
        nombre_gdb
    )

# ==================================================
# EXPORTAR ESQUEMA COMPLETO
# ==================================================

print("Exportando esquema de la GDB origen...")

arcpy.management.ExportXMLWorkspaceDocument(
    in_data=gdb_origen,
    out_file=xml_temp,
    export_type="SCHEMA_ONLY",
    storage_type="BINARY"
)

# ==================================================
# IMPORTAR ESQUEMA
# ==================================================

print("Importando esquema en GDB destino...")

arcpy.management.ImportXMLWorkspaceDocument(
    target_geodatabase=gdb_destino,
    in_file=xml_temp,
    import_type="SCHEMA_ONLY"
)

# ==================================================
# VACIAR TABLAS Y FEATURE CLASSES
# (por seguridad)
# ==================================================

print("Limpiando datasets...")

arcpy.env.workspace = gdb_destino

# FC en raíz
for fc in arcpy.ListFeatureClasses():
    arcpy.management.DeleteRows(fc)

# Tablas
for tabla in arcpy.ListTables():
    arcpy.management.DeleteRows(tabla)

# Feature datasets
for fds in arcpy.ListDatasets("", "Feature"):

    arcpy.env.workspace = os.path.join(gdb_destino, fds)

    for fc in arcpy.ListFeatureClasses():
        arcpy.management.DeleteRows(fc)

# ==================================================
# RECORTE DE FEATURE CLASSES
# ==================================================

print("Iniciando proceso de recorte...")

arcpy.env.workspace = gdb_origen

datasets = arcpy.ListDatasets("", "Feature")

if datasets is None:
    datasets = []

datasets.insert(0, "")

for dataset in datasets:

    if dataset == "":
        workspace_actual = gdb_origen
    else:
        workspace_actual = os.path.join(
            gdb_origen,
            dataset
        )

    arcpy.env.workspace = workspace_actual

    fc_list = arcpy.ListFeatureClasses()

    if not fc_list:
        continue

    for fc in fc_list:

        try:

            print(f"Procesando {fc}")

            if dataset == "":

                fc_origen = os.path.join(
                    gdb_origen,
                    fc
                )

                fc_destino = os.path.join(
                    gdb_destino,
                    fc
                )

            else:

                fc_origen = os.path.join(
                    gdb_origen,
                    dataset,
                    fc
                )

                fc_destino = os.path.join(
                    gdb_destino,
                    dataset,
                    fc
                )

            temp_clip = rf"memory\clip_{fc}"

            if arcpy.Exists(temp_clip):
                arcpy.management.Delete(temp_clip)

            # -----------------------------------
            # CLIP
            # -----------------------------------

            arcpy.analysis.Clip(
                fc_origen,
                poligono_corte,
                temp_clip
            )

            # -----------------------------------
            # APPEND
            # -----------------------------------

            resultado = int(
                arcpy.management.GetCount(
                    temp_clip
                )[0]
            )

            if resultado > 0:

                arcpy.management.Append(
                    temp_clip,
                    fc_destino,
                    "NO_TEST"
                )

            arcpy.management.Delete(temp_clip)

            print(f"  Registros cargados: {resultado}")

        except Exception as e:

            print(
                f"ERROR en {fc}: {str(e)}"
            )

# ==================================================
# ELIMINAR XML TEMPORAL
# ==================================================

if os.path.exists(xml_temp):
    os.remove(xml_temp)

print("\nProceso finalizado correctamente.")