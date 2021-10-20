import os
import time
from distutils.dir_util import copy_tree
from resize import Resize
from augment import Augment
from visualize import Visualize
from utils import get_class_names

import random
from pathlib import Path
import subprocess
from PIL import Image


if __name__ == "__main__":
    start = time.perf_counter()

    Resize().resize()
    Augment().augment()
    Visualize().visualize_bboxes()

    classes = tuple(get_class_names("./dataset"))

    with open("./yolox/data/datasets/voc_classes.py", "w") as f:
        f.write("VOC_CLASSES = " + str(classes))
        
    with open("./yolox/data/datasets/coco_classes.py", "w")as f:
        f.write("COCO_CLASSES = " + str(classes))
        
    os.symlink("/home/rohan/object_detection/YOLOX/dataset/", "./datasets/VOCdevkit")

    os.mkdir("./datasets/VOCdevkit/VOC2007")
    
    root_path = "./datasets/VOCdevkit/"

    xmlfilepath = root_path + 'VOC2007/Annotations/'
    os.mkdir(xmlfilepath)
    imagefilepath = root_path + 'VOC2007/JPEGImages/'
    os.mkdir(imagefilepath)

    # Move annotations to annotations folder
    for filename in os.listdir(root_path):
        if filename.endswith('.xml'):
            with open(os.path.join(root_path, filename)) as f:
                Path(root_path + filename).rename(xmlfilepath + filename)

        if filename.endswith('.jpg'):
            with open(os.path.join(root_path, filename)) as f:
                Path(root_path + filename).rename(imagefilepath + filename)


    txtsavepath = root_path + '/VOC2007/ImageSets/Main'

    if not os.path.exists(root_path):
        print("cannot find such directory: " + root_path)
        exit()

    if not os.path.exists(txtsavepath):
        os.makedirs(txtsavepath)

    trainval_percent = 0.9
    train_percent = 0.8
    total_xml = os.listdir(xmlfilepath)
    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    print("Number of images (Train + Valid) :", tv)
    print("Number of images (Train):", tr)
    print("\n")
    print("-" * 30)

    ftrainval = open(txtsavepath + '/trainval.txt', 'w')
    ftest = open(txtsavepath + '/test.txt', 'w')
    ftrain = open(txtsavepath + '/train.txt', 'w')
    fval = open(txtsavepath + '/val.txt', 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

    os.mkdir("datasets/VOCdevkit/VOC2012")
    copy_tree("datasets/VOCdevkit/VOC2007/.", "datasets/VOCdevkit/VOC2012/.")

    end = time.perf_counter()

    print("\n")
    print("=" * 30)
    print(f"Time taken: {end - start} seconds")

    subprocess.call([f"sed -i -e 's/self.num_classes = 20/self.num_classes = {len(classes)}/g' 'exps/example/yolox_voc/yolox_x.py'"], shell = True)