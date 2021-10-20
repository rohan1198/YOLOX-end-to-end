import os
import random
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from PIL import Image
from utils import get_class_names


def visualize_bbox(img, bbox, class_name, thickness = 2):
    x_min, x_max, y_min, y_max = bbox

    color = np.random.choice(range(256), size=3).astype(np.uint8).tolist()
    txt_color =  (255, 255, 255)

    cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color = color, thickness = thickness)
    
    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)    
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), color, -1)
    cv2.putText(img, 
                text = class_name, 
                org = (x_min, y_min - int(0.3 * text_height)),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 0.35, 
                color = txt_color, 
                lineType = cv2.LINE_AA,
                )
    return img


def visualize(image, bboxes, class_names):
    img = image.copy()
    
    for bbox, class_name in zip(bboxes, class_names):
        img = visualize_bbox(img, bbox, class_name)
    
    return img



class Visualize(object):
    def __init__(self, path = "./dataset"):
        self.path = path
        self.image_formats = ('.jpeg', '.JPEG', '.png', '.PNG', '.jpg', '.JPG')


    def visualize_bboxes(self, output_name = "augmented_dataset.png"):
        imgs_list = []
        augmented_images = []

        for img in os.listdir(self.path):
            if img.endswith(self.image_formats):
                imgs_list.append(img)

        imgs_list = imgs_list[:16]

        bboxes = []
        names = []

        for img in imgs_list:
            file = os.path.splitext(img)[0]

            tree = ET.parse(f"./dataset/{file}.xml")
            root = tree.getroot()

            for bbox_attr in root.findall("object"):
                name = bbox_attr.find("name").text
                xmin = bbox_attr.find("bndbox//xmin").text
                xmax = bbox_attr.find("bndbox//xmax").text
                ymin = bbox_attr.find("bndbox//ymin").text
                ymax = bbox_attr.find("bndbox//ymax").text

                bboxes.append(np.array([xmin, xmax, ymin, ymax]).astype(int))
                names.append(name)
            
            image = cv2.imread(f"./dataset/{img}")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            augmented_images.append(visualize(image, bboxes, names))
        
            bboxes.clear()
            names.clear()

        for num, x in enumerate(augmented_images):
            img = Image.fromarray(np.uint8(x)).convert('RGB')
            plt.subplot(4, 4, num+1)
            plt.axis('off')
            plt.imshow(img)
        plt.savefig(output_name, dpi = 500)