import arcpy

arcpy.env.overwriteOutput = True

capaPuntos = "Cluster_FeatureToPoint1"

# Agregando campos

arcpy.management.AddFields(
    in_table=capaPuntos,
    field_description="X_3116 DOUBLE # # # #;Y_3116 DOUBLE # # # #;X_CTM12 DOUBLE # # # #;Y_CTM12 DOUBLE # # # #;LON_GMS TEXT # # # #;LAT_GMS TEXT # # # #",
    template=None
)

# MAGNA-SIRGAS Origen Bogotá

arcpy.management.CalculateGeometryAttributes(
    in_features=capaPuntos,
    geometry_property="X_3116 POINT_X",
    length_unit="",
    area_unit="",
    coordinate_system='PROJCS["MAGNA_Colombia_Bogota",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",1000000.0],PARAMETER["False_Northing",1000000.0],PARAMETER["Central_Meridian",-74.07750791666666],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",4.596200416666666],UNIT["Meter",1.0]]',
    coordinate_format="SAME_AS_INPUT"
)

arcpy.management.CalculateGeometryAttributes(
    in_features=capaPuntos,
    geometry_property="Y_3116 POINT_Y",
    length_unit="",
    area_unit="",
    coordinate_system='PROJCS["MAGNA_Colombia_Bogota",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",1000000.0],PARAMETER["False_Northing",1000000.0],PARAMETER["Central_Meridian",-74.07750791666666],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",4.596200416666666],UNIT["Meter",1.0]]',
    coordinate_format="SAME_AS_INPUT"
)

# MAGNA-SIRGAS Origen Único

arcpy.management.CalculateGeometryAttributes(
    in_features=capaPuntos,
    geometry_property="X_CTM12 POINT_X",
    length_unit="",
    area_unit="",
    coordinate_system='PROJCS["MAGNA-SIRGAS_CMT12",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',
    coordinate_format="SAME_AS_INPUT"
)

arcpy.management.CalculateGeometryAttributes(
    in_features=capaPuntos,
    geometry_property="Y_CTM12 POINT_Y",
    length_unit="",
    area_unit="",
    coordinate_system='PROJCS["MAGNA-SIRGAS_CMT12",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]]',
    coordinate_format="SAME_AS_INPUT"
)

# WGS84 Grados Minutos y Segundos

arcpy.management.CalculateGeometryAttributes(
    in_features=capaPuntos,
    geometry_property="LON_GMS POINT_X",
    length_unit="",
    area_unit="",
    coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
    coordinate_format="DMS_DIR_LAST"
)

arcpy.management.CalculateGeometryAttributes(
    in_features=capaPuntos,
    geometry_property="LAT_GMS POINT_Y",
    length_unit="",
    area_unit="",
    coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
    coordinate_format="DMS_DIR_LAST"
)

# Script Finalizado