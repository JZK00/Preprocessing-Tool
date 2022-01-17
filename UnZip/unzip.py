#!/usr/bin/env python3
# .zip .rar .tar .tgz .tar.gz .tar.bz2 .tar.bz .tar.tgz
import os
import zlib
import unrar
import shutil
import zipfile
import tarfile
from time import sleep
# from unrar import rarfile

filepath = "./all-MRI"  #relative path

class BaseTool(object):
    def __init__(self, path):
        self.path = path
        self.compress = [".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz",".zip",".rar"]
 
    def iszip(self,  file):
        for z in self.compress:
            if file.endswith(z):
                return z
 
    def zip_to_path(self, file):
        for i in self.compress:
            file = file.replace(i,"")
        return file

    def error_record(self, info):
        with open("error.txt","a+") as r:
            r.write(info+"\n")

    def un_zip(self, src, dst):
        """ src : aa/asdf.zip
            dst : unzip/aa/asdf.zip
        """
        try:
            zip_file = zipfile.ZipFile(src)
            uz_path = self.zip_to_path(dst)
            if not os.path.exists(uz_path):
                os.makedirs(uz_path)
            for name in zip_file.namelist():
                zip_file.extract(name, uz_path)
            zip_file.close()
        except zipfile.BadZipfile:
            pass
        except zlib.error:
            print("zlib error : "+src)
            self.error_record("zlib error : "+src)
 
    def un_rar(self, src, dst):
        try:
            rar = unrar.rarfile.RarFile(src)
            uz_path = self.zip_to_path(dst)
            rar.extractall(uz_path)
        except unrar.rarfile.BadRarFile:
            pass
        except Exception as e:
            print(e)
            self.error_record(str(e)+src)    

    def un_tar(self, src, dst):
        try:
            tar = tarfile.open(src)
            uz_path = self.zip_to_path(dst)
            tar.extractall(path = uz_path)
        except tarfile.ReadError:
            pass
        except Exception as e:
            print(e)
            self.error_record(str(e)+src)

 
class UnZip(BaseTool):
    """ UnZip files """
    def __init__(self, path):
        super(UnZip, self).__init__(self)
        self.path = path
        self.output = "./all-MRI/unzip/"
        self.current_path = os.getcwd()+"/"
 
    def recursive_unzip(self, repath):
        """recursive unzip file
        """
        for (root, dirs, files) in os.walk(repath):
            for filename in files:
                src = os.path.join(root,filename)
                if self.iszip(src) == ".zip":
		            #print("[+] child unzip: "+src)
                    self.un_zip(src, src)
                    os.remove(src)
                    self.recursive_unzip(self.zip_to_path(src))
                    sleep(0.1)
                if self.iszip(src) == ".rar":
                    from unrar import rarfile
                    print("[+] child unrar : "+src)
                    self.un_rar(src,src) 
                    os.remove(src)
                    self.recursive_unzip(self.zip_to_path(src))
                    sleep(0.1)
                if self.iszip(src) in (".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz"):
                    print("[+] child untar : "+src)
                    self.un_tar(src,src)
                    os.remove(src)
                    self.recursive_unzip(self.zip_to_path(src))
                    sleep(0.1)

    def main_unzip(self):
        for (root, dirs, files) in os.walk(self.path):
            for filename in files:
                zippath = os.path.join(self.output,root)
                if not os.path.exists(zippath):
                    os.makedirs(zippath)
                src = os.path.join(root,filename)
                dst = os.path.join(self.output,root,filename)
                if self.iszip(src) == ".zip":
                    print("[+] main unzip : "+src)
                    self.un_zip(src,dst)
                if self.iszip(src) == ".rar":
                    from unrar import rarfile
                    print("[+] main unrar : "+src)
                    self.un_rar(src,dst)
                if self.iszip(src) in (".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz"):
                    print("[+] main untar : "+src)
                    self.un_tar(src,dst)
                else:
                    try:
                        shutil.copyfile(src,dst)
                    except OSError as e:
                        print(str(e))
                        self.error_record(str(e))
                     
        self.recursive_unzip(self.output+self.path)
 

def main():
    z = UnZip(filepath)   #relative path
    z.main_unzip()
 
if __name__ == '__main__':
    main()