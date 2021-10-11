import os
import xml.etree.ElementTree as ET



if __name__ == "__main__":
    xml_list = []
    classes = []

    for file in os.listdir(f"./VOC"):
        if file.endswith(".xml"):
            xml_list.append(file)

    for i in xml_list:
        bbox = []
        tree = ET.parse(f"./VOC/{i}")
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

            bbox.append([xmin, xmax, ymin, ymax])

        print("Filename: ", filename)
        #print("Path: ", path)
        #print("Width: ", width)
        #print("Height: ", height)
        #print("Depth: ", depth)
        #print("Name: ", name)
        #print(f"[{xmin}, {xmax}, {ymin}, {ymax}]")
        print(bbox)
        print("\n")

        classes.append(name)
        bbox.clear()
    
    names = list(dict.fromkeys(classes))
    print(names)
    print(len(names))