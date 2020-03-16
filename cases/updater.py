import schedule
import threading
import time
from django.utils import timezone
from typing import Dict, List, Any
from .decorators import skip_when_testing
from .map_client import fetch_cases
from .models import CoronaCaseRaw


class Updater():
    # 1 hour
    interval = 3600

    @skip_when_testing
    def run(self):
        self.update()
        schedule.every(self.interval).seconds.do(self.update)
        self.run_continuously(self.interval)

    def run_continuously(self, interval: int = 1):
        """Runs pending tasks continuously on a non-blocking thread

        Notes:
            Taken from here: https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def update(self):
        print('updating...')
        cases = fetch_cases()
        self.sync_db(cases)
        print('finished updating')

    def sync_db(self, cases: List[Dict[str, Any]]) -> None:
        """Pulls data from the google map, and syncs this data with the database.
        """
        if not self.valid_update_flags():
            raise ValueError('The CoronaCaseRaw table contains inconsistent update flags.')
        new_flag: bool = not self.latest_flag()
        new_date = timezone.now()
        # insert into db
        for case in cases:
            CoronaCaseRaw.objects.update_or_create(
                defaults={
                    'update_flag': new_flag,
                    'date_received': new_date,
                    **case,
                },
                **case
            )
        # delete any cases which weren't in the map data
        CoronaCaseRaw.objects.filter(update_flag=(not new_flag)).delete()
        if not self.valid_update_flags():
            raise ValueError('The CoronaCaseRaw table contains inconsistent update flags.')
        
    def latest_flag(self) -> bool:
        """Returns the update flag of the most recently updated record
        """
        if CoronaCaseRaw.objects.all().count() == 0:
            return True
        return CoronaCaseRaw.objects.latest('date_received').update_flag

    def valid_update_flags(self) -> bool:
        """Returns True if all CoronaCaseRaw records have the same update flag
        """
        if CoronaCaseRaw.objects.all().count() < 2:
            return True
        return not CoronaCaseRaw.objects.filter(update_flag=(not self.latest_flag())).exists()
