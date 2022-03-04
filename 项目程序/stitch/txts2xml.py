#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on : 2021-11-15
#  Author : Joe Aaron
#  Email :  pant333@163.com
#  Description :  transfer txt to xml
#  How to run : python .\txt2xml/py /VC /calib.xml
############################################################
import os
import glob
import sys
from xml.dom.minidom import Document
from tqdm import tqdm

path = os.path.dirname(__file__)

def read_txt(txt_dir):
    """ 根据 txt 文件夹路径读取数据
    Args:
        txt_dir (str)：
    Return:
        rotates (dict)：
        trans (dict)：
    """
    calib_num = 0
    rotates = {}
    trans = {}

    txt_list = glob.glob(os.path.join(path + txt_dir, '*.txt'))

    for i,file in enumerate(txt_list):
        calib_num += 1
        with open(os.path.join(txt_dir, file)) as f:
            lines = f.readlines()
            rotate = []
            rotate.extend(lines[2].split()[0:3])
            rotate.extend(lines[3].split()[0:3])
            rotate.extend(lines[4].split()[0:3])
            tran = []
            tran.append(lines[2].split()[-1])
            tran.append(lines[3].split()[-1])
            tran.append(lines[4].split()[-1])
            for j,v in enumerate(rotate):
                key = (i,j)
                rotates[key]=v
            for j,v in enumerate(tran):
                key = (i,j)
                trans[key]=v
    return calib_num, rotates, trans

def write_xml(calib_num, rotates,trans,save_xml_path):
    """ 保存信息为xml
    Args:
        rotates (dict)：
        trans (dict)：
        save_xml_path (str)：
    """
    xml_doc = Document()
    calib_result = xml_doc.createElement("CalibrationResult")
    xml_doc.appendChild(calib_result)
    calib_info = xml_doc.createElement("CalibrationInformation")
    num = str(calib_num)
    calib_info.setAttribute("CaliNum", num)

    for n in range(calib_num):
        for i in tqdm(rotates):
            if (n == i[0]):
                calib_info.setAttribute("Rotate_{}_{}".format(i[0],i[1]),rotates[i])

        for i in tqdm(trans):
            if (n == i[0]):
                calib_info.setAttribute("Tran_{}_{}".format(i[0],i[1]),trans[i])

        calib_info.setAttribute("RMS_{}".format(n), "0.000000")

    calib_result.appendChild(calib_info)
    with open(path + save_xml_path, 'w') as fxml:
        xml_doc.writexml(fxml, addindent='\t', newl='\n', encoding="utf-8")


if __name__ == '__main__':
    #txt_dir = r"/VC"
    #save_xml_path = r"/calibVC.xml"

    txt_dir = sys.argv[1]
    save_xml_path = sys.argv[2]

    calib_num, rotates, trans = read_txt(txt_dir)
    write_xml(calib_num, rotates, trans, save_xml_path)
    print("done!")


