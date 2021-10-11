import xml.etree.ElementTree as ET



#xmlfile = "document.xml"
xmlfile = "chess_dataset/test/2f6fb003bb89cd401322a535acb42f65_jpg.rf.91ad9df05bd1f86bab67c8368ae5e4ad.xml"

tree = ET.parse(xmlfile)
root = tree.getroot()

#print(root[4][1].text)

"""
for size in root.findall("size"):
    width = size.find("width").text
    height = size.find("height").text
    depth = size.find("depth").text
    print(width, height, depth)

for obj in root.findall("object"):
    name = obj.find("name").text
    xmin = obj.find("bndbox/xmin").text
    print(name, xmin)
"""



# filename, width, height, depth, name, xmin, xmax, ymin, ymax


for elem in root.findall("."):
    filename = elem.find("filename").text
    path = elem.find("path").text
    
    width = elem.find("size/width").text
    height = elem.find("size/height").text
    depth = elem.find("size/depth").text

    name = elem.find("object/name").text
    xmin = elem.find("object/bndbox/xmin").text
    xmax = elem.find("object/bndbox/xmax").text
    ymin = elem.find("object/bndbox/ymin").text
    ymax = elem.find("object/bndbox/ymax").text

    print("Filename: ", filename)
    print("Path: ", path)
    print("Width: ", width)
    print("Height: ", height)
    print("Depth: ", depth)
    print("Name: ", name)
    print("Xmin: ", xmin)
    print("Xmax: ", xmax)
    print("Ymin: ", ymin)
    print("Ymax: ", ymax)