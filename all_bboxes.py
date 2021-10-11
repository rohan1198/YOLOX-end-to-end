import os
import xml.etree.ElementTree as ET


file = "/home/rohan/projects/yolox/VOC/2007_000027.xml"

tree = ET.parse(file)
root = tree.getroot()

for attr in root.findall("object//bndbox"):
    bbox = attr.find("xmin").text
    
    print(bbox)