import sys, requests, bs4
import xml.etree.ElementTree as ET
import pickle

def get_pickle_file():
    f = open("combined_concept_list.pkl", 'rb')
    ret = pickle.load(f)
    f.close()
    return ret

def get_wiki(concept):
    res = requests.get("https://en.wikipedia.org/wiki/" + concept)
    res.raise_for_status()
    wiki = bs4.BeautifulSoup(res.text, "html.parser")
    for i in wiki.select("p"):
        return (i.getText())

def get_xml(concept):
    # create the file structure
    data = ET.Element('doc')
    id = ET.SubElement(data,'id')
    concept_name = ET.SubElement(data, 'concept_name')
    wiki = ET.SubElement(data, 'wiki')
    id.text = "Concept_01"
    concept_name.text = "Machine Learning"
    wiki.text = get_wiki("machine_learning")
    with open("Concept_01.xml", 'wb') as f:
        f.write(ET.tostring(data))

def concept_to_string(c):
    return c.replace(" ", "_")

if __name__ == "__main__":
    concept_list = get_pickle_file()
    for concept in concept_list:
        s = (concept_to_string(concept))
        print(s)
        print(get_wiki(s))
