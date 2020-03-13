import xml.sax, xml.sax.handler
import xml.dom.minidom
import csv
from typing import Dict, List, Any, IO

CASE_TYPES = {
    'Suspected Cases': 'Suspected',
    'Confirmed Cases': 'Confirmed',
    'Recovered Cases': 'Recovered',
    'Deceased Cases': 'Deceased',
    'Quarantine': 'Quarantined',
}


def parse_link(kml: IO[bytes]) -> str:
    DOMTree = xml.dom.minidom.parse(kml)
    collection = DOMTree.documentElement
    return collection.getElementsByTagName('href')[0].childNodes[0].data 


def parse_cases(kml: IO[bytes]) -> List[Dict[str, Any]]:
    DOMTree = xml.dom.minidom.parse(kml)
    collection = DOMTree.documentElement

    result = []

    folders = collection.getElementsByTagName('Folder')
    for folder in folders:
        case_type = folder.getElementsByTagName('name')[0].childNodes[0].data
        if case_type in CASE_TYPES:
            placemarks = folder.getElementsByTagName('Placemark')
            print(case_type)
            for placemark in placemarks:
                try:
                    name = placemark.getElementsByTagName('name')[0].childNodes[0].data
                    description = placemark.getElementsByTagName('description')[0].childNodes[0].data
                    point = placemark.getElementsByTagName('Point')[0]
                    coordinates = point.getElementsByTagName('coordinates')[0].childNodes[0].data
                    longitude, latitude, _ = coordinates.split(',')
                    row = {
                        'case_type': CASE_TYPES[case_type],
                        'latitude': latitude.strip(),
                        'longitude': longitude.strip(),
                        'name': f"\'{name.strip()}\'",
                        'description': f"\'{description.strip()}\'",
                    }
                    result.append(row)
                except Exception as e:
                    print(e)
    return result


def save_csv(cases_dict, outputfile):
    with open(outputfile, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, 
                            fieldnames=cases_dict[0].keys(),
                            delimiter=',')
        fc.writeheader()
        fc.writerows(cases_dict)
