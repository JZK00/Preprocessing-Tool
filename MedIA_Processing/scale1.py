# -*- coding: utf-8 -*-
import os
import cv2


# 遍历指定目录，显示目录下的所有文件名
def CropImage4File(filepath, destpath):
    pathDir = os.listdir(filepath)  # list all the path or file  in filepath
    for allDir in pathDir:
        child = os.path.join(filepath, allDir)
        dest = os.path.join(destpath, allDir)
        if os.path.isfile(child):
            image = cv2.imread(child)
            sp = image.shape#obtain the image shape
            sz1 = sp[0]#height(rows) of image
            sz2 = sp[1]#width(colums) of image
            #sz3 = sp[2]#the pixels value is made up of three primary colors, here we do not use
            #你想对文件的操作
            print(sp)
            a=int(sz1/2-270) # x start
            b=int(sz1/2+301) # x end
            c=int(sz2/2-393) # y start
            d=int(sz2/2+178) # y end
            cropImg = image[a:b,c:d] #crop the image
            cv2.imwrite(dest,cropImg)# write in destination path


if __name__ == '__main__':
    filepath = 'E:/train/scale/train/' # source images
    destpath = 'E:/train/scale/new/' # resized images saved here
    CropImage4File(filepath,destpath)
