"""Utility functions for settings"""
import os
from pathlib import Path
import re


def joinpath(*paths, resolve=False):
    """Helper function to determine paths in config file"""
    base_dir = Path(__file__).parent.parent.resolve()
    result = base_dir.joinpath(*paths)
    if resolve:
        result.resolve()
    return str(result)


class Environment:
    """Helper class to access environental variables"""
    def __init__(self, prefix='', strict=False):
        def _attrname(name):
            result = re.sub(r'[^a-z0-9]', '_', name.lower())
            result = result[len(prefix):].strip('_')
            return result or name.lower()

        self._keys = {
            _attrname(key): key
            for key in os.environ.keys()
            if key.startswith(prefix)
        }
        self.prefix = prefix
        self._strict = strict

    def __dir__(self):
        attrs = set(self._keys.keys()) | set(super().__dir__())
        return sorted(list(attrs))

    def __getattr__(self, name):
        try:
            if name in self._keys:
                value = os.environ.get(self._keys[name])
            else:
                value = os.environ[name]
            try:
                return int(value)
            except ValueError:
                return value

        except KeyError:
            if not self._strict:
                return ''
            msg = (
                f'{self.prefix.upper()}_{name.upper()} '
                f'not found in {dir(self)}'
            )
            raise AttributeError(msg)
