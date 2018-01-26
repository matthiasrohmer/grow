"""Grow translation extractor."""

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

    def __init__(self, pod):
        self.pod = pod
        self.results = ExtractedMessages()

    def extract_object(self, obj, source=None):
        """Extract the translatable strings from an object.

        Translateable strings are tagged with an ending @ symbol.

        Keys can be tagged with a locale and a trailing @ (ex: foo@es@) to be extracted as a
        translation of the base string (foo@).
        """
        pass

    def extract_template(self, template):
        """Extract the translatable strings from a template."""
        pass


class ExtractedMessages(object):
    """Results from the extraction process to retrieve extracted strings with locale support."""

    def __init__(self):
        self.meesages_to_locations = {}
        self.pattern_to_messages = {}

    @property
    def messages(self):
        """Messages that have been extracted."""
        return self.meesages_to_locations.keys()

    def add_message(self, message, location=None):
        """Add a message to the results."""
        if message not in self.meesages_to_locations:
            self.meesages_to_locations[message] = set()
        if location:
            self.meesages_to_locations[message].add(location)

    def add_translation(self, pattern, message, translated):
        """Add a translation from the extraction."""
        if not message:
            raise MissingBaseError(u'Missing base string for translation: {}'.format(translated))

        if pattern not in self.pattern_to_messages:
            self.pattern_to_messages[pattern] = {}
        self.pattern_to_messages[pattern][message] = translated

    def get_translations(self, locale):
        """Retrieve the translations that match a given locale."""
        translations = {}
        locale = str(locale)

        # Only return the translations that match the locale pattern to the locale.
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
