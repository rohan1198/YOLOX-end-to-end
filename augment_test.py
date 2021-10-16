import os
import cv2
import numpy as np
import albumentations as A
import argparse
import shutil
import time
import xml.etree.ElementTree as ET
from distutils.dir_util import copy_tree
from tqdm import tqdm


# List of transformations to apply
transforms = [A.Resize(width = 416, height = 416),      
              A.RandomCrop(width = 416, height = 416),
              A.Rotate(limit = 40, p = 0.9, border_mode = cv2.BORDER_CONSTANT),
              A.HorizontalFlip(p = 0.5),
              A.VerticalFlip(p = 0.9),
              A.RGBShift(r_shift_limit = 25, g_shift_limit = 25, b_shift_limit = 25, p = 0.9)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type = int, default = 3, help = "Number of augmentations per image")
    args  = parser.parse_args()

    # Empty directory to store images names and annotations
    imgs_list = []
    bboxes = []
    category_ids = []

    # Check if directory exists, else make one
    if not os.path.isdir("./dataset"):
        os.mkdir("./dataset")

    # If directory is not empty, copt the data from the resized dataset
    if len(os.listdir("./dataset")) == 0:
        copy_tree("./resized_dataset", "./dataset")
        print("Successfully copied all files to the Dataset folder")
    else:
        print("Directory is not empty. Skipping...")
        pass
    print("\n")

    # Check the number of images in the resized dataset
    print("Before Augmentation:")
    for path, dirs, files in os.walk("./resized_dataset/"):
        print(f"Number of images in the train folder: {len(files)}")
    for path, dirs, files in os.walk("./resized_dataset/"):
        print(f"Number of images in the valid folder: {len(files)}")
    for path, dirs, files in os.walk("./resized_dataset/"):
        print(f"Number of images in the test folder: {len(files)}")
    print("\n")

    # Read and load the configuration file
    classes = ['person', 'chair', 'bird', 'car', 'bottle', 'bicycle', 'cow', 'bus',
           'diningtable', 'aeroplane', 'boat', 'pottedplant', 'tvmonitor', 
           'train', 'horse', 'cat', 'dog', 'sheep', 'sofa', 'motorbike']

    labels = {i: classes[i] for i in range(0, len(classes))}
    print("Labels and Indices: ")
    print(labels)
    print("\n")

    start = time.perf_counter()

    for i in tqdm(os.listdir(f"./dataset")):
        if i.endswith(".jpg"):
            img_name = os.path.splitext(i)

            bboxes.clear()
            category_ids.clear()

            image = cv2.imread(f"./dataset/{i}")
            transform = A.Compose(transforms, bbox_params = A.BboxParams(format = "pascal_voc", label_fields = ["category_ids"]))

            file = ET.parse(f"./dataset/{img_name[0]}.xml")
            root = file.getroot()
            for attr in root.findall("."):
                filename = attr.find("filename")
                width = attr.find("size/width")
                height = attr.find("size/height")
                depth = attr.find("size/depth")

            for bbox_attr in root.findall("object"):
                name = bbox_attr.find("name")
                xmin = bbox_attr.find("bndbox//xmin")
                xmax = bbox_attr.find("bndbox//xmax")
                ymin = bbox_attr.find("bndbox//ymin")
                ymax = bbox_attr.find("bndbox//ymax")

                bboxes.append([int(xmin.text), int(ymin.text), int(xmax.text), int(ymax.text)])
                category_ids.append(name.text)

            for aug in range(args.n):
                transformed = transform(image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB), bboxes = bboxes, category_ids = category_ids)
                transformed_bboxes = np.array(transformed["bboxes"]).astype(int)

                cv2.imwrite(f"./dataset/{str(aug)}_{i}", transformed["image"])

                root.find('filename').text = f"./dataset/{str(aug)}_{i}"
                print(filename.text)

                for j, elem in enumerate(root.iter("xmin")):
                        elem.text = str([x[0] for x in transformed_bboxes][j])
                for j, elem in enumerate(root.iter("ymin")):
                        elem.text = str([x[1] for x in transformed_bboxes][j])
                for j, elem in enumerate(root.iter("xmax")):
                        elem.text = str([x[2] for x in transformed_bboxes][j])
                for j, elem in enumerate(root.iter("ymax")):
                        elem.text = str([x[3] for x in transformed_bboxes][j])

                tree = ET.ElementTree(root)
                tree.write(f"./dataset/{str(aug)}_{img_name[0]}.xml")
    
    end = time.perf_counter()
    
    print("\nAugmentation Complete!\n")
    print("After Augmentation:")
    for path, dirs, files in os.walk("./dataset/"):
        print(f"Number of images in the train folder: {len(files)}")
    for path, dirs, files in os.walk("./dataset/"):
        print(f"Number of images in the valid folder: {len(files)}")
    for path, dirs, files in os.walk("./dataset/"):
        print(f"Number of images in the test folder: {len(files)}")

    print("\nRemoving redundant directories...")
    shutil.rmtree("./resized_dataset")
    print("Redundant directories removed")

    print(f"\nTime taken: {round(end - start, 4)} seconds")