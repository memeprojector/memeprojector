"""
Trying to project a sample image to a sample projection using EPSG. 

https://stackoverflow.com/questions/18960229/how-to-project-a-flat-image-to-spherical-mercator-epgs900013-to-use-in-a-image

gdal_translate -a_srs EPSG:4326 -gcp 0 0 -89.38939600 30.39282800 -gcp 1024 0 -87.00029400 30.01043900 -gcp 0 1250 -89.99424800 27.37030800 -gcp 1024 1250 -87.67748400 26.98606100 "originalImage.tif" "image_trans.tiff"
gdalwarp -dstalpha -t_srs EPSG:4326 image_trans.tiff image_warped.tiff
"""
from osgeo import gdal

GCPs = [gdal.GCPs()]
to = gdal.TranslateOptions(GCPs=GCPs)
gdal.Translate(destDS, srcDS, to)