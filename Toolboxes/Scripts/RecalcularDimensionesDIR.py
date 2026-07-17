import arcpy

# arcpy.env.workspace = r'C:\o\OneDrive - SERINGTEC\zecl\PROYECTOS\Gral_SERINGTEC\GDB\DIR_test.gdb'
# out_sr = ('Magna Colombia Este')

arcpy.env.workspace = arcpy.GetParameterAsText(0)
out_sr = arcpy.GetParameterAsText(1)

sr = arcpy.SpatialReference(text=out_sr)
sr_text = sr.exportToString()
print(sr_text)

datasets = arcpy.ListDatasets()
for ds in datasets:
    featureclasses = arcpy.ListFeatureClasses(feature_dataset=ds)
    for fc in featureclasses:
        fields = arcpy.ListFields(fc)
        desc = arcpy.Describe(fc)
        if desc.shapeType == 'Polygon':
            for field in fields:
                #print(fc,' ',field.name)
                if field.name == "AREA_HA":
                    arcpy.management.CalculateGeometryAttributes(
                    in_features=fc,
                    geometry_property="AREA_HA AREA",
                    length_unit="",
                    area_unit="HECTARES",
                    coordinate_system=sr_text,
                    coordinate_format="SAME_AS_INPUT"
                    )
                elif field.name == "AREA_M2":    
                    arcpy.management.CalculateGeometryAttributes(
                    in_features=fc,
                    geometry_property="AREA_M2 AREA",
                    length_unit="",
                    area_unit="SQUARE_METERS",
                    coordinate_system=sr_text,
                    coordinate_format="SAME_AS_INPUT"
                    )
        elif desc.shapeType == 'Polyline':
            for field in fields:
                #print(fc,' ',field.name)
                if field.name == "LONG_M":
                    arcpy.management.CalculateGeometryAttributes(
                    in_features=fc,
                    geometry_property="LONG_M LENGTH",
                    length_unit="METERS",
                    area_unit="",
                    coordinate_system=sr_text,
                    coordinate_format="SAME_AS_INPUT"
                    )

print('Script Finalizado')
