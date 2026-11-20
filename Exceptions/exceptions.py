class InvalidConfigJson(Exception):
    """Raised when DIRAG config JSON is malformed"""
    pass
class InvalidDictKeys(Exception):
    """Raised when Invalid Keys are accessed in dict"""
    pass
class InvalidSession(Exception):
    """Raised when Session key is Invalid/Session Not found"""
    pass
class SessionSaveError(Exception):
    """Raised when unable to save Session"""
    pass
class NoDocsFound(Exception):
    """Raised when no documents found/Empty Documnets for embedding"""
    pass
class VectorStoreSaveError(Exception):
    """Raised when unable to save docs in Vector store"""
    pass
class VectorSearchFail(Exception):
    """Raised when Vector Search Fails"""
    pass