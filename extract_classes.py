import os
import xml.etree.ElementTree as ET




def get_classes(xml_file):
    tree = ET.parse(f"./VOC/{xml_file}")
    root = tree.getroot()

    for attr in root.findall("."):
        filename = attr.find("filename").text
        width = attr.find("size/width").text
        height = attr.find("size/height").text
        depth = attr.find("size/depth").text

    for bbox_attr in root.findall("object"):
        name = bbox_attr.find("name").text
        xmin = bbox_attr.find("bndbox//xmin").text
        xmax = bbox_attr.find("bndbox//xmax").text
        ymin = bbox_attr.find("bndbox//ymin").text
        ymax = bbox_attr.find("bndbox//ymax").text

    return filename, width, height, depth, name, xmin, xmax, ymin, ymax




if __name__ == "__main__":
    xml_list = []
    classes = []
    bbox_annotations = []

    for file in os.listdir(f"./VOC"):
        if file.endswith(".xml"):
            xml_list.append(file)

    for i in xml_list:
        filename, width, height, depth, name, xmin, xmax, ymin, ymax = get_classes(i)
        classes.append(name)
        bbox_annotations.append([xmin, xmax, ymin, ymax])

    names = list(dict.fromkeys(classes))
    print(names)