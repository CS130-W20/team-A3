import sys, requests, bs4
import xml.etree.ElementTree as ET

def get_wiki(concept):
    res = requests.get("https://en.wikipedia.org/wiki/" + concept)
    res.raise_for_status()
    wiki = bs4.BeautifulSoup(res.text, "html.parser")
    for i in wiki.select("p"):
        return (i.getText())


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
