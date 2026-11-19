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