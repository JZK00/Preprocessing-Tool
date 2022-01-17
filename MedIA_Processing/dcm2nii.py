# -*- coding: utf-8 -*-
import os
import SimpleITK as sitk


def get_dnimg_pid_sname(data_path):

    # string_list = data_path.split("/")
    string_list = data_path.split("\\")
    name_list = data_path.split("_")
    for name_ in name_list:
        if len(name_) > 4 and name_[:4] == "0000":
            patient_id = name_
            series_name = string_list[-1]
    return patient_id, series_name


if __name__ == "__main__":

    # 需要根据实际路径进行修改
    # root_path = "/media/Data/zijian/dataset1"
    root_path = "E:\\zijian\\dataset1"
    dcm_dir = "dcm"
    nii_dir = "nii"

    in_path = os.path.join(root_path, dcm_dir)
    out_path = os.path.join(root_path, nii_dir)

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for root, dirs, files in os.walk(in_path):
        for dir_ in dirs:
            pid_path = os.path.join(root, dir_)
            reader = sitk.ImageSeriesReader()

            print(f"\ndir_ = {dir_}")
            series_ids = reader.GetGDCMSeriesIDs(pid_path)
            if not series_ids:
                print(f"\n{pid_path}")
                print("Warning! Directory does not contain a DICOM series.")
                continue
            else:
                print(f"{pid_path}")
                # 文件夹中只包含1个dicom影像序列
                series_num = len(series_ids)
                if series_num == 1:
                    print("Only 1 series are found.")
                    series_file_names = reader.GetGDCMSeriesFileNames(
                        pid_path, series_ids[0])
                    if len(series_file_names) <= 1:
                        print("Warning: no more than one slice!")
                        continue
                    else:
                        # str_list = pid_path.split("/")
                        str_list = pid_path.split("\\")
                        # 需要根据文件名进行修改
                        for str_ in str_list:
                            if len(str_) > 4 and str_[:4] == "0000":
                                pid = str_
                                sname = f"series{1}"
                                break
                            elif "0000" in str_:
                                pid, sname = get_dnimg_pid_sname(pid_path)
                                break
                            elif "TCGA" in str_:
                                pid = str_
                                sname = str_list[-1]
                                break
                        reader.SetFileNames(series_file_names)
                        dcm_img = reader.Execute()

                        out_fname = os.path.join(out_path, f"{pid}_{sname}.nii")
                        sitk.WriteImage(dcm_img, out_fname)
                # 文件夹中包含多个dicom影像序列
                else:
                    print(f"{series_num} series are found.")
                    for idx, series_ID in enumerate(series_ids):
                        info = {}
                        series_file_names = reader.GetGDCMSeriesFileNames(
                            pid_path, series_ID)
                        if len(series_file_names) <= 1:
                            print("Warning: no more than one slice!")
                            continue
                        else:
                            # str_list = pid_path.split("/")
                            str_list = pid_path.split("\\")
                            # 需要根据文件名进行修改
                            for str_ in str_list:
                                if len(str_) > 4 and str_[:4] == "0000":
                                    pid = str_
                                    break
                            reader.SetFileNames(series_file_names)
                            dcm_img = reader.Execute()
                            try:
                                reader.MetaDataDictionaryArrayUpdateOn()
                                sname = reader.GetMetaData(0, '0008|103e')
                            except RuntimeError:
                                sname = f"series{idx + 1}"
                            out_fname = os.path.join(out_path, f"{dir_}_{sname}.nii")
                            sitk.WriteImage(dcm_img, out_fname)

    print("\nConversion finished.")
