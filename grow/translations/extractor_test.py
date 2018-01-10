"""Tests for extractor."""

import unittest
from grow.pods import pods
from grow import storage
from grow.testing import testing


class ExtractorTest(unittest.TestCase):

    def setUp(self):
        dir_path = testing.create_test_pod_dir()
        self.pod = pods.Pod(dir_path, storage=storage.FileStorage)

    def test_object(self):
        pass

if __name__ == '__main__':
    unittest.main()
