"""Grow translation extractor."""

import collections
import re


class Error(Exception):
    """Base error for extracting."""
    pass


class MissingBaseError(Error):
    """Error with missing a base string for a translation."""
    pass


class Extractor(object):
    """Translation extractor for finding translatable strings.

    Also supports extracting already translated strings from objects with tagging.

    ```
    foo@: "Extracted for translation."
    foo@es: "Not extracted, tagging overwrites value in document fields."
    foo@es@: "Extracted as the translation for foo@, tagging keeps the foo@ value."
    ```
    """

    TAG_EXTRACT = '@'
    TAG_COMMENT = '#'

    def __init__(self, pod):
        self.pod = pod
        self.results = ExtractedMessages()

    def _deep_extract(self, results, item, source=None, is_parent_tagged=False, comment=None):
        """Recursively extract an object into the results."""

        # String should have already been extracted if the key was tagged.
        if isinstance(item, basestring):
            # Values are tagged when the key is tagged.
            if is_parent_tagged:
                results.add_message(item, source, comment=comment)
            return

        # Handle arrays by going deeper and respecting the parent tagged state.
        if isinstance(item, collections.Sequence):
            for value in item:
                self._deep_extract(
                    results, value, source=source, comment=comment,
                    is_parent_tagged=is_parent_tagged)
            return

        for key, value in item.iteritems():
            is_tagged = isinstance(
                key, basestring) and key.endswith(self.TAG_EXTRACT)
            comment_key = '{}{}'.format(key, self.TAG_COMMENT)
            comment = item[comment_key] if comment_key in item else None
            self._deep_extract(
                results, value, source=source, is_parent_tagged=is_tagged, comment=comment)

    def extract_object(self, obj, source=None, default_locale=None):
        """Extract the translatable strings from an object.

        Translateable strings are tagged with an ending @ symbol.

        Keys can be tagged with a locale and a trailing @ (ex: foo@es@) to be extracted as a
        translation of the base string (foo@).
        """
        results = ExtractedMessages(default_locale=default_locale)
        self._deep_extract(results, obj, source=source)
        return results

    def extract_template(self, template):
        """Extract the translatable strings from a template."""
        pass


class ExtractedMessages(object):
    """Results from the extraction process to retrieve extracted strings with locale support."""

    def __init__(self, default_locale=None):
        self.default_locale = default_locale
        self.messages_to_meta = {}
        self.pattern_to_messages = {}

    @property
    def messages(self):
        """Messages that have been extracted."""
        return self.messages_to_meta.keys()

    def add_message(self, message, location=None, comment=None):
        """Add a message to the results."""
        if message not in self.messages_to_meta:
            self.messages_to_meta[message] = {
                'locations': set(),
                'comments': [],
            }
        if location:
            self.messages_to_meta[message]['locations'].add(location)
        if comment:
            self.messages_to_meta[message]['comments'].append(comment)

    def add_translation(self, pattern, message, translated):
        """Add a translation from the extraction."""
        if not message:
            raise MissingBaseError(
                u'Missing base string for translation: {}'.format(translated))

        if pattern not in self.pattern_to_messages:
            self.pattern_to_messages[pattern] = {}
        self.pattern_to_messages[pattern][message] = translated

    def get_translations(self, locale):
        """Retrieve the translations that match a given locale."""
        translations = {}
        locale = str(locale)

        # Only return the translations that match the locale pattern to the
        # locale.
        for locale_pattern, messages in self.pattern_to_messages.iteritems():
            locale_re = re.compile(locale_pattern)
            if locale_re.search(locale):
                for message, translation in messages.iteritems():
                    translations[message] = translation

        return translations


# Ideas

# extract_files
# - Provided a path generator.
# - Read each file.
#   - Yaml files parsed with raw yaml parser.
#   - Non-yaml files parsed for yaml front_matter.
# extract_object with the parsed yaml object.

# extract_templates
# - Provided a path generator.
# - Read each file.
# - Use bable extraction on the template to find static strings.
