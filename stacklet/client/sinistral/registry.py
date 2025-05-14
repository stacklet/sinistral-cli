# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0

from .exceptions import InvalidInputException


class PluginRegistry:
    def __init__(self, plugin_type):
        self.plugin_type = plugin_type
        self._factories = {}
        self.items = self._factories.items
        self.keys = self._factories.keys

    def register(self, name):
        # invoked as class decorator
        def _register_class(klass):
            self._factories[name] = klass
            klass.type = name
            return klass

        return _register_class

    def get(self, name, default=None):
        if name in self._factories:
            return self._factories[name]
        elif default is None:
            raise InvalidInputException(f"Unknown {self.plugin_type} plugin: {name}")
        elif default in self._factories:
            return self._factories[default]
        else:
            raise InvalidInputException(f"Unknown {self.plugin_type} plugin: {name} or {default}")
