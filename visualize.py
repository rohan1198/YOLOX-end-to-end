import os
import math
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from PIL import Image


classes = ['person', 'chair', 'bird', 'car', 'bottle', 'bicycle', 'cow', 'bus',
           'diningtable', 'aeroplane', 'boat', 'pottedplant', 'tvmonitor', 
           'train', 'horse', 'cat', 'dog', 'sheep', 'sofa', 'motorbike']


BOX_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)



def visualize_bbox(img, bbox, class_name, color = BOX_COLOR, thickness = 1):
    x_min, x_max, y_min, y_max = bbox

    cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color = color, thickness = thickness)
    
    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)    
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(img, 
                text = class_name, 
                org = (x_min, y_min - int(0.3 * text_height)),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 0.35, 
                color = TEXT_COLOR, 
                lineType = cv2.LINE_AA,
                )
    return img



def visualize(image, bboxes, class_names):
    img = image.copy()
    
    for bbox, class_name in zip(bboxes, class_names):
        img = visualize_bbox(img, bbox, class_name)
    
    return img


if __name__ == "__main__":
    imgs_list = []
    annotations = []
    augmented_images = []

    for img in os.listdir("./VOC"):
        if img.endswith(".jpg"):
            imgs_list.append(img)

    imgs_list = imgs_list[:16]

    labels = {i: classes[i] for i in range(0, len(classes))}

    bboxes = []
    names = []

    for img in imgs_list:
        file = os.path.splitext(img)[0]

        tree = ET.parse(f"./VOC/{file}.xml")
        root = tree.getroot()

        for attr in root.findall("."):
            filename = attr.find("filename").text
            #path = attr.find("path").text
            width = attr.find("size/width").text
            height = attr.find("size/height").text
            depth = attr.find("size/depth").text

        for bbox_attr in root.findall("object"):
            name = bbox_attr.find("name").text
            xmin = bbox_attr.find("bndbox//xmin").text
            xmax = bbox_attr.find("bndbox//xmax").text
            ymin = bbox_attr.find("bndbox//ymin").text
            ymax = bbox_attr.find("bndbox//ymax").text

            bboxes.append(np.array([xmin, xmax, ymin, ymax]).astype(int))
            names.append(name)

        image = cv2.imread(f"./VOC/{img}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        augmented_images.append(visualize(image, bboxes, names))

        bboxes.clear()
        names.clear()

    for num, x in enumerate(augmented_images):
        img = Image.fromarray(np.uint8(x)).convert('RGB')
        plt.subplot(4, 4, num+1)
        plt.axis('off')
        plt.imshow(img)
    plt.savefig("augmented_images.png", dpi = 500)