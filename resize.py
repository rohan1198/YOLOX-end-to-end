import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import argparse
from tqdm import tqdm
from distutils.dir_util import copy_tree




def get_file_name(path):
    base_dir = os.path.dirname(path)
    filename, extension = os.path.splitext(os.path.basename(path))
    extension = extension.replace(".", "")
    return (base_dir, filename, extension)



def resize(img_path, xml_path, size):
    image = cv2.imread(img_path)

    scale_x = size / image.shape[1]
    scale_y = size / image.shape[0]

    image = cv2.resize(image, (size, size))

    new_bboxes = []

    root = ET.parse(xml_path).getroot()
    root.find("filename").text = img_path.split('/')[-1]
    size_node = root.find("size")
    size_node.find("width").text = str(size)
    size_node.find("height").text = str(size)

    for attr in root.findall("object"):
        bndbox = attr.find("bndbox")

        xmin = bndbox.find("xmin")
        xmax = bndbox.find("xmax")
        ymin = bndbox.find("ymin")
        ymax = bndbox.find("ymax")

        xmin.text = str(int(np.round(float(xmin.text) * scale_x)))
        ymin.text = str(int(np.round(float(ymin.text) * scale_y)))
        xmax.text = str(int(np.round(float(xmax.text) * scale_x)))
        ymax.text = str(int(np.round(float(ymax.text) * scale_y)))

        new_bboxes.append([1, 0, int(float(xmin.text)), int(float(ymin.text)), int(float(xmax.text)), int(float(ymax.text))])

    (_, filename, extension) = get_file_name(img_path)
    cv2.imwrite(os.path.join("./resized_dataset", ".".join([filename, extension])), image)

    tree = ET.ElementTree(root)
    tree.write(f"./resized_dataset/{filename}.xml")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dir", type = str, required = True, help = "Path to the dataset")
    parser.add_argument("--size", type = int, default = 416, help = "Resized image size")

    args = parser.parse_args()

    IMAGE_FORMATS = ('.jpeg', '.JPEG', '.png', '.PNG', '.jpg', '.JPG')

    if not os.path.isdir("./resized_dataset"):
        os.mkdir("./resized_dataset")
        print("Created directory for resized dataset")
    
    if  len(os.listdir("./resized_dataset")) == 0:
        copy_tree(args.dir, "./resized_dataset")
        print("Successfully copied all files to the resized_dataset folder")
    else:
        print("Directory is not empty")
        pass

    print("Resizing Images...")
    for root, dirs, files in os.walk("./resized_dataset"):
        for name in tqdm(files):
            filepath = root + os.sep + name
            
            if name.endswith(IMAGE_FORMATS):
                img_path = filepath
                xml_path = f"{os.path.splitext(img_path)[0]}.xml"

                resize(img_path, xml_path, size = 416)

    print(args.size)