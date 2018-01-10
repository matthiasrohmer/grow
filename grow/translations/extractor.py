"""Grow translation extractor."""

from babel.messages import pofile


class Error(Exception):
    pass


class Extractor(object):

    def __init__(self, pod):
        self.pod = pod

    def extract_object(self, obj):
        pass


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
