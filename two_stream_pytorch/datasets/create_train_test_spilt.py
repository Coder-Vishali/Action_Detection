# Usage:
# python build_file_list.py --dataset gms --frame_path gms_frames --out_list_path settings

import os
import numpy as np
import pathlib

dataset_directory = r"gms"
folder = os.path.join(os.getcwd(), dataset_directory)
print("Data Directory: ", folder)

for i in range(1,4):
    # Count the files in the given image folder
    for class_path in pathlib.Path(folder).iterdir():
        print("\nClass path: ", class_path)
        dataset_path = "/media/laiml/DATA/ActionDetection/" + str(class_path).rsplit("\\",1)[1] + "/"
        # print(dataset_path)
        allFileNames = os.listdir(class_path)
        np.random.shuffle(allFileNames)
        test_ratio = 0.25
        train_FileNames, test_FileNames = np.split(np.array(allFileNames),
                                                   [int(len(allFileNames) * (1 - test_ratio))])
        train_FileNames = [str(class_path) + '\\' + name for name in train_FileNames.tolist()]
        test_FileNames = [str(class_path) + '\\' + name for name in test_FileNames.tolist()]
        # print("train_FileNames", train_FileNames)
        # print("test_FileNames", test_FileNames)
        print("train_FileNames", len(train_FileNames))
        print("test_FileNames", len(test_FileNames))

        split_directory = r"gms_splits"
        split_folder = os.path.join(os.getcwd(), split_directory)
        train_list = str(split_folder) + "\\" + "trainlist_" + str(i) + ".txt"
        file2 = open(train_list, 'a')

        for each in train_FileNames:
            print(dataset_path + each.rsplit('\\', 1)[1])
            file2.write(dataset_path + each.rsplit('\\', 1)[1])
            file2.write("\n")
        file2.close()

        test_list = str(split_folder) + "\\" + "testlist_" + str(i) + ".txt"
        file3 = open(test_list, 'a')

        for each in test_FileNames:
            print(dataset_path + each.rsplit('\\', 1)[1])
            file3.write(dataset_path + each.rsplit('\\', 1)[1])
            file3.write("\n")
        file3.close()