import arcpy
import os

gdb = r"C:\o\OneDrive - SERINGTEC\zecl\PROYECTOS\ECO027017\GDB\GDB_ECO_027_017.gdb"
arcpy.env.overwriteOutput = True

print("Analizando:", gdb)

# -------- Feature Classes en la raíz --------
arcpy.env.workspace = gdb

for fc in arcpy.ListFeatureClasses():
    if int(arcpy.GetCount_management(fc)[0]) == 0:
        print(f"Borrando FC vacía: {fc}")
        arcpy.Delete_management(fc)

# -------- Feature Classes dentro de datasets --------
datasets = arcpy.ListDatasets(feature_type='feature')

for ds in datasets:
    ds_path = os.path.join(gdb, ds)
    arcpy.env.workspace = ds_path

    for fc in arcpy.ListFeatureClasses():
        if int(arcpy.GetCount_management(fc)[0]) == 0:
            print(f"Borrando FC vacía: {ds}/{fc}")
            arcpy.Delete_management(fc)

# -------- Borrar datasets vacíos --------
arcpy.env.workspace = gdb

for ds in datasets:
    ds_path = os.path.join(gdb, ds)
    arcpy.env.workspace = ds_path

    if not arcpy.ListFeatureClasses():
        arcpy.env.workspace = gdb
        print(f"Borrando Dataset vacío: {ds}")
        arcpy.Delete_management(ds)

print("✅ Limpieza finalizada")