import arcpy
import os

# 1. Configuración del entorno de trabajo
arcpy.env.overwriteOutput = True
workspace = r"C:\O\OneDrive - SERINGTEC\zecl\PROYECTOS\RUBIALES\GDB\Rubiales_Default.gdb"
arcpy.env.workspace = workspace

# 2. Definición de las capas de entrada
epoca_1 = "ZonManAmbRub_20260113"  # Enero 2026
epoca_2 = "ZonManAmbRub_20260410"  # Abril 2026

# === PARÁMETROS DE FILTRADO INDEPENDIENTES ===
campo_exclusion_e1 = "NOMENCLAT"
valor_exclusion_e1 = "Exclusión"

campo_exclusion_e2 = "NOMENCLAT"
valor_exclusion_e2 = "Exclusión"

# 3. UNICA Ruta de salida definitiva
salida_final = os.path.join(workspace, "Cambio_ZonasExclusion")

# Rutas temporales en memoria para el procesamiento operativo
layer_epoca1 = "lyr_epoca1_filtrada"
layer_epoca2 = "lyr_epoca2_filtrada"
temp_interseccion = "memory\\temp_interseccion"
temp_diferencia = "memory\\temp_diferencia"

try:
    print("Iniciando filtrado independiente por capas...")
    
    # Construcción de cláusulas WHERE
    where_e1 = f"{campo_exclusion_e1} = '{valor_exclusion_e1}'" if isinstance(valor_exclusion_e1, str) else f"{campo_exclusion_e1} = {valor_exclusion_e1}"
    where_e2 = f"{campo_exclusion_e2} = '{valor_exclusion_e2}'" if isinstance(valor_exclusion_e2, str) else f"{campo_exclusion_e2} = {valor_exclusion_e2}"
    
    # Capas en memoria con el filtro aplicado
    arcpy.management.MakeFeatureLayer(epoca_1, layer_epoca1, where_e1)
    arcpy.management.MakeFeatureLayer(epoca_2, layer_epoca2, where_e2)

    print("\nProcesando análisis geoespacial unificado...")

    # A. Obtener las zonas que PERSISTEN (Intersección)
    print("-> Analizando Persistencias...")
    arcpy.analysis.Intersect([layer_epoca1, layer_epoca2], temp_interseccion, "ONLY_FID")
    arcpy.management.AddField(temp_interseccion, "Tipo_Cambio", "TEXT", field_length=20)
    arcpy.management.CalculateField(temp_interseccion, "Tipo_Cambio", "'Persistencia'", "PYTHON3")

    # B. Obtener los cambios (Nuevas y Eliminadas) usando Diferencia Simétrica
    print("-> Analizando Nuevas y Eliminadas...")
    arcpy.analysis.SymDiff(layer_epoca1, layer_epoca2, temp_diferencia, "ALL")
    
    # Añadir el campo clasificador a la diferencia simétrica
    arcpy.management.AddField(temp_diferencia, "Tipo_Cambio", "TEXT", field_length=20)
    
    # Separar cuáles son nuevas y cuáles eliminadas usando los FID heredados
    # En ArcGIS, SymDiff hereda el FID original. Si FID_Capa1 es -1, significa que el polígono pertenece SOLO a la Capa 2 (Nueva).
    fid_e1 = f"FID_{os.path.basename(epoca_1)}"
    
    code_block = f"""
def clasificar(fid_previo):
    if fid_previo == -1 or fid_previo is None:
        return 'Nueva'
    else:
        return 'Eliminada'
"""
    arcpy.management.CalculateField(
        in_table=temp_diferencia,
        field="Tipo_Cambio",
        expression=f"clasificar(!{fid_e1}!)",
        expression_type="PYTHON3",
        code_block=code_block
    )

    # C. Unir todo en la capa de salida final única
    print("\nFusionando resultados en una sola capa...")
    arcpy.management.Merge([temp_interseccion, temp_diferencia], salida_final)

    # D. Calcular áreas y generar reporte final en la consola
    arcpy.management.CalculateGeometryAttributes(
        in_features=salida_final,
        geometry_property=[["Area_Ha", "AREA"]],
        area_unit="HECTARES"
    )

    print("\n--- REPORTES DE SUPERFICIE (CAPA UNIFICADA) ---")
    reporte = {"Persistencia": 0.0, "Nueva": 0.0, "Eliminada": 0.0}
    with arcpy.da.SearchCursor(salida_final, ["Tipo_Cambio", "Area_Ha"]) as cursor:
        for row in cursor:
            if row[0] in reporte and row[1]:
                reporte[row[0]] += row[1]
                
    for clave, valor in reporte.items():
        print(f"-> {clave}: {round(valor, 2)} Hectáreas.")

    # Limpieza de elementos volátiles en memoria
    arcpy.management.Delete(layer_epoca1)
    arcpy.management.Delete(layer_epoca2)
    arcpy.management.Delete(temp_interseccion)
    arcpy.management.Delete(temp_diferencia)
    
    print(f"\n¡Proceso completado! Capa única generada en: {salida_final}")

except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")