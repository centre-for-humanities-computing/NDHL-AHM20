#!/home/knielbo/virtenvs/ndhl/bin/python
"""
Extract content and metadata for NYT collection

@author: kln@cas.au.dk
"""
import os
import sys
import glob
import re
from xml.dom.minidom import parse, Node
from pandas import DataFrame

# parser
def tag2list(fname, tag = "p"):
    """
    Get text node content based on tags in xml file
    - store every element in list
    """
    xmltree=parse(fname)
    tag_list = []
    for node1 in xmltree.getElementsByTagName(tag):
        for node2 in node1.childNodes:
            if node2.nodeType == Node.TEXT_NODE:
                tag_list.append(node2.data)
    return tag_list

# metadata to dat file with fname as key
def gen_metadata(text, meta_tags = ["publication_day_of_month", "publication_month", "publication_year","publication_day_of_week","dsk","print_page_number","print_section","print_column"]):
    """
    Create metadata file with objects in rows and features in columns
    - text: vanilla nitf xml file
    - meta_tags: tags from text to be treated as metadata
    """
    match = re.findall(r'<meta content=(.*)/>',text)
    colname = []
    metadata = []
    colname = []
    metadata = []
    for i in range(len(match)):
        tmp = match[i]
        tmp = re.sub(r'"','',tmp)
        tmp = tmp.split(" name=")
        metadata.append(tmp[0])
        colname.append(tmp[1])
    result = []
    for tag in meta_tags:# try: result.append(metadata[colname.index(tag)]); except: result.append(NA)
        result.append(metadata[colname.index(tag)])
    return result

# title, and content to dat file with fname as key
## TODO: remove repetitions of content
def get_content(fname):
    """
    Extract content from paragraphs in xml file
    - fname: filename for xml
    - remove LEAD paragraphs
    - keep paragraph structure with line char
    """
    content = tag2list(fname)
    title = tag2list(fname, tag = "title")[0]
    pat = re.compile(r"LEAD:")
    idx = []
    for i, p in enumerate(content):
        if pat.match(p):
            idx.append(i)
    if idx:
        for i in sorted(idx, reverse = True):
            del content[i]
    return " \n".join(content), title

def main():
    #fpath = sys.argv[1]
    fpath = os.path.join("..","dat","sample")# sample
    #fpath = os.path.join("..","..","..","data","nyt","xml")# full data set
    fnames = sorted(glob.glob(os.path.join(fpath,"*.xml")))
    META, DATA = list(), list()
    for fname in fnames:
        try:
            fileid = fname.split("/")[-1].split(".")[0]
            print(fileid)
            with open(fname, "r") as f:
                text = f.read()
            #text = open(fname).read()
            META.append([fileid] + gen_metadata(text))
            DATA.append([fileid, tag2list(fname, tag = "title")[0], get_content(fname)])
        except:
            pass
    DF_meta = DataFrame(META)
    DF_content = DataFrame(DATA)
    DF_meta.columns = ["id", "publication_day_of_month", "publication_month", "publication_year","publication_day_of_week","dsk","print_page_number","print_section","print_column"]
    DF_content.columns = ["id","title","paragraphs"]
    datpath = os.path.join("..", "dat")
    DF_meta.to_csv(os.path.join(datpath, "metadata_sample.csv"), index = False)
    DF_content.to_csv(os.path.join(datpath, "content_sample.csv"), index = False)

if __name__ == '__main__':
    main()
