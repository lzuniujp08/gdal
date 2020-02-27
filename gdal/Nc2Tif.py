import numpy as np
from netCDF4 import Dataset
from osgeo import gdal, osr

# 1. 路径处理和变量定义
rootDir = r'/Users/lzugis/Documents/ncdata'
ncPath = rootDir + '/china_gdfs.nc'
tifPath = '../out/china_gdfs_tem.tif'

ncDataset = Dataset(ncPath)
lat = ncDataset.variables['lat'][:]
lon = ncDataset.variables['lon'][:]
tem = ncDataset.variables['TEM'][:, :]
#  处理异常值
tem = np.asarray(tem)
tem[np.where(tem == 1.e+30)] = -99

lonMin, latMax, lonMax, latMin = [lon.min(), lat.max(), lon.max(), lat.min()]

# 2. 影像的分辨率，此处float(N_lon)-1是为了保证分辨率为0.5 degree，不知是否合理，望指正
nLat = len(lat)
nLon = len(lon)
lonRes = (lonMax - lonMin) / (float(nLon) - 1)
latRes = (latMax - latMin) / (float(nLat) - 1)

# 3. 构建.tiff文件框架
temDataset = gdal.GetDriverByName('Gtiff').Create(tifPath, nLon, nLat, 1, gdal.GDT_Float32)

# 4. 设置影像的显示范围
geoTransform = (lonMin, lonRes, 0, latMin, 0, latRes)
temDataset.SetGeoTransform(geoTransform)

# 5. 地理坐标系统信息
srs = osr.SpatialReference()  # 获取地理坐标系统信息，用于选取需要的地理坐标系统
srs.ImportFromEPSG(4326)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
temDataset.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息

# 6. 数据写出
temDataset.GetRasterBand(1).WriteArray(tem)  # 将数据写入内存，此时没有写入硬盘
temDataset.FlushCache()  # 将数据写入硬盘
temDataset = None  # 关闭temDataset指针，注意必须关闭

print('Finished')
