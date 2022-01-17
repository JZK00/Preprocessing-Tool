# -*- coding: utf-8 -*-
import pydicom
import pylab

ds = pydicom.read_file("E:/DATA/datasets/none/1.dcm")

##查看有哪些属性
print(ds.dir("pat"))

##查看对应属性的具体值
print ds.PatientName

##将属性值给某个元素
data_element = ds.data_element("PatientsName")  # or data_element = ds[0x10,0x10]
print data_element.VR, data_element.value

##删除属性
# del ds.SoftwareVersions

##原始二进制文件
pixel_bytes = ds.PixelData

##CT值组成了一个矩阵
pix = ds.pixel_array

##读取显示图片
pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
pylab.show()

##修改图片中的元素，不能直接使用data_array,需要转换成PixelData
for n, val in enumerate(ds.pixel_array.flat):  # example: zero anything < 300
    if val < 300:
        ds.pixel_array.flat[n] = 0
ds.PixelData = ds.pixel_array.tostring()
ds.save_as("E:/DATA/datasets/none/2.dcm")
