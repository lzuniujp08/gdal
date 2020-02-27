from osgeo import gdal
import osgeo.ogr as ogr
import osgeo.osr as osr
import csv

# 为了支持中文路径，请添加下面这句代码
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
# 为了使属性表字段支持中文，请添加下面这句
# gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
# set up the shapefile driver
driver = ogr.GetDriverByName("ESRI Shapefile")

rootDir = r'D:\data\nc'
shpPath = rootDir + '\\tem.shp'

# create the data source
data_source = driver.CreateDataSource(shpPath)

# create the spatial reference, WGS84
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# create the layer
layer = data_source.CreateLayer("tem", srs, ogr.wkbPoint)

# Add the fields we're interested in
field_name = ogr.FieldDefn("name", ogr.OFTString)
field_name.SetWidth(24)
layer.CreateField(field_name)
layer.CreateField(ogr.FieldDefn("lon", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("lat", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("tem_max", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("tem_min", ogr.OFTReal))

# use a dictionary reader so we can access by field name
csvPath = 'D:\\lzugis20\\code\\python-demo\\data\\tem.txt'
with open(csvPath, newline='', encoding='UTF-8') as csvfile:
  rows = csv.DictReader(csvfile)
  for row in rows:
    # create the feature
    feature = ogr.Feature(layer.GetLayerDefn())
    # Set the attributes using the values from the delimited text file
    feature.SetField("name", row['name'])
    feature.SetField("lon", row['lon'])
    feature.SetField("lat", row['lat'])
    feature.SetField("tem_max", row['tem_max'])
    feature.SetField("tem_min", row['tem_min'])

    # create the WKT for the feature using Python string formatting
    wkt = "POINT(%f %f)" % (float(row['lon']), float(row['lat']))

    # Create the point from the Well Known Txt
    point = ogr.CreateGeometryFromWkt(wkt)

    # Set the feature geometry using the point
    feature.SetGeometry(point)

    # Create the feature in the layer (shapefile)
    layer.CreateFeature(feature)

    # Dereference the feature
    feature = None

  # Save and close the data source
data_source = None
print('shp create success')
