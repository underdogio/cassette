import urllib2
import cassette
import os
import shutil
from datetime import datetime, timedelta
from cassette.tests.base import TestCase

TEST_URL = "http://127.0.0.1:5000/non-ascii-content"
CASSETTE_FILE = './cassette/tests/data/performance.tmp'
CASSETTE_DIRECTORY = './cassette/tests/data/performancedir/'


class TestCassettePerformanceSingleFile(TestCase):

    def setUp(self):
        self.filename = CASSETTE_FILE

        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        # Tear down for every test case
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def generate_large_cassette_yaml(self):
        # Record every next request
        cassette.insert(self.filename)

        # Create 100 requests to load in
        for i in range(0, 100):
            url = '%s?%s' % (TEST_URL, i)
            urllib2.urlopen(url).read()

        # Write out to files
        cassette.eject()

    def generate_large_cassette_json(self):
        # Record every next request
        cassette.insert(self.filename, encoding='json')

        # Create 100 requests to load in
        for i in range(0, 100):
            url = '%s?%s' % (TEST_URL, i)
            urllib2.urlopen(url).read()

        # Write out to files
        cassette.eject()

    def test_generate_speed_yaml(self):
        # Record how long it takes for the generation to take place
        start_time = datetime.now()
        self.generate_large_cassette_yaml()
        stop_time = datetime.now()

        # Verify the file generates in under 2 seconds
        two_seconds = timedelta(seconds=2)
        self.assertLess(stop_time - start_time, two_seconds)

    def fetch_frequent_cassette(self):
        # 100 times in a row
        for i in range(0, 100):
            # Open cassette
            cassette.insert(self.filename)

            # Make a few requests
            for j in range(0, 5):
                url = '%s?%s' % (TEST_URL, j)
                urllib2.urlopen(url).read()

            # Close cassette
            cassette.eject()

    def fetch_frequent_cassette_json(self):
        # 100 times in a row
        for i in range(0, 100):
            # Open cassette
            cassette.insert(self.filename, encoding='json')

            # Make a few requests
            for j in range(0, 5):
                url = '%s?%s' % (TEST_URL, j)
                urllib2.urlopen(url).read()

            # Close cassette
            cassette.eject()

    def test_fetch_speed_yaml(self):
        # Guarantee there is a large cassette to test against
        if not os.path.exists(self.filename):
            self.generate_large_cassette_yaml()

        # Record how long it takes to fetch from a file frequently
        start_time = datetime.now()
        self.fetch_frequent_cassette()
        stop_time = datetime.now()

        # Verify the frequent fetches can run in under 2 seconds
        two_seconds = timedelta(seconds=2)
        self.assertLess(stop_time - start_time, two_seconds)

    def test_generate_speed_json(self):
        # Record how long it takes for the generation to take place
        start_time = datetime.now()
        self.generate_large_cassette_json()
        stop_time = datetime.now()

        # Verify the file generates in under 2 seconds
        two_seconds = timedelta(seconds=2)
        self.assertLess(stop_time - start_time, two_seconds)

    def test_fetch_speed_json(self):
        # Guarantee there is a large cassette to test against
        if not os.path.exists(self.filename):
            self.generate_large_cassette_json()

        # Record how long it takes to fetch from a file frequently
        start_time = datetime.now()
        self.fetch_frequent_cassette_json()
        stop_time = datetime.now()

        # Verify the frequent fetches can run in under 2 seconds
        two_seconds = timedelta(seconds=2)
        self.assertLess(stop_time - start_time, two_seconds)


class TestCassettePerformanceDirectory(TestCassettePerformanceSingleFile):

    def setUp(self):
        self.filename = CASSETTE_DIRECTORY

        if os.path.exists(self.filename) and os.path.isdir(self.filename):
            shutil.rmtree(self.filename)

        # Directory must exist prior to cassette instantiation
        os.mkdir(self.filename)

    def tearDown(self):
        # Tear down for every test case
        if os.path.exists(self.filename) and os.path.isdir(self.filename):
            shutil.rmtree(self.filename)
