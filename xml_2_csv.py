import os
import glob
import pandas as pd
from xml.dom import minidom
import xml.etree.ElementTree as ET

def convert_xml2yolo(file_path):
    column_list = ['ImageID', 'source', 'width', 'height', 'ClassName', 'XMin', 'YMin', 'XMax', 'YMax']
    xml_list = []
    fh = open(file_path,'r')
    converted_path=[]
    #print(fname)
    lines =fh.readlines()
    #print(lines[10])
    for fname in lines:
        fname_orig = fname
        fname_orig = fname_orig.replace('.jpg', '')
        fname = fname.rstrip()
        fname = fname.replace('images','labels')
        fname = fname.replace('jpg', 'xml')
        #print(fname)
        xmldoc = minidom.parse(fname)
        itemlist = xmldoc.getElementsByTagName('object')
        size = xmldoc.getElementsByTagName('size')[0]
        width = int((size.getElementsByTagName('width')[0]).firstChild.data)
        height = int((size.getElementsByTagName('height')[0]).firstChild.data)

        for item in itemlist:
            # get class label
            classid =  (item.getElementsByTagName('name')[0]).firstChild.data
            
            # get bbox coordinates
            xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
            ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
            xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
            ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            xml_list.append([fname_orig, 'IDD', width, height, classid, xmin, ymin, xmax, ymax])
            #f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')
    xml_df = pd.DataFrame(xml_list, columns=column_list)
    xml_df.to_csv("test-annotations.csv", index=False)


def main():
    
    image_path = os.path.join(os.getcwd())
    print(image_path)
    file_path="/media/chai-rbccps/580aa4d5-a188-47a1-b2bc-d8e1e077e349/tata/datasets/IDD/IDD_Detection/test.txt"

    convert_xml2yolo(file_path)
    #xml_df.to_csv('data/tt_labels.csv', index=None)
    print('Successfully converted xml to csv.')


main()
