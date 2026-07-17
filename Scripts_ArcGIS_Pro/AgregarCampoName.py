import arcpy

aprx = arcpy.mp.ArcGISProject("CURRENT")
campo_agregar = 'Name'

# Funcion para verificar si las capas tienen el campo a agregar
def field_exists(feature_class, field_name):
    # Use a list comprehension for a robust case-insensitive check
    field_names = [field.name.lower() for field in arcpy.ListFields(feature_class)]
    if field_name.lower() in field_names:
        return True
    else:
        return False

# Crear listado con las capas del mapa actual
map_layer_list = []
for m in aprx.listMaps():
    for layer in m.listLayers():
        map_layer_list.append(layer.name)

# Agregar campo Name si la capa aún no lo tiene
for layer_name in map_layer_list:
    if field_exists(layer_name, campo_agregar):
        print(f"No se agregó ningún campo adicional en la capa '{layer_name}', porque la capa ya tiene el campo '{campo_agregar}' ")
    else:
        arcpy.AddField_management(layer_name, campo_agregar, "TEXT", field_length=150)
        print(f"Se agregó el campo '{campo_agregar}' en la capa '{layer_name}'")

print("Script Finalizado")