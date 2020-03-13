from django.utils import timezone
from .map_client import fetch_cases
from .models import CoronaCaseRaw


def sync_db() -> None:
    """Pulls data from the google map, and syncs this data with the database.
    """
    if not valid_update_flags():
        raise ValueError('The CoronaCaseRaw table contains inconsistent update flags.')
    new_flag: bool = not latest_flag()
    # fetch map data
    cases = fetch_cases()
    # insert into db
    for case in cases:
        CoronaCaseRaw.objects.update_or_create(
            case_type=case['case_type'],
            name=case['name'],
            description=case['description'],
            latitude=case['latitude'],
            longitude=case['longitude'],
            update_flag=new_flag,
            date_received=timezone.now(),
        )
    # delete any cases which weren't in the map data
    CoronaCaseRaw.objects.filter(update_flag=(not new_flag)).delete()
    if not valid_update_flags():
        raise ValueError('The CoronaCaseRaw table contains inconsistent update flags.')
    

def latest_flag() -> bool:
    """Returns the update flag of the most recently updated record
    """
    return CoronaCaseRaw.objects.latest('date_received').update_flag

def valid_update_flags() -> bool:
    """Returns True if all CoronaCaseRaw records have the same update flag
    """
    return not CoronaCaseRaw.objects.filter(update_flag=(not latest_flag())).exists()
