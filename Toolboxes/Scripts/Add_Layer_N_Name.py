# -*- coding: utf-8 -*-
import arcpy

# Parámetros de entrada
input_layer = arcpy.GetParameterAsText(0)  # Capa de entrada
source_field = arcpy.GetParameterAsText(1) # Campo seleccionado

# Nombres de los campos a crear
name_field = "Name"
layer_field = "Layer"

# Obtener campos existentes
existing_fields = [f.name for f in arcpy.ListFields(input_layer)]

# Agregar campo Name si no existe
if name_field not in existing_fields:
    arcpy.AddField_management(
        in_table=input_layer,
        field_name=name_field,
        field_type="TEXT",
        field_length=255
    )

# Agregar campo Layer si no existe
if layer_field not in existing_fields:
    arcpy.AddField_management(
        in_table=input_layer,
        field_name=layer_field,
        field_type="TEXT",
        field_length=255
    )

# Expresión para copiar el valor del campo seleccionado
expression = f"!{source_field}!"

# Calcular campo Name
arcpy.CalculateField_management(
    in_table=input_layer,
    field=name_field,
    expression=expression,
    expression_type="PYTHON3"
)

# Calcular campo Layer
arcpy.CalculateField_management(
    in_table=input_layer,
    field=layer_field,
    expression=expression,
    expression_type="PYTHON3"
)

arcpy.AddMessage("Campos Name y Layer creados y calculados correctamente.")