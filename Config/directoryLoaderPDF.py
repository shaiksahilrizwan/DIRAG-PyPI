try:
    from .docLoader import DocLoader
except ImportError:
    from Config.docLoader import DocLoader

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader


class DirectoryLoaderPDF(DocLoader):
    def __init__(self, dir_path: str):
        self.loader = DirectoryLoader(
            path=dir_path,
            glob="*.pdf",
            loader_cls=PyPDFLoader,
        )
        self.docs = None

    def load_all_docs(self):
        docs = self.loader.load()
        self.docs = docs if docs else []
        return self.docs

    def lazy_load_docs(self):
        return self.loader.lazy_load()