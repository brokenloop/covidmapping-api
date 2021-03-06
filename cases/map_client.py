import requests
from io import BytesIO
from typing import Dict, List, Any
from zipfile import ZipFile
from .kmz_parser import parse_link, parse_cases
import os


def fetch_cases() -> List[Dict[str, Any]]:
    module_dir = os.path.dirname(__file__)
    link_file = "covidmap-network-linked.kmz"
    file_path = os.path.join(module_dir, link_file)
    with ZipFile(file_path, 'r') as link_kmz:
        with link_kmz.open('doc.kml', 'r') as link_kml:
            link = parse_link(link_kml)

    response = requests.get(link)
    with ZipFile(BytesIO(response.content)) as cases_kmz:
        with cases_kmz.open('doc.kml', 'r') as kml:
            return parse_cases(kml)
