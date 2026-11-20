from abc import ABC,abstractmethod

class DocLoader(ABC):

    @abstractmethod
    def load_all_docs():
        pass
    @abstractmethod
    def lazy_load_docs():
        pass
    