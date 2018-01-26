"""Tests for extractor."""

import unittest
from grow.pods import pods
from grow import storage
from grow.testing import testing
from grow.translations import extractor


class ExtractorTest(unittest.TestCase):
    """Translation extractor tests."""

    def setUp(self):
        dir_path = testing.create_test_pod_dir()
        self.pod = pods.Pod(dir_path, storage=storage.FileStorage)
        self.extract = extractor.Extractor(self.pod)

    def test_object(self):
        """Object extraction extracts basic keys correctly."""
        test_obj = {
            'key': 'value',
            'foo@': 'bar',
        }
        results = self.extract.extract_object(test_obj)
        self.assertEqual(set(['bar']), set(results.messages))

    def test_object_nested_objects(self):
        """Object extraction extracts nested keys correctly."""
        test_obj = {
            'key': {
                'nested@': 'value',
                'other': 'valued',
            },
            'bar': {
                'baz': {
                    'bum': 'dum',
                    'boo@': 'foobar',
                },
            },
            'foo@': 'bar',
        }
        results = self.extract.extract_object(test_obj)
        self.assertEqual(set(['bar', 'value', 'foobar']), set(results.messages))

    def test_object_nested_arrays(self):
        """Object extraction extracts nested keys correctly."""
        test_obj = {
            'key@': [
                'value',
                'foo',
            ],
            'bar': [
                {
                    'bum@': [
                        'baz',
                        'trae',
                    ],
                    'boo@': 'foobar',
                    'tre': 'paz',
                },
            ],
        }
        results = self.extract.extract_object(test_obj)
        self.assertEqual(set(['foo', 'value', 'baz', 'trae', 'foobar']), set(results.messages))


class ExtractedMessagesTest(unittest.TestCase):
    """Extracted messages tests."""

    def setUp(self):
        self.results = extractor.ExtractedMessages()

    def test_message(self):
        """Messages are part of the extracted string results."""
        self.results.add_message('foo')
        self.assertEqual(set(['foo']), set(self.results.messages))

    def test_translations(self):
        """Translations are part of the extracted results."""
        self.results.add_translation('es', 'foo', 'foobar')
        self.assertEqual({
            'foo': 'foobar',
        }, self.results.get_translations('es'))

    def test_translations_patterns(self):
        """Patterns are used to match the locales against translations."""
        self.results.add_translation('(es|fr)', 'foo', 'foobar')
        self.results.add_translation('es', 'fuz', 'ball')
        self.results.add_translation('fr', 'bar', 'bell')
        self.assertEqual({
            'foo': 'foobar',
            'fuz': 'ball',
        }, self.results.get_translations('es'))
        self.assertEqual({
            'foo': 'foobar',
            'bar': 'bell',
        }, self.results.get_translations('fr'))
        self.assertEqual({}, self.results.get_translations('en'))

    def test_missing_base(self):
        """Translations cannot be missing the base string."""
        with self.assertRaises(extractor.MissingBaseError):
            self.results.add_translation('es', '', 'foobar')

        with self.assertRaises(extractor.MissingBaseError):
            self.results.add_translation('es', None, 'foobar')


if __name__ == '__main__':
    unittest.main()
