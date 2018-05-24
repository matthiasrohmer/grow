"""Base class for the preprocess hook."""

from grow.extensions.hooks import base_hook


class PreprocessHook(base_hook.BaseHook):
    """Hook for preprocess."""

    KEY = 'preprocess'
    NAME = 'Preprocess'
    KIND = None

    # pylint: disable=arguments-differ
    def should_trigger(self, config, names, tags, run_all, *_args, **_kwargs):
        """Determine if the preprocess should trigger."""
        name = config.get('name')
        kind = config.get('kind')
        config_tags = config.get('tags', [])
        autorun = config.get('autorun', True)

        if kind != self.KIND:
            return False

        if names and name in names:
            return True
        elif tags and set(config_tags).intersection(tags):
            return True
        elif autorun or run_all:
            return True
        return False

    # pylint: disable=arguments-differ,unused-argument
    def trigger(self, previous_result, config, names, tags, run_all, rate_limit, *_args, **_kwargs):
        """Trigger the preprocess hook."""
        if previous_result:
            return previous_result
        return None
