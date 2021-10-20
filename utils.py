import os
import xml.etree.ElementTree as ET




def get_file_name(path):
    base_dir = os.path.dirname(path)
    filename, extension = os.path.splitext(os.path.basename(path))
    extension = extension.replace(".", "")

    return (base_dir, filename, extension)



def get_class_names(path):
    xml_list = []
    classes = []
    
    for file in os.listdir(path):
        if file.endswith(".xml"):
            xml_list.append(f"{path}/{file}")
    
    for i in xml_list:
        tree = ET.parse(i)
        root = tree.getroot()
        
        for bbox_attr in root.findall("object"):
            name = bbox_attr.find("name").text
            classes.append(name)
    
    return list(dict.fromkeys(classes))
