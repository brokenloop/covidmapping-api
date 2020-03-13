from django.utils import timezone
from typing import Dict, List, Any
from .map_client import fetch_cases
from .models import CoronaCaseRaw


def sync_db(cases: List[Dict[str, Any]]) -> None:
    """Pulls data from the google map, and syncs this data with the database.
    """
    if not valid_update_flags():
        raise ValueError('The CoronaCaseRaw table contains inconsistent update flags.')
    new_flag: bool = not latest_flag()
    new_date = timezone.now()
    # insert into db
    for case in cases:
        case['update_flag'] = new_flag
        case['date_received'] = new_date
        CoronaCaseRaw.objects.update_or_create(
            latitude=case['latitude'],
            longitude=case['longitude'],
            defaults=case,
        )
    # delete any cases which weren't in the map data
    CoronaCaseRaw.objects.filter(update_flag=(not new_flag)).delete()
    if not valid_update_flags():
        raise ValueError('The CoronaCaseRaw table contains inconsistent update flags.')
    

def latest_flag() -> bool:
    """Returns the update flag of the most recently updated record
    """
    if CoronaCaseRaw.objects.all().count() == 0:
        return True
    return CoronaCaseRaw.objects.latest('date_received').update_flag

def valid_update_flags() -> bool:
    """Returns True if all CoronaCaseRaw records have the same update flag
    """
    if CoronaCaseRaw.objects.all().count() < 2:
        return True
    return not CoronaCaseRaw.objects.filter(update_flag=(not latest_flag())).exists()
