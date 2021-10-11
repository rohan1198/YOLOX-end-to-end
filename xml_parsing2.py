import xml.etree.ElementTree as ET

"""
Two loops:
1. Filename, path,  width, height, depth
2. Name, xmin, xmax, ymin, ymax
"""


def parse_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()

    for attr in root.findall("."):
        filename = attr.find("filename").text
        path = attr.find("path").text
        width = attr.find("size/width").text
        height = attr.find("size/height").text
        depth = attr.find("size/depth").text

    print("Filename: ", filename)
    print("Path: ", path)
    print("Width: ", width)
    print("Height: ", height)
    print("Depth: ", depth)
    print("\n")

    for bbox_attr in root.findall("object"):
        name = bbox_attr.find("name").text
        xmin = bbox_attr.find("bndbox/xmin").text
        xmax = bbox_attr.find("bndbox/xmax").text
        ymin = bbox_attr.find("bndbox/ymin").text
        ymax = bbox_attr.find("bndbox/ymax").text

        #print(name)
        #print(f"Xmin, Xmax, Ymin, Ymax: [{xmin}, {xmax}, {ymin}, {ymax}]\n")
        print(name, xmin, xmax, ymin, ymax)




if __name__ == "__main__":
    xml_file = "chess_dataset/test/2f6fb003bb89cd401322a535acb42f65_jpg.rf.91ad9df05bd1f86bab67c8368ae5e4ad.xml"

    parse_xml(xml_file)