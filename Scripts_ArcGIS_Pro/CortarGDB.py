import arcpy
import os

# Permitir sobrescritura de archivos
arcpy.env.overwriteOutput = True

# Parámetros de entrada
gdb_in = r"C:\O\OneDrive - SERINGTEC\zecl\PROYECTOS\temp\GDB\TempCarto.gdb"
gdb_out = r"C:\O\OneDrive - SERINGTEC\zecl\PROYECTOS\temp\GDB\CartoCutTest.gdb"
clip_feature = r"C:\O\OneDrive - SERINGTEC\zecl\PROYECTOS\temp\temp.gdb\AOI"

# Crear GDB de destino si no existe
if not arcpy.Exists(gdb_out):
    arcpy.CreateFileGDB_management(os.path.dirname(gdb_out), os.path.basename(gdb_out))

# --- COPIAR DOMINIOS ---
# Mantenemos esto al inicio para asegurar que la GDB de destino conozca todos los dominios
print("Copiando dominios entre Geodatabases...")
dominios_destino = [d.name for d in arcpy.da.ListDomains(gdb_out)]

for domain in arcpy.da.ListDomains(gdb_in):
    if domain.name not in dominios_destino:
        try:
            if domain.domainType == "CodedValue":
                temp_dom_table = os.path.join(gdb_out, "temp_dom_table")
                arcpy.management.DomainToTable(gdb_in, domain.name, temp_dom_table, "code", "description")
                arcpy.management.TableToDomain(temp_dom_table, "code", "description", gdb_out, domain.name, domain.description, "REPLACE")
                arcpy.management.Delete(temp_dom_table)
            
            elif domain.domainType == "Range":
                arcpy.management.CreateRangeDomain(gdb_out, domain.name, domain.description, domain.type, domain.range[0], domain.range[1])
                
        except Exception as e:
            print(f"No se pudo copiar el dominio {domain.name}: {e}")

print("Dominios copiados con éxito.\n")


# --- FUNCIÓN PARA PROCESAR FEATURE CLASSES ---
def procesar_feature_class(fc_origen, fc_destino):
    """
    Corta la capa directamente de GDB a GDB. 
    Esto conserva automáticamente Subtipos, Dominios asociados y Alias de campos.
    """
    try:
        # El Clip directo se encarga de crear el esquema idéntico y filtrar los datos en un solo paso
        arcpy.analysis.Clip(fc_origen, clip_feature, fc_destino)
        print(f"Capa {os.path.basename(fc_destino)} procesada con éxito (subtipos y dominios preservados).")
    except Exception as e:
        print(f"Error al procesar la capa {os.path.basename(fc_origen)}: {e}")


# --- PROCESAR FEATURE DATASETS ---
arcpy.env.workspace = gdb_in
datasets = arcpy.ListDatasets("", "Feature") or []

for ds in datasets:
    ds_in = os.path.join(gdb_in, ds)
    ds_out = os.path.join(gdb_out, ds)
    sr = arcpy.Describe(ds_in).spatialReference
    
    if not arcpy.Exists(ds_out):
        arcpy.management.CreateFeatureDataset(gdb_out, ds, sr)

    arcpy.env.workspace = ds_in
    for fc in arcpy.ListFeatureClasses() or []:
        fc_in = os.path.join(ds_in, fc)
        fc_out = os.path.join(ds_out, fc)
        procesar_feature_class(fc_in, fc_out)


# --- PROCESAR FEATURE CLASSES SUELTOS (EN LA RAÍZ) ---
arcpy.env.workspace = gdb_in
for fc in arcpy.ListFeatureClasses() or []:
    fc_in = os.path.join(gdb_in, fc)
    fc_out = os.path.join(gdb_out, fc)
    procesar_feature_class(fc_in, fc_out)

print("\n¡Proceso finalizado con éxito!")