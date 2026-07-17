import arcpy

# arcpy.env.workspace = r'C:\o\OneDrive - SERINGTEC\zecl\PROYECTOS\Gral_SERINGTEC\GDB\DIR_test.gdb'
# destinationFolder = r'C:\o\OneDrive - SERINGTEC\zecl\PROYECTOS\Gral_SERINGTEC\SHP\DIR'

arcpy.env.workspace = arcpy.GetParameterAsText(0)
destinationFolder = arcpy.GetParameterAsText(1)

datasets = arcpy.ListDatasets()
for ds in datasets:
    arcpy.management.CreateFolder(destinationFolder, ds)
    featureclasses = arcpy.ListFeatureClasses(feature_dataset=ds)
    outputFolder = destinationFolder + '\\' + ds
    for fc in featureclasses:
        arcpy.conversion.FeatureClassToShapefile(fc, outputFolder)

print('Script Finalizado')
