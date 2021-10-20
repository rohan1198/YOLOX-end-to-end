import os
import cv2
import numpy as np
import albumentations as A
import shutil
import xml.etree.ElementTree as ET
from distutils.dir_util import copy_tree
from tqdm import tqdm
from utils import get_class_names
from parameters import augmentation_parameters as P
from parameters import augmentation_images as N



aug_transforms = [
                  A.Resize(width = P["Resize"][0], height = P["Resize"][0]) if "Resize" in P.keys() else None,
                  A.RandomCrop(width = P["Random Crop"][1], height = P["Random Crop"][1]) if "Random Crop" in P.keys() else None,
                  A.Rotate(limit = P["Rotate"][1], p = P["Rotate"][0]) if "Rotate" in P.keys() else None,
                  A.HorizontalFlip(P["Horizontal Flip"][0]) if "Horizontal Flip" in P.keys() else None,
                  A.VerticalFlip(P["Vertical Flip"][0]) if "Vertical Flip" in P.keys() else None,
                  A.RGBShift(r_shift_limit = P["RGB Shift"][1], g_shift_limit = P["RGB Shift"][2], b_shift_limit = P["RGB Shift"][3], p = P["RGB Shift"][0]) if "RGB Shift" in P.keys() else None,
                  A.GaussianBlur(blur_limit = P["Gaussian Blur"][1], p = P["Gaussian Blur"][0]) if "Gaussian Blur" in P.keys() else None,
                  A.GaussNoise(var_limit = P["Gaussian Noise"][1], p = P["Gaussian Noise"][0]) if "Gaussian Noise" in P.keys() else None,
                  ]

transforms = list(filter(None.__ne__, (aug_transforms)))



class Augment(object):
    def __init__(self, n = N["n"]):
        self.n = n


    def get_file_name(self, path):
        base_dir = os.path.dirname(path)
        filename, extension = os.path.splitext(os.path.basename(path))
        extension = extension.replace(".", "")
        return (base_dir, filename, extension)


    def augment(self, path = "./dataset"):
        bboxes = []
        category_ids = []
        print("=" * 90)

        if not os.path.isdir(path):
            os.mkdir(path)

        if len(os.listdir(path)) == 0:
            copy_tree("./resized_dataset", path)
            print("Successfully copied all files to the Dataset folder")
        else:
            print("Directory is not empty. Skipping...")
            pass
        print("-" * 20)
        print("\n")

        print("Before Augmentation:")
        for path, dirs, files in os.walk("./resized_dataset/"):
            print(f"Number of images in the train folder: {int(len(files) / 2)}")
        print("-" * 70)
        print("\n")
        
        classes = get_class_names(path)

        labels = {i: classes[i] for i in range(0, len(classes))}
        print("Classes:")
        print(labels)
        print("-" * 90)
        print("\n")

        print("Augmenting Images...")
        for i in tqdm(os.listdir(f"./dataset/")):
            if i.endswith(".jpg"):
                img_name = os.path.splitext(i)

                bboxes.clear()
                category_ids.clear()

                xml_path = ET.parse(f"./dataset/{img_name[0]}.xml")
                root = xml_path.getroot()

                for bbox_attr in root.findall("object"):
                    name = bbox_attr.find("name")
                    xmin = bbox_attr.find("bndbox//xmin")
                    xmax = bbox_attr.find("bndbox//xmax")
                    ymin = bbox_attr.find("bndbox//ymin")
                    ymax = bbox_attr.find("bndbox//ymax")

                    bboxes.append([int(xmin.text), int(ymin.text), int(xmax.text), int(ymax.text)])
                    category_ids.append(name.text)
                
                image = cv2.imread(f"./dataset/{i}")
                transform = A.Compose(transforms, 
                                    bbox_params = A.BboxParams(format = "pascal_voc", label_fields = ["category_ids"]))
                
                for aug in range(self.n):
                    transformed = transform(image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB), bboxes = bboxes, category_ids = category_ids)
                    transformed_bboxes = np.array(transformed["bboxes"]).astype(int)

                    cv2.imwrite(f"./dataset/{img_name[0]}_{str(aug)}.jpg", transformed["image"])

                    root.find('filename').text = f"./dataset/{img_name[0]}_{str(aug)}.jpg"

                    for j, elem in enumerate(root.iter("xmin")):
                            elem.text = str([x[0] for x in transformed_bboxes][j])
                    for j, elem in enumerate(root.iter("ymin")):
                            elem.text = str([x[1] for x in transformed_bboxes][j])
                    for j, elem in enumerate(root.iter("xmax")):
                            elem.text = str([x[2] for x in transformed_bboxes][j])
                    for j, elem in enumerate(root.iter("ymax")):
                            elem.text = str([x[3] for x in transformed_bboxes][j])

                    tree = ET.ElementTree(root)
                    tree.write(f"./dataset/{img_name[0]}_{str(aug)}.xml")


        print("\nAugmentation Complete!")
        print("-" * 20)
        print("\n")

        print("After Augmentation:")
        for path, dirs, files in os.walk("./dataset/"):
            print(f"Number of images in the train folder: {int(len(files) / 2)}")

        print("-" * 90)
        print("\n")

        print("\nRemoving redundant directories...")
        shutil.rmtree("./resized_dataset")
        print("Redundant directories removed")

        print("\n")
        print("=x" * 45)
        print("\n")