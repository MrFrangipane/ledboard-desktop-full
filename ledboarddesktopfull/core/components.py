from dataclasses import dataclass

# from ledboarddesktopfull.components.project_persistence_ui import ProjectPersistenceUi
from ledboarddesktopfull.core.configuration import Configuration
from ledboarddesktopfull.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
    project_persistence_ui = None  # FIXME use an AbstractProjectPersistenceUi
