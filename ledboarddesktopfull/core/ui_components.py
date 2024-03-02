from dataclasses import dataclass

from ledboarddesktopfull.core.configuration import Configuration
from ledboarddesktopfull.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class _Widgets:
    board_selector = None
    board_configurator = None
    board_illuminator = None
    scan = None

    # FIXME: make this a python extension ?
    def __getattribute__(self, item):
        attribute = super().__getattribute__(item)
        if attribute is None:
            raise RuntimeError(f"Widget '{item}' is not initialized")
        return attribute


@dataclass
class UiComponents(metaclass=SingletonMetaclass):
    configuration = Configuration()
    project_persistence = None
    widgets = _Widgets()

    # FIXME: make this a python extension ?
    def __getattribute__(self, item):
        attribute = super().__getattribute__(item)
        if attribute is None:
            raise RuntimeError(f"Ui Component '{item}' is not initialized")
        return attribute
