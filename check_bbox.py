import os
import xml.etree.ElementTree as ET

xml_list = []

for file in os.listdir("./VOC2012/Annotations"):
    if file.endswith(".xml"):
        xml_list.append(file)


for i in xml_list:
    tree = ET.parse(f"./VOC2012/Annotations/{i}")
    root = tree.getroot()

    for bbox_attr in root.findall("object"):
        name = bbox_attr.find("name").text
        xmin = bbox_attr.find("bndbox/xmin").text
        xmax = bbox_attr.find("bndbox/xmax").text
        ymin = bbox_attr.find("bndbox/ymin").text
        ymax = bbox_attr.find("bndbox/ymax").text

        if not xmin.isdigit():
            print(f"{xmin} | {i}")
            break
        
        if not xmax.isdigit():
            print(f"{xmax} | {i}")
            break

        if not ymin.isdigit():
            print(f"{ymin} | {i}")
            break

        if not ymax.isdigit():
            print(f"{ymax} | {i}")
            break