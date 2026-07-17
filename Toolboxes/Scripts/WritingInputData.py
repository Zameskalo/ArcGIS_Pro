import arcpy

capas = arcpy.GetParameterAsText(0)
out_sr = arcpy.GetParameterAsText(1)

sr = str(arcpy.SpatialReference(text=out_sr))

f = open("../txt/writing.txt", "w")
f.write("Content in the input is:\n")
f.write(capas)
f.write("\nOutput SR is:\n")
f.write(out_sr)
f.close()