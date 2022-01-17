import numpy
import pydicom
import os

# dicom文件所在的文件夹目录
PathDicom = 'E:/DATA/datasets/dicom/'

# 筛选出文件夹目录下所有的dicom文件
lstFilesDCM = []
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if '.dcm' in filename.lower():
            lstFilesDCM.append(os.path.join(dirName, filename))

# Get ref file
RefDs = pydicom.read_file(lstFilesDCM[0])
Pixel Spacing = Row Spacing\Column Spacing = 0.30 mm\0.25 mm

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

# save info.txt
info = ConstPixelDims + ConstPixelSpacing
f = open('E:/DATA/datasets/info.txt', 'w')
for n in info:
    f.write(str(n) + ' ')
f.close()

# According to location sorting
location = []
for i in range(len(lstFilesDCM)):
    ds = pydicom.read_file(lstFilesDCM[i])
    location.append(ds.SliceLocation)
location.sort()

# The array is sized based on 'ConstPixelDims'
ArrayDicom = numpy.zeros((len(lstFilesDCM), RefDs.Rows, RefDs.Columns), dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
    # read the file
    ds = pydicom.read_file(filenameDCM)
    # store the raw image data
    ArrayDicom[location.index(ds.SliceLocation), :, :] = ds.pixel_array

# save raw
ds = ArrayDicom.tostring()
f = open('/home/lk/testdata/1.3.6.1.4.1.9328.50.1.42697596859477567872763647333745089432/1.raw', 'wb')
f.write(ds)
f.close()
