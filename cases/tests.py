import mock
from django.test import TestCase
from django.utils import timezone
from cases.map_client import fetch_cases
from .updater import Updater
from .models import CoronaCaseRaw


def mocked_fetch_cases(*args, **kwargs):
    return SAMPLE_DATA

class UpdaterTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(UpdaterTests, self).__init__(*args, **kwargs)
        self.updater = Updater()

    def test_sync_db_create(self):
        """Test that cases can be inserted
        """
        self.updater.sync_db(SAMPLE_DATA)
        expected_num_entries: int = len(SAMPLE_DATA)
        num_entries: int = CoronaCaseRaw.objects.all().count()
        self.assertEqual(expected_num_entries, num_entries)

    def test_sync_db_update(self):
        """Test that cases can be updated
        """
        update_flag: bool = True
        date_received = timezone.now() - timezone.timedelta(hours=1)
        first_case = SAMPLE_DATA[0]
        second_case = SAMPLE_DATA[1]
        CoronaCaseRaw.objects.get_or_create(
            case_type=first_case['case_type'],
            name=first_case['name'],
            description="updated description",
            latitude=first_case['latitude'],
            longitude=first_case['longitude'],
            update_flag=update_flag,
            date_received=date_received,
        )
        CoronaCaseRaw.objects.get_or_create(
            case_type=second_case['case_type'],
            name='updated name',
            description=second_case['description'],
            latitude=second_case['latitude'],
            longitude=second_case['longitude'],
            update_flag=update_flag,
            date_received=date_received,
        )
        self.updater.sync_db(SAMPLE_DATA)
        expected_num_entries: int = len(SAMPLE_DATA)
        num_entries: int = CoronaCaseRaw.objects.all().count()
        self.assertEqual(expected_num_entries, num_entries)

    def test_sync_db_delete(self):
        """Test that cases can be deleted
        """
        update_flag: bool = True
        date_received = timezone.now() - timezone.timedelta(hours=1)
        first_case = SAMPLE_DATA[0]
        second_case = SAMPLE_DATA[1]
        CoronaCaseRaw.objects.get_or_create(
            case_type=first_case['case_type'],
            name=first_case['name'],
            description=first_case['description'],
            latitude=first_case['latitude'],
            longitude=first_case['longitude'],
            update_flag=update_flag,
            date_received=date_received,
        )
        CoronaCaseRaw.objects.get_or_create(
            case_type=second_case['case_type'],
            name=second_case['name'],
            description=second_case['description'],
            latitude=second_case['latitude'],
            longitude=second_case['longitude'],
            update_flag=update_flag,
            date_received=date_received,
        )
        self.updater.sync_db([])
        expected_num_entries: int = 0
        num_entries: int = CoronaCaseRaw.objects.all().count()
        self.assertEqual(expected_num_entries, num_entries)

    def test_sync_db_invalid_flags(self):
        """Test that cases can be deleted
        """
        date_received = timezone.now() - timezone.timedelta(hours=1)
        first_case = SAMPLE_DATA[0]
        second_case = SAMPLE_DATA[1]
        CoronaCaseRaw.objects.get_or_create(
            case_type=first_case['case_type'],
            name=first_case['name'],
            description="updated description",
            latitude=first_case['latitude'],
            longitude=first_case['longitude'],
            update_flag=True,
            date_received=date_received,
        )
        CoronaCaseRaw.objects.get_or_create(
            case_type=second_case['case_type'],
            name='updated name',
            description=second_case['description'],
            latitude=second_case['latitude'],
            longitude=second_case['longitude'],
            update_flag=False,
            date_received=timezone.now(),
        )
        self.updater.sync_db([])


    def test_sync_db_multiple_updates(self):
        self.updater.sync_db(SAMPLE_DATA)
        self.updater.sync_db([SAMPLE_DATA[0]])
        expected_num_entries: int = 1
        num_entries: int = CoronaCaseRaw.objects.all().count()
        self.assertEqual(expected_num_entries, num_entries)

    def test_should_update_true(self):
        update_delta: int = self.updater.interval * 2
        date_received = timezone.now() - timezone.timedelta(seconds=update_delta)
        first_case = SAMPLE_DATA[0]
        CoronaCaseRaw.objects.get_or_create(
            case_type=first_case['case_type'],
            name=first_case['name'],
            description=first_case['description'],
            latitude=first_case['latitude'],
            longitude=first_case['longitude'],
            update_flag=True,
            date_received=date_received,
        )
        self.assertTrue(self.updater.should_update())

    def test_should_update_false(self):
        update_delta: int = self.updater.interval // 2
        date_received = timezone.now() - timezone.timedelta(seconds=update_delta)
        first_case = SAMPLE_DATA[0]
        CoronaCaseRaw.objects.get_or_create(
            case_type=first_case['case_type'],
            name=first_case['name'],
            description=first_case['description'],
            latitude=first_case['latitude'],
            longitude=first_case['longitude'],
            update_flag=True,
            date_received=date_received,
        )
        self.assertFalse(self.updater.should_update())

    # def test_with_live_data(self):
    #     cases = fetch_cases()
    #     self.updater.sync_db(cases)


SAMPLE_DATA = [
    {
        'case_type': 'Suspected',
        'latitude': '43.7044406',
        'longitude': '-72.2886935',
        'name': 'USA - New Hampshire - Dartmouth College',
        'description': '4 cases suspected MAR 05-2020 <br><br>Four students at Dartmouth College’s Geisel School of Medicine have been added to the growing list of people under two-week self-quarantine after they were exposed to the state\'s second coronavirus patient.<br><br>https://www.unionleader.com/news/health/coronavirus/four-dartmouth-medical-students-exposed-to-coronavirus/article_b803eac1-36db-548d-a073-94936be04f40.html',
    },
    {
        'case_type': 'Confirmed',
        'latitude': '53.0852407',
        'longitude': '6.9778815',
        'name': 'Netherlands - Pekela',
        'description': '1 confirmed case.<br><br>https://www.pekela.nl/Bestuur/Nieuws/Nieuwsarchief/2020/Eerste_twee_besmettingen_met_coronavirus_in_Groningen 11-MAR-2020',
    },
]


