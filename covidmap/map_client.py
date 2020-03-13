import requests
from io import BytesIO
from typing import Dict, List, Any
from zipfile import ZipFile
from .kmz_parser import parse_link, parse_cases


def fetch_cases(link_file: str) -> List[Dict[str, Any]]:
    with ZipFile(link_file, 'r') as link_kmz:
        with link_kmz.open('doc.kml', 'r') as link_kml:
            link = parse_link(link_kml)

    response = requests.get(link)
    with ZipFile(BytesIO(response.content)) as cases_kmz:
        with cases_kmz.open('doc.kml', 'r') as kml:
            return parse_cases(kml)
