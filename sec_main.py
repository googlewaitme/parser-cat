import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def write_in_xml(parsed):
    root = ET.Element('root')
    for row in parsed:
        etem = ET.SubElement(root, 'item')
        ET.SubElement(etem, 'name').text = row[0]
        ET.SubElement(etem, 'price').text = row[1]
        ET.SubElement(etem, 'delta').text = row[2]
        ET.SubElement(etem, 'symbol').text = row[3]
    tree = ET.ElementTree(root)
    tree.write('data.xml', encoding="utf-8")


def get(url, name):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    el = soup.find('a', {'title': name})
    parent = el.find_parent('tr')
    elems = parent.find_all('td')
    symbol = '↑'
    procent = elems[3].text
    if procent[0] == '-':
        symbol = '↓'
        procent = procent[1:]
    data = [
        elems[0].text,
        elems[1].text.replace('\xa0', ''),
        procent,
        symbol
    ]
    return data


url = 'https://www.finanz.ru/birzhevyye-tovary'
names = ['Алюминий', 'Медь', 'Нефть (Brent)']
data = [get(url, name) for name in names]
write_in_xml(data)
