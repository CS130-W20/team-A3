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
    counter = 0
    ret_text = ""
    
    for i in wiki.select("p"):
        ret_text += i.getText()
        counter += 1
        if counter > 3:
            return ret_text
    return ret_text

def get_xml(concept, concept_name_str):
    # create the file structure
    data = ET.Element('doc')
    id = ET.SubElement(data,'id')
    concept_name = ET.SubElement(data, 'concept_name')
    wiki = ET.SubElement(data, 'wiki')
    id.text = concept
    concept_name.text = concept_name_str
    wiki.text = get_wiki(concept)
    with open("./data_concepts/" + concept+".xml", 'wb') as f:
        f.write(ET.tostring(data))

def concept_to_string(c):
    return c.replace(" ", "_")

if __name__ == "__main__":
    concept_list = get_pickle_file()
    for concept in concept_list:
        s = (concept_to_string(concept))
        print(s)
        try:
            get_xml(s, concept)
        except requests.exceptions.HTTPError:
            with open("not_found_entries.txt", "a+") as f:
                f.write(s + "\n")
                
